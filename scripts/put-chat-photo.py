#!/usr/bin/env python3
"""Send one chosen JPEG or PNG to the single-use Hype chat upload address; never print that address.

Usage: put-chat-photo.py "<exact photo path>" "<uploadUrl from chat-upload-start>"
Prints one line: "ok: ..." (exit 0) or "refused: ..." (exit 1).
Limits: 5 MiB, JPEG or PNG by file signature, Hype's own storage host only, no redirects, 60-second timeout.
"""
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

STORAGE_HOST = 'acllesvdddrhjnhtfeix.supabase.co'
UPLOAD_PATH = '/storage/v1/object/upload/sign/'
MAX_BYTES = 5 * 1024 * 1024
TIMEOUT_SECONDS = 60
SIGNATURES = ((b'\xff\xd8\xff', 'image/jpeg'), (b'\x89PNG\r\n\x1a\n', 'image/png'))


class Refused(Exception):
    pass


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):
        raise Refused('storage tried to send the photo somewhere else; start a new upload')


def check_address(url):
    parts = urllib.parse.urlsplit(url)
    if (parts.scheme != 'https' or parts.hostname != STORAGE_HOST or parts.port not in (None, 443)
            or parts.username or parts.password or not parts.path.startswith(UPLOAD_PATH)
            or not parts.query or parts.fragment):
        raise Refused('that is not a Hype chat upload address; start a new upload')


def read_photo(path):
    if not os.path.isfile(path):
        raise Refused('no photo file at that exact path; ask the person for the full path')
    size = os.path.getsize(path)
    if size == 0:
        raise Refused('the photo file is empty')
    if size > MAX_BYTES:
        raise Refused('the photo is larger than 5 MiB; ask for a smaller copy')
    with open(path, 'rb') as photo:
        data = photo.read(MAX_BYTES + 1)
    if len(data) != size:
        raise Refused('the photo changed while it was being read; try again')
    for signature, content_type in SIGNATURES:
        if data.startswith(signature):
            return data, content_type
    raise Refused('only JPEG or PNG photos can be sent')


def upload(path, url, opener=None):
    check_address(url)
    data, content_type = read_photo(path)
    request = urllib.request.Request(url, data=data, method='PUT', headers={
        'Content-Type': content_type, 'x-upsert': 'false', 'Cache-Control': 'no-store'})
    opener = opener or urllib.request.build_opener(NoRedirect)
    try:
        with opener.open(request, timeout=TIMEOUT_SECONDS) as answer:
            status = answer.status
    except urllib.error.HTTPError as error:
        # The body is never printed: it can echo the address or the stored path.
        if error.code == 409 or b'already exists' in (error.read(2048) or b'').lower():
            raise Refused('this upload address was already used; start a new upload and never send this one')
        raise Refused('storage answered %s; start a new upload' % error.code)
    except (urllib.error.URLError, TimeoutError, OSError):
        raise Refused('could not reach storage; start a new upload')
    if not 200 <= status < 300:
        raise Refused('storage answered %s; start a new upload' % status)
    return '%d bytes (%s)' % (len(data), content_type)


def main(argv):
    if len(argv) != 2:
        print('refused: run with exactly the photo path and the upload address')
        return 1
    try:
        print('ok: sent ' + upload(argv[0], argv[1]))
        return 0
    except Refused as reason:
        print('refused: %s' % reason)
        return 1


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
