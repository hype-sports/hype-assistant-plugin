#!/usr/bin/env python3
"""Read one .xlsx sheet as CSV on stdout; never extract or write files.

Dates stay as stored numbers. Formulas are not run: only cached values are read.
Limits: 5,000 rows, 100 columns, 16 MiB per XML part/CSV output, 50 MiB per workbook.
"""
import argparse
import csv
import io
from pathlib import PurePosixPath
import re
import os
import sys
import xml.etree.ElementTree as ET
import zipfile
import zlib

MAX_ROWS = 5000
MAX_COLUMNS = 100
MAX_XML_BYTES = 16 * 1024 * 1024
MAX_WORKBOOK_BYTES = 50 * 1024 * 1024
MAX_CSV_BYTES = 16 * 1024 * 1024


class WorkbookError(ValueError):
    pass


def xml_bytes(book, path):
    if book.getinfo(path).file_size > MAX_XML_BYTES:
        raise WorkbookError('An XML part exceeds the 16 MiB reading limit; use a smaller CSV export.')
    with book.open(path) as part:
        data = part.read(MAX_XML_BYTES + 1)
    if len(data) > MAX_XML_BYTES:
        raise WorkbookError('An XML part exceeds the 16 MiB reading limit; use a smaller CSV export.')
    # Reject declarations rather than expand entities from an untrusted workbook.
    if b'<!DOCTYPE' in data.upper() or b'<!ENTITY' in data.upper() or b'\x00' in data:
        raise WorkbookError('Unsupported workbook XML; use a CSV export.')
    return data


def sheet_path(target):
    if not target or any(char in target for char in '\\:?#'):
        raise WorkbookError('Invalid worksheet path inside the workbook.')
    path = target[1:] if target.startswith('/') else 'xl/' + target
    if any(part in ('', '.', '..') for part in path.split('/')) or not path.startswith('xl/'):
        raise WorkbookError('Worksheet paths must stay inside xl/.')
    return str(PurePosixPath(path))


def string_text(element):
    return ''.join(t.text or '' for t in element.iter() if t.tag.rsplit('}', 1)[-1] == 't')


