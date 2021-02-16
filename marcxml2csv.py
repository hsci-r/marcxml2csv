#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 15 18:59:15 2021

@author: jiemakel
"""

# %%
from lxml import etree
import csv
import argparse

def parse_arguments():
    ap = argparse.ArgumentParser(description="MARCXML to CSV converter")  
    ap.add_argument("-o","--output",help="Output CSV file",required=True)
    ap.add_argument("-i","--input",help="Input MARXCML file",required=True)
    return (ap.parse_args())

# %%

def convert_record(n,record,co):
    f = 1
    for field in record:
        if field.tag == '{http://www.loc.gov/MARC21/slim}leader':
            co.writerow([n,f,'','leader','',field.text])
        elif field.tag == '{http://www.loc.gov/MARC21/slim}controlfield':
            co.writerow(([n,f,'',field.attrib['tag'],'',field.text]))
        elif field.tag == '{http://www.loc.gov/MARC21/slim}datafield':
            tag = field.attrib['tag']
            if field.attrib['ind1']!=' ':
                co.writerow([n,f,'',tag,'ind1',field.attrib['ind1']])
            if field.attrib['ind2']!=' ':
                co.writerow([n,f,'',tag,'ind2',field.attrib['ind2']])
            sf = 1
            for subfield in field:
                co.writerow([n,f,sf,tag,subfield.attrib['code'],subfield.text])
                sf += 1
        else:
            raise Exception('Unknown field '+field.tag)
        f+=1


def convert(input: str, output: str) -> None:
    with open(output,"w") as of:
        co = csv.writer(of)
        co.writerow(['record_number','field_number','subfield_number','field_code','subfield_code','value'])
        n = 1
        context = etree.iterparse(input, events=('end',), tag='{http://www.loc.gov/MARC21/slim}record')
        for _, elem in context:
            convert_record(n,elem,co)
            n += 1
            elem.clear()
            while elem.getprevious() is not None:
                del elem.getparent()[0]
        del context

# %%

def main():
    args = parse_arguments()
    convert(args.input,args.output)
    
if __name__ == '__main__':
    main()