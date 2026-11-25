#!/usr/bin/env python3
"""PUT one local photo once; never print or accept a signed address in argv.

Usage: python3 -I put-chat-photo.py PHOTO [PRIVATE_START_RESPONSE_JSON_FILE]
Without a response file, read the chat-upload-start response JSON from stdin.
Print exactly uploaded (exit 0), refused: <fixed reason> (exit 1), or unknown (exit 2).
This validates type/size/header dimensions, not full decoding or EXIF orientation;
save the photo upright first. Hype revalidates it before publishing.
"""
import datetime
import http.client
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request

STORAGE_HOST = 'acllesvdddrhjnhtfeix.supabase.co'
UPLOAD_PATH = re.compile(
    r'/storage/v1/object/upload/sign/chat-upload-staging/'
    r'[0-9a-f-]{36}/[0-9a-f-]{36}\.(jpg|png)\Z')
MAX_BYTES = 5 * 1024 * 1024
MAX_EDGE = 2048
TIMEOUT_SECONDS = 60


class Refused(Exception):
    pass


class Unknown(Exception):
    pass


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):
        raise Refused('storage redirect blocked')


def check_address(url):
    try:
        parts = urllib.parse.urlsplit(url)
        query = urllib.parse.parse_qs(parts.query, strict_parsing=True)
        valid = (parts.scheme == 'https' and parts.hostname == STORAGE_HOST
                 and parts.port in (None, 443) and not parts.username and not parts.password
                 and UPLOAD_PATH.fullmatch(parts.path) and not parts.fragment
                 and set(query) == {'token'} and len(query['token']) == 1
                 and not any(char.isspace() or ord(char) < 32 or ord(char) == 127 for char in url))
    except ValueError:
        valid = False
    if not valid:
        raise Refused('not a Hype chat upload address')


def read_address(source):
    try:
        raw = source.read(32769)
        if len(raw) > 32768:
            raise ValueError()
        response = json.loads(raw)
        if (not isinstance(response, dict)
                or set(response) != {'uploadId', 'uploadUrl', 'expiresAt'}
                or not isinstance(response['uploadId'], str) or not response['uploadId']
                or not isinstance(response['uploadUrl'], str) or len(response['uploadUrl']) > 8192
                or not isinstance(response['expiresAt'], str)):
            raise ValueError()
        expiry = datetime.datetime.fromisoformat(response['expiresAt'].replace('Z', '+00:00'))
        if expiry.tzinfo is None:
            raise ValueError()
    except (ValueError, OSError, UnicodeError, RecursionError):
        raise Refused('invalid upload-start response') from None
    if expiry <= datetime.datetime.now(datetime.timezone.utc):
        raise Refused('upload receipt expired')
    check_address(response['uploadUrl'])
    return response['uploadUrl']


def image_dimensions(data):
    if data.startswith(b'\x89PNG\r\n\x1a\n'):
        if len(data) >= 33 and data[8:16] == b'\x00\x00\x00\rIHDR':
            return 'image/png', int.from_bytes(data[16:20], 'big'), int.from_bytes(data[20:24], 'big')
    elif data.startswith(b'\xff\xd8\xff'):
        at = 2
        while at < len(data) and data[at] == 0xff:
            while at < len(data) and data[at] == 0xff:
                at += 1
            if at >= len(data):
                break
            marker = data[at]
            at += 1
            if marker in (0xda, 0xd9):
                break
            if marker == 1 or 0xd0 <= marker <= 0xd7:
                continue
            length = int.from_bytes(data[at:at + 2], 'big')
            if length < 2 or at + length > len(data):
                break
            if marker in (0xc0, 0xc1, 0xc2, 0xc3, 0xc5, 0xc6, 0xc7,
                          0xc9, 0xca, 0xcb, 0xcd, 0xce, 0xcf) and length >= 8:
                return 'image/jpeg', int.from_bytes(data[at + 5:at + 7], 'big'), int.from_bytes(data[at + 3:at + 5], 'big')
            at += length
    else:
        raise Refused('only JPEG or PNG photos can be sent')
    raise Refused('unreadable photo dimensions')


def read_photo(path):
    try:
        if not os.path.isfile(path):
            raise Refused('no photo file at that exact path')
        with open(path, 'rb') as photo:
            size = os.fstat(photo.fileno()).st_size
            if size == 0:
                raise Refused('photo is empty')
            if size > MAX_BYTES:
                raise Refused('photo is larger than 5 MiB')
            data = photo.read(MAX_BYTES + 1)
    except OSError:
        raise Refused('photo could not be read') from None
    if len(data) != size:
        raise Refused('photo changed while being read')
    content_type, width, height = image_dimensions(data)
    if min(width, height) < 1:
        raise Refused('unreadable photo dimensions')
    if max(width, height) > MAX_EDGE:
        raise Refused('photo is larger than 2048 px on the long edge')
    return data, content_type


def upload(path, url, opener=None):
    check_address(url)
    data, content_type = read_photo(path)
    request = urllib.request.Request(url, data=data, method='PUT', headers={
        'Content-Type': content_type, 'x-upsert': 'false', 'Cache-Control': 'no-store'})
    opener = opener or urllib.request.build_opener(urllib.request.ProxyHandler({}), NoRedirect)
    try:
        with opener.open(request, timeout=TIMEOUT_SECONDS) as answer:
            status = answer.status
    except urllib.error.HTTPError as error:
        # Never read or print response bodies, reasons or exceptions: they can echo the signed address.
        status = error.code
        error.close()
    except (urllib.error.URLError, OSError, http.client.HTTPException):
        raise Unknown() from None
    if 200 <= status < 300:
        return
    if 300 <= status < 400:
        raise Refused('storage redirect blocked')
    if status == 409:
        raise Refused('upload address already used')
    if status in (400, 401, 403, 404, 405, 410, 413, 415, 422):
        raise Refused('storage rejected upload')
    raise Unknown()


def main(argv):
    if len(argv) not in (1, 2):
        print('refused: use a photo path and optional private response file')
        return 1
    try:
        if len(argv) == 2:
            with open(argv[1], encoding='utf-8') as source:
                url = read_address(source)
        else:
            url = read_address(sys.stdin)
        upload(argv[0], url)
    except Refused as reason:
        print('refused: ' + str(reason))
        return 1
    except (OSError, ValueError):
        print('refused: input could not be read')
        return 1
    except (Unknown, KeyboardInterrupt):
        print('unknown')
        return 2
    print('uploaded')
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
