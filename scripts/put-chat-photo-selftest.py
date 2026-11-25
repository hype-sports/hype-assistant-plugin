#!/usr/bin/env python3
"""Offline upload checks with synthetic image headers and a stub connection; no network."""
import contextlib
import datetime
import email.message
import http.client
import io
import json
from pathlib import Path
import runpy
import struct
import sys
import tempfile
from unittest.mock import patch
import urllib.error
import urllib.request
import urllib.response

uploader = runpy.run_path(str(Path(__file__).with_name('put-chat-photo.py')))
Refused, Unknown = uploader['Refused'], uploader['Unknown']
GOOD = ('https://acllesvdddrhjnhtfeix.supabase.co/storage/v1/object/upload/sign/'
        'chat-upload-staging/00000000-0000-4000-8000-000000000001/'
        '00000000-0000-4000-8000-000000000002.png?token=offline-placeholder')
EXPIRES = (datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=5)).isoformat()
RESPONSE = {'uploadId': '00000000-0000-4000-8000-000000000003',
            'uploadUrl': GOOD, 'expiresAt': EXPIRES}


def png(width=1, height=1):
    return b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR' + struct.pack('>II', width, height) + b'\x08\x02\x00\x00\x00' + b'\x00' * 4


def jpeg(width=1, height=1, marker=0xc0):
    return (b'\xff\xd8\xff\xe0\x00\x04xx\xff' + bytes([marker])
            + b'\x00\x0b\x08' + struct.pack('>HH', height, width) + b'\x01\x01\x11\x00\xff\xd9')


class Answer:
    def __init__(self, status):
        self.status = status

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False


class FakeOpener:
    def __init__(self, status=200, error=None):
        self.status, self.error, self.requests = status, error, []

    def open(self, request, timeout):
        self.requests.append((request, timeout))
        if self.error:
            raise self.error
        return Answer(self.status)


def fails(call, exception, words=''):
    try:
        call()
    except exception as reason:
        assert words in str(reason), 'wrong closed refusal'
        return
    raise AssertionError('expected refusal or unknown')


def cli(args, code, line, opener=None, response=None):
    output, errors = io.StringIO(), io.StringIO()
    if response is None:
        response = json.dumps(RESPONSE)
    with (patch.object(sys, 'stdin', io.StringIO(response)),
          patch('urllib.request.build_opener', return_value=opener or FakeOpener()),
          contextlib.redirect_stdout(output), contextlib.redirect_stderr(errors)):
        assert uploader['main'](args) == code
    assert output.getvalue() == line + '\n', 'unexpected or unsafe output'
    assert errors.getvalue() == '', 'stderr must stay empty'


