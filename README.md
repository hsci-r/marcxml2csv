# marcxml2csv

A simple converter of (possibly gzipped) MARCXML/PICAXML to (possibly gzipped) CSV/TSV.

The resulting CSV/TSV has been designed to be easy to use as a data table, but also to retain all ordering informaation in the original when such is needed. The format is as follows:
`record_number,field_number,subfield_number,field_code,subfield_code,value`

Here, `record_number` identifies the MARC/PICA+ record, while `field_number` and `subfield_number` can be used for more exact filtering / reconstructing the original field flow if needed.

For the MARC leader and control fields, `subfield_number` will be empty.

For MARC data fields, `ind1` and `ind2` values are reported as separate rows with the `subfield_code` being `ind1` or `ind2`, but only when non-empty. The also have an empty `subfield_number`.

## Installation

Install from pypi with e.g. `pipx install marcxml2csv`.

## Usage

```
Usage: marcxml2csv [OPTIONS] [INPUT]...

  Convert from MARCXML (gz) input files into (gzipped) CSV/TSV

Options:
  -o, --output TEXT  Output CSV/TSV (gz) file  [required]
  --help             Show this message and exit.
```

```
Usage: picaxml2csv [OPTIONS] [INPUT]...

  Convert from PICAXML (gz) input files into (gzipped) CSV/TSV

Options:
  -o, --output TEXT  Output CSV/TSV (gz) file  [required]
  --help             Show this message and exit.
```

Files will be read/written using gzip if the filename ends with `.gz`. TSV format will be used if the output filename contains `.tsv`, otherwise CSV will be used.
