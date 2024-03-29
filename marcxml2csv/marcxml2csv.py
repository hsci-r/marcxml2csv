#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 15 18:59:15 2021

@author: jiemakel
"""

import csv
import gzip
import itertools
import os
import zipfile
from functools import reduce
from pathlib import Path
from typing import Iterator, Tuple

from hsciutil.fs import expand_globs

import click as click
import tqdm
from lxml import etree


def convert_record(n, record, co):
    f = 1
    for field in record:
        if field.tag == '{http://www.loc.gov/MARC21/slim}leader':
            co.writerow([n, f, '', 'leader', '', field.text])
        elif field.tag == '{http://www.loc.gov/MARC21/slim}controlfield':
            co.writerow(([n, f, '', field.attrib['tag'], '', field.text]))
        elif field.tag == '{http://www.loc.gov/MARC21/slim}datafield':
            tag = field.attrib['tag']
            if field.attrib['ind1'] != ' ':
                co.writerow([n, f, '', tag, 'ind1', field.attrib['ind1']])
            if field.attrib['ind2'] != ' ':
                co.writerow([n, f, '', tag, 'ind2', field.attrib['ind2']])
            sf = 1
            for subfield in field:
                co.writerow([n, f, sf, tag, subfield.attrib['code'], subfield.text])
                sf += 1
        else:
            raise Exception('Unknown field ' + field.tag)
        f += 1


@click.command
@click.option("-o", "--output", help="Output CSV/TSV (gz) file", required=True)
@click.argument('input', nargs=-1)
def convert(input: list[str], output: str) -> None:
    """Convert from MARCXML (gz/zip) INPUT files (actually glob patterns, parsed recursively) into (gzipped) CSV/TSV"""
    with gzip.open(output, 'wt') if output.endswith(".gz") else open(output, "wt") as of:
        co = csv.writer(of, delimiter='\t' if '.tsv' in output else ',')
        co.writerow(['record_number', 'field_number', 'subfield_number', 'field_code', 'subfield_code', 'value'])
        n = 1

        def iterate_zipfile(input: Path) -> Iterator[Tuple[Path, int]]:
            zf = zipfile.ZipFile(input)
            zp = zipfile.Path(zf)
            return map(lambda filepath: (filepath,zf.getinfo(filepath.name).file_size), zp.iterdir())

        input_files = list(itertools.chain.from_iterable(map(lambda path: iterate_zipfile(path) if path.name.endswith(".zip") else [(path, path.stat().st_size)], expand_globs(input, recurse=True))))
        tsize = reduce(lambda tsize, path: tsize + path[1], input_files, 0)
        pbar = tqdm.tqdm(total=tsize, unit='b', unit_scale=True, unit_divisor=1024)
        processed_files_tsize = 0
        for (input_path, input_size) in input_files:
            pbar.set_description(f"Processing {input_path}")
            with input_path.open("rb") as oinf:
                with gzip.open(oinf, 'rb') if input_path.name.endswith(".gz") else oinf as inf:
                    context = etree.iterparse(inf, events=('end',), tag='{http://www.loc.gov/MARC21/slim}record')
                    for _, elem in context:
                        convert_record(n, elem, co)
                        n += 1
                        elem.clear()
                        while elem.getprevious() is not None:
                            del elem.getparent()[0]
                        pbar.n = processed_files_tsize + oinf.tell()
                        pbar.update(0)
                    del context
            processed_files_tsize += input_size


if __name__ == '__main__':
    convert()
