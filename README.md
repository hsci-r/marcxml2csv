# marcxml2csv

A simple converter of MARCXML to CSV/TSV. The resulting CSV/TSV has been designed to be easy to use as a data table, but also to retain all ordering informaation in the original when such is needed. The format is as follows:
`record_number,field_number,subfield_number,field_code,subfield_code,value`

Here, `record_number` identifies the MARC record, while `field_number` and `subfield_number` can be used for more exact filtering / reconstructing the original MARC flow if needed.

For the leader and control fields, `subfield_number` will be empty.

For data fields, `ind1` and `ind2` values are reported as separate rows with the `subfield_code` being `ind1` or `ind2`, but only when non-empty. The also have an empty `subfield_number`.
