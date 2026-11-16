#!/usr/bin/env python3
"""Check the chat photo uploader with a fake connection: no network, made-up files only."""
import contextlib
import email.message
import io
from pathlib import Path
import runpy
import tempfile
import urllib.error

uploader = runpy.run_path(str(Path(__file__).with_name('put-chat-photo.py')))
Refused = uploader['Refused']
GOOD = ('https://acllesvdddrhjnhtfeix.supabase.co/storage/v1/object/upload/sign/chat/made-up/one.png'
        '?token=made-up-not-a-secret')
PNG = b'\x89PNG\r\n\x1a\n' + b'0' * 64
JPEG = b'\xff\xd8\xff\xe0' + b'0' * 64


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


def http_error(code, body=b''):
    return urllib.error.HTTPError(GOOD, code, 'made-up', email.message.Message(), io.BytesIO(body))


def refused(call, words):
    try:
        call()
    except Refused as reason:
        assert words in str(reason), (words, str(reason))
        return
    raise AssertionError('not refused: ' + words)


with tempfile.TemporaryDirectory() as folder:
    root = Path(folder)
    png, jpeg, text, empty, big = (root / name for name in ('a.png', 'b.jpg', 'c.png', 'd.png', 'e.png'))
    png.write_bytes(PNG)
    jpeg.write_bytes(JPEG)
    text.write_bytes(b'not an image at all')
    empty.write_bytes(b'')
    big.write_bytes(b'\x89PNG\r\n\x1a\n' + b'0' * (5 * 1024 * 1024))

    for bad in ('http://acllesvdddrhjnhtfeix.supabase.co/storage/v1/object/upload/sign/x?token=t',
                'https://example.test/storage/v1/object/upload/sign/x?token=t',
                'https://acllesvdddrhjnhtfeix.supabase.co.example.test/storage/v1/object/upload/sign/x?token=t',
                'https://user:pw@acllesvdddrhjnhtfeix.supabase.co/storage/v1/object/upload/sign/x?token=t',
                'https://acllesvdddrhjnhtfeix.supabase.co:8443/storage/v1/object/upload/sign/x?token=t',
                'https://acllesvdddrhjnhtfeix.supabase.co/storage/v1/object/public/x?token=t',
                'https://acllesvdddrhjnhtfeix.supabase.co/storage/v1/object/upload/sign/x',
                'https://acllesvdddrhjnhtfeix.supabase.co/storage/v1/object/upload/sign/x?token=t#frag'):
        opener = FakeOpener()
        refused(lambda: uploader['upload'](str(png), bad, opener), 'not a Hype chat upload address')
        assert not opener.requests, bad

    for path, words in ((root / 'missing.png', 'no photo file'), (empty, 'empty'),
                        (big, 'larger than 5 MiB'), (text, 'only JPEG or PNG'), (root, 'no photo file')):
        opener = FakeOpener()
        refused(lambda: uploader['upload'](str(path), GOOD, opener), words)
        assert not opener.requests, path

    for path, data, kind in ((png, PNG, 'image/png'), (jpeg, JPEG, 'image/jpeg')):
        opener = FakeOpener()
        assert uploader['upload'](str(path), GOOD, opener) == '%d bytes (%s)' % (len(data), kind)
        (request, timeout), = opener.requests
        assert request.get_method() == 'PUT' and request.data == data and timeout == 60
        assert request.get_header('Content-type') == kind and request.get_header('X-upsert') == 'false'

    for error, words in ((http_error(409), 'already used'),
                         (http_error(400, b'{"error":"Duplicate","message":"The resource already exists"}'),
                          'already used'),
                         (http_error(403), 'storage answered 403'),
                         (urllib.error.URLError('offline'), 'could not reach storage'),
                         (TimeoutError(), 'could not reach storage')):
        refused(lambda: uploader['upload'](str(png), GOOD, FakeOpener(error=error)), words)
    refused(lambda: uploader['upload'](str(png), GOOD, FakeOpener(status=302)), 'storage answered 302')
    refused(lambda: uploader['NoRedirect']().redirect_request(None, None, 307, 'x', {}, GOOD),
            'somewhere else')

    # The single printed line never carries the upload address or its token, even on a refusal.
    for opener_error in (None, http_error(500, GOOD.encode())):
        output = io.StringIO()
        original = uploader['upload']
        main = uploader['main']
        main.__globals__['upload'] = lambda p, u: original(p, u, FakeOpener(error=opener_error))
        with contextlib.redirect_stdout(output):
            code = main([str(png), GOOD])
        main.__globals__['upload'] = original
        printed = output.getvalue()
        assert code == (0 if opener_error is None else 1), printed
        assert 'token' not in printed and 'supabase' not in printed and printed.count('\n') == 1, printed
    output = io.StringIO()
    with contextlib.redirect_stdout(output):
        assert uploader['main']([str(png)]) == 1
    assert output.getvalue().startswith('refused: run with exactly')

print('PASS put-chat-photo selftest')
