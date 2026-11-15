#!/usr/bin/env python3
"""Check the read-only converter using only small, in-memory workbooks."""
import csv
import io
from pathlib import Path
import runpy
import zipfile

converter = runpy.run_path(str(Path(__file__).with_name('xlsx-to-csv.py')))
NS = 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'
REL = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'


def workbook(rows, target='worksheets/sheet1.xml', shared=True):
    data = io.BytesIO()
    with zipfile.ZipFile(data, 'w', zipfile.ZIP_DEFLATED) as book:
        book.writestr('[Content_Types].xml', '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/><Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/><Override PartName="/xl/worksheets/sheet2.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/><Override PartName="/xl/sharedStrings.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sharedStrings+xml"/></Types>')
        book.writestr('_rels/.rels', f'<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="r1" Type="{REL}/officeDocument" Target="xl/workbook.xml"/></Relationships>')
        book.writestr('xl/workbook.xml', f'<workbook xmlns="{NS}" xmlns:r="{REL}"><sheets><sheet name="Family" sheetId="1" r:id="r1"/><sheet name="Other" sheetId="2" r:id="r2"/></sheets></workbook>')
        book.writestr('xl/_rels/workbook.xml.rels', f'<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="r1" Type="{REL}/worksheet" Target="{target}"/><Relationship Id="r2" Type="{REL}/worksheet" Target="/xl/worksheets/sheet2.xml"/></Relationships>')
        book.writestr('xl/worksheets/sheet1.xml', f'<worksheet xmlns="{NS}"><sheetData>{rows}</sheetData></worksheet>')
        book.writestr('xl/worksheets/sheet2.xml', f'<worksheet xmlns="{NS}"><sheetData><row><c t="inlineStr"><is><t>Other sheet</t></is></c></row></sheetData></worksheet>')
        if shared:
            book.writestr('xl/sharedStrings.xml', f'<sst xmlns="{NS}"><si><r><t>Ari</t></r><r><t> Bell</t></r></si></sst>')
    data.seek(0)
    return data


SAMPLE_ROWS = '<row r="1"><c r="A1" t="s"><v>0</v></c><c r="C1" t="inlineStr"><is><t>comma, quote &quot; and\nnewline</t></is></c><c r="D1"><v>45000</v></c><c r="E1"/><c r="F1"><f>1+1</f><v>2</v></c><c r="G1"><f>1+2</f></c></row><row r="3"><c r="B3"><v>7</v></c></row>'


def self_test():
    convert = converter['convert']
    text, notices = convert(workbook(SAMPLE_ROWS))
    assert list(csv.reader(io.StringIO(text))) == [
        ['Ari Bell', '', 'comma, quote " and\nnewline', '45000', '', '2', ''],
        [], ['', '7'],
    ]
    assert 'Dates remain stored numbers' in notices[0]
    assert notices[-1] == "Read sheet 'Family' (1 of 2: Family, Other)."
    assert convert(workbook(SAMPLE_ROWS), 'Other')[0] == 'Other sheet\n'
    assert convert(workbook('<row><c t="inlineStr"><is><t>Sam</t></is></c></row>', shared=False))[0] == 'Sam\n'
    print('PASS: workbook strings, numbers, empty positions, cached formulas and sheet selection')

    text, notices = convert(workbook('<row r="5000"><c r="CV5000"><v>9</v></c><c r="CW5000"><v>10</v></c></row><row r="5001"><c><v>11</v></c></row>'))
    rows = list(csv.reader(io.StringIO(text)))
    assert len(rows) == 5000 and len(rows[-1]) == 100 and rows[-1][-1] == '9'
    assert any('5,000 rows' in n for n in notices) and any('100 columns' in n for n in notices)
    print('PASS: row and column limits disclose incomplete CSV')

    for target in ('../outside.xml', '/outside.xml', 'worksheets/../../outside.xml', 'https://example.invalid/sheet.xml', 'worksheets\\sheet1.xml'):
        try:
            convert(workbook('', target=target))
        except converter['WorkbookError']:
            pass
        else:
            raise AssertionError('Unsafe worksheet path accepted')
    for data, sheet in ((io.BytesIO(b'not a workbook'), None), (workbook(''), 'Missing'), (workbook('<row><c t="s"><v>9</v></c></row>'), None), (workbook('<row>'), None)):
        try:
            convert(data, sheet)
        except (ValueError, zipfile.BadZipFile, converter['ET'].ParseError):
            pass
        else:
            raise AssertionError('Invalid workbook accepted')
    print('PASS: unsafe ZIP paths, missing sheets and invalid workbooks are rejected')

    globals_ = convert.__globals__
    for limit in ('MAX_XML_BYTES', 'MAX_WORKBOOK_BYTES', 'MAX_CSV_BYTES'):
        previous = globals_[limit]
        try:
            globals_[limit] = 8
            try:
                convert(workbook(SAMPLE_ROWS))
            except converter['WorkbookError']:
                pass
            else:
                raise AssertionError('Workbook reading limit ignored')
        finally:
            globals_[limit] = previous
    for unsafe in ('<!DOCTYPE row>', '<!entity x "y">'):
        try:
            convert(workbook(unsafe))
        except converter['WorkbookError']:
            pass
        else:
            raise AssertionError('XML declaration accepted')
    print('PASS: XML, workbook and CSV output limits and unsafe XML declarations are enforced')


if __name__ == '__main__':
    self_test()
