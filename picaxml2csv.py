#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 15 18:59:15 2021

@author: jiemakel
"""

import csv
import gzip
import os
from functools import reduce

import click as click
from lxml import etree
import tqdm


def convert_record(n, record, co) -> None:
    f = 1
    for field in record:
        tag = field.attrib['tag']
        sf = 1
        for subfield in field:
            co.writerow([n, f, sf, tag, subfield.attrib['code'], subfield.text])
            sf += 1
        f += 1


@click.command
@click.option("-o", "--output", help="Output CSV/TSV (gz) file", required=True)
@click.argument('input', nargs=-1, type=click.Path())
def convert(input: list[str], output: str) -> None:
    """Convert from PICAXML (gz) input files into (gzipped) CSV/TSV"""
    with gzip.open(output, 'wt') if output.endswith(".gz") else open(output, "wt") as of:
        co = csv.writer(of, delimiter='\t' if '.tsv' in output else ',')
        co.writerow(['record_number', 'field_number', 'subfield_number', 'field_code', 'subfield_code', 'value'])
        n = 1
        tsize = reduce(lambda tsize, tweet_file_name: tsize + os.path.getsize(tweet_file_name), input, 0)
        pbar = tqdm.tqdm(total=tsize, unit='b', unit_scale=True, unit_divisor=1024)
        processed_files_tsize = 0
        for input_path in input:
            pbar.set_description(f"Processing {input_path}")
            with open(input_path, "rb") as oinf:
                with gzip.open(oinf, 'rb') if input_path.endswith(".gz") else oinf as inf:
                    context = etree.iterparse(inf, events=('end',), tag='{info:srw/schema/5/picaXML-v1.0}record')
                    for _, elem in context:
                        convert_record(n, elem, co)
                        n += 1
                        elem.clear()
                        while elem.getprevious() is not None:
                            del elem.getparent()[0]
                        pbar.n = processed_files_tsize + oinf.tell()
                        pbar.update(0)
                    del context
            processed_files_tsize += os.path.getsize(input_path)


if __name__ == '__main__':
    convert()