# Any accidental connection in a self-test is a failure, never a real upload.
with patch('socket.create_connection', side_effect=AssertionError('network forbidden')):
    with tempfile.TemporaryDirectory() as folder:
        root = Path(folder)
        photo = root / 'chosen.png'
        response_file = root / 'private-response.json'
        response_file.write_text(json.dumps(RESPONSE))
        photo.write_bytes(png())

        for bad in (GOOD.replace('https:', 'http:'), GOOD.replace('supabase.co', 'supabase.co.example.test'),
                    GOOD.replace('https://', 'https://user:pw@'), GOOD.replace('.co/', '.co:8443/'),
                    GOOD.replace('.co/', '.co:bad/'), GOOD.replace('chat-upload-staging/', 'another-bucket/'),
                    GOOD.replace('/upload/sign/', '/public/'), GOOD.split('?')[0], GOOD + '#fragment',
                    GOOD + '\n', GOOD + '&other=value', GOOD.replace('?token=', '?other=')):
            opener = FakeOpener()
            fails(lambda: uploader['upload'](str(photo), bad, opener), Refused, 'not a Hype chat upload address')
            assert not opener.requests
        print('PASS: only exact Hype staging addresses; invalid addresses make no request')

        for data, words in ((b'', 'empty'), (b'not an image', 'only JPEG or PNG'),
                            (png() + b'0' * uploader['MAX_BYTES'], 'larger than 5 MiB'),
                            (png(2049, 1), 'larger than 2048'), (png(1, 2049), 'larger than 2048'),
                            (jpeg(2049, 1), 'larger than 2048'), (jpeg(1, 2049), 'larger than 2048'),
                            (png(0, 1), 'unreadable'), (jpeg(1, 0), 'unreadable'),
                            (png()[:24], 'unreadable'), (b'\xff\xd8\xff\xe0\x00\xff', 'unreadable'),
                            (b'\xff\xd8\xff\xda\x00\x02', 'unreadable'), (b'\xff\xd8\xff\xff', 'unreadable')):
            photo.write_bytes(data)
            opener = FakeOpener()
            fails(lambda: uploader['upload'](str(photo), GOOD, opener), Refused, words)
            assert not opener.requests
        for path in (root, root / 'missing.png'):
            fails(lambda: uploader['upload'](str(path), GOOD, FakeOpener()), Refused, 'no photo file')
        print('PASS: size, type, both dimension axes and malformed headers refused before PUT')

        for data, kind in ((png(2048, 2048), 'image/png'), (jpeg(2048, 2048), 'image/jpeg'),
                           (jpeg(marker=0xc2), 'image/jpeg'),
                           (png() + b'0' * (uploader['MAX_BYTES'] - len(png())), 'image/png')):
            photo.write_bytes(data)
            opener = FakeOpener(status=201)
            assert uploader['upload'](str(photo), GOOD, opener) is None
            (request, timeout), = opener.requests
            assert request.full_url == GOOD and request.get_method() == 'PUT'
            assert request.data == data and timeout == 60
            assert request.get_header('Content-type') == kind
            assert request.get_header('X-upsert') == 'false'
        print('PASS: JPEG/PNG, progressive JPEG, exact 5 MiB/2048 px limits; one byte-identical no-overwrite PUT')

        photo.write_bytes(png())
        for code in (301, 302, 303, 307, 308, 400, 403, 409, 415, 500, 503, 408, 429):
            for error in (None, urllib.error.HTTPError(GOOD, code, GOOD, email.message.Message(), io.BytesIO(GOOD.encode()))):
                opener = FakeOpener(status=code, error=error)
                exception = Unknown if code in (500, 503, 408, 429) else Refused
                fails(lambda: uploader['upload'](str(photo), GOOD, opener), exception)
                assert len(opener.requests) == 1
        for error in (urllib.error.URLError(GOOD), TimeoutError(GOOD), OSError(GOOD),
                      http.client.RemoteDisconnected(GOOD)):
            opener = FakeOpener(error=error)
            fails(lambda: uploader['upload'](str(photo), GOOD, opener), Unknown)
            assert len(opener.requests) == 1
        class StubHTTPS(urllib.request.HTTPSHandler):
            def __init__(self, code):
                super().__init__()
                self.code, self.requests = code, []

            def https_open(self, request):
                self.requests.append(request)
                headers = email.message.Message()
                headers['Location'] = 'https://example.test/do-not-upload'
                answer = urllib.response.addinfourl(io.BytesIO(), headers, request.full_url, self.code)
                answer.msg = 'offline redirect'
                return answer

        for code in (301, 302, 303, 307, 308):
            handler = StubHTTPS(code)
            opener = urllib.request.build_opener(urllib.request.ProxyHandler({}), uploader['NoRedirect'], handler)
            fails(lambda: uploader['upload'](str(photo), GOOD, opener), Refused, 'redirect blocked')
            assert len(handler.requests) == 1
        print('PASS: real urllib redirect handling blocked offline; uncertainty stays unknown; no retries')

        cli([str(photo)], 0, 'uploaded')
        cli([str(photo), str(response_file)], 0, 'uploaded', response='unused')
        cli([], 1, 'refused: use a photo path and optional private response file')
        cli([str(photo), str(root / 'missing.json')], 1, 'refused: input could not be read')
        for bad in (GOOD, '{}', '[]', '{', 'x' * 32769,
                    json.dumps({**RESPONSE, 'uploadUrl': None}),
                    json.dumps({**RESPONSE, 'expiresAt': 'not-a-date'}),
                    json.dumps({**RESPONSE, 'expiresAt': '2099-01-01T00:00:00'}),
                    json.dumps({**RESPONSE, 'signedUrl': GOOD})):
            cli([str(photo)], 1, 'refused: invalid upload-start response', response=bad)
        cli([str(photo)], 1, 'refused: upload receipt expired',
            response=json.dumps({**RESPONSE, 'expiresAt': '2000-01-01T00:00:00Z'}))
        cli([str(photo)], 1, 'refused: storage rejected upload', opener=FakeOpener(error=
            urllib.error.HTTPError(GOOD, 400, GOOD, email.message.Message(), io.BytesIO(GOOD.encode()))))
        cli([str(photo)], 2, 'unknown', opener=FakeOpener(error=urllib.error.URLError(GOOD)))
        cli([str(photo)], 2, 'unknown', opener=FakeOpener(status=500))
        cli([str(photo)], 2, 'unknown', opener=FakeOpener(error=KeyboardInterrupt()))
        cli([str(photo)], 1, 'refused: invalid upload-start response', response='[' * 2000 + ']' * 2000)
        print('PASS: stdin/file response fields and expiry; closed stdout, empty stderr, no signed-address disclosure')

print('PASS put-chat-photo selftest (offline stub; no image decoder or live service)')