def convert(source, sheet_name=None):
    """Return bounded CSV and notices, so invalid input never prints partial rows."""
    source.seek(0, 2)
    if source.tell() > MAX_WORKBOOK_BYTES:
        raise WorkbookError('Workbook exceeds the 50 MiB reading limit; use a smaller CSV export.')
    source.seek(0)
    with zipfile.ZipFile(source) as book:
        workbook = ET.fromstring(xml_bytes(book, 'xl/workbook.xml'))
        if workbook.tag.rsplit('}', 1)[-1] != 'workbook':
            raise WorkbookError('Not a valid .xlsx workbook.')
        sheets = workbook.findall('{*}sheets/{*}sheet')
        sheet = next((s for s in sheets if sheet_name is None or s.get('name') == sheet_name), None)
        if sheet is None:
            raise WorkbookError('No matching worksheet found; check the sheet name or use a CSV export.')
        relation_id = next((value for key, value in sheet.attrib.items() if key.rsplit('}', 1)[-1] == 'id'), None)
        relations = ET.fromstring(xml_bytes(book, 'xl/_rels/workbook.xml.rels'))
        relation = next((r for r in relations if r.get('Id') == relation_id), None)
        if relation is None or relation.get('TargetMode', 'Internal') != 'Internal' or not relation.get('Type', '').endswith('/worksheet'):
            raise WorkbookError('Invalid or unsupported worksheet relationship.')
        path = sheet_path(relation.get('Target'))
        strings = []
        if 'xl/sharedStrings.xml' in book.namelist():
            shared = ET.fromstring(xml_bytes(book, 'xl/sharedStrings.xml'))
            if shared.tag.rsplit('}', 1)[-1] != 'sst':
                raise WorkbookError('Invalid shared strings in workbook.')
            strings = [string_text(item) for item in shared.findall('{*}si')]
        output = io.StringIO(newline='')
        writer = csv.writer(output, lineterminator='\n')
        notices = ['Dates remain stored numbers; formulas are not run (cached values only).']
        previous_row = 0
        output_bytes = 0
        column_limit = False
        root = None
        for event, element in ET.iterparse(io.BytesIO(xml_bytes(book, path)), events=('start', 'end')):
            if root is None:
                root = element
                if root.tag.rsplit('}', 1)[-1] != 'worksheet':
                    raise WorkbookError('Not a valid worksheet.')
            if event != 'end' or element.tag.rsplit('}', 1)[-1] != 'row':
                continue
            row_number = int(element.get('r', previous_row + 1))
            if row_number <= previous_row:
                raise WorkbookError('Invalid worksheet row order.')
            if row_number > MAX_ROWS:
                notices.append('Stopped at 5,000 rows; CSV is incomplete. Use a smaller CSV export for the rest.')
                break
            while previous_row + 1 < row_number:
                writer.writerow([])
                output_bytes += 1
                previous_row += 1
            values = []
            previous_column = 0
            for cell in element.findall('{*}c'):
                reference = cell.get('r')
                column = previous_column + 1
                if reference is not None:
                    match = re.fullmatch(r'([A-Z]{1,3})([1-9][0-9]*)', reference)
                    if not match or int(match[2]) != row_number:
                        raise WorkbookError('Invalid worksheet cell position.')
                    column = 0
                    for letter in match[1]:
                        column = column * 26 + ord(letter) - ord('A') + 1
                if column <= previous_column:
                    raise WorkbookError('Invalid worksheet column order.')
                if column > MAX_COLUMNS:
                    column_limit = True
                    break
                previous_column = column
                values.extend([''] * (column - len(values)))
                value = cell.findtext('{*}v', default='')
                if cell.get('t') == 's':
                    index = int(value)
                    if index < 0 or index >= len(strings):
                        raise WorkbookError('Invalid shared string reference.')
                    value = strings[index]
                elif cell.get('t') == 'inlineStr':
                    inline = cell.find('{*}is')
                    value = '' if inline is None else string_text(inline)
                values[column - 1] = value
            # Bound expansion when many cells reuse the same large shared string.
            output_bytes += 1
            for value in values:
                output_bytes += len(value.encode('utf-8')) + value.count('"') + 3
                if output_bytes > MAX_CSV_BYTES:
                    raise WorkbookError('CSV exceeds the 16 MiB output budget; use a smaller CSV export.')
            writer.writerow(values)
            previous_row = row_number
            element.clear()
        if column_limit:
            notices.append('Stopped at 100 columns per row; CSV is incomplete. Additional columns were not read.')
        names = ', '.join(s.get('name', '') for s in sheets)
        notices.append(f"Read sheet '{sheet.get('name', '')}' ({sheets.index(sheet) + 1} of {len(sheets)}: {names}).")
        return output.getvalue(), notices


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('path', help='the exact .xlsx file chosen by the person')
    parser.add_argument('sheet', nargs='?', help='sheet name (default: first worksheet)')
    args = parser.parse_args()
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
    try:
        with open(args.path, 'rb') as source:
            text, notices = convert(source, args.sheet)
    except FileNotFoundError:
        # Names only, one folder, so the assistant never needs ls or find to locate an attached file.
        folder = os.path.dirname(os.path.abspath(args.path))
        try:
            found = sorted(n for n in os.listdir(folder) if n.lower().endswith('.xlsx') and not n.startswith('~$'))
        except OSError:
            found = []
        if found:
            shown = [os.path.join(folder, n) for n in found[:20]]
            more = f' (and {len(found) - 20} more)' if len(found) > 20 else ''
            listing = 'Spreadsheets in that folder: ' + ', '.join(shown) + more + '. If exactly one is clearly the same file, run once more with that full path; if more than one could be, ask the person which.'
        else:
            listing = 'None found in ' + folder + '.'
        print('Cannot find workbook: no file at ' + args.path + '. ' + listing + ' Otherwise ask the person for the exact path.', file=sys.stderr)
        return 1
    except WorkbookError as exc:
        print('Cannot read workbook: ' + str(exc), file=sys.stderr)
        return 1
    except (OSError, ValueError, KeyError, ET.ParseError, zipfile.BadZipFile, RuntimeError, NotImplementedError, EOFError, zlib.error):
        print('Cannot read workbook: not a valid, readable .xlsx file. Save it as CSV instead.', file=sys.stderr)
        return 1
    for notice in notices:
        print('# ' + notice, file=sys.stderr)
    sys.stdout.write(text)
    return 0


if __name__ == '__main__':
    sys.exit(main())
