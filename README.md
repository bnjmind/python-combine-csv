# python-combine-csv
Combine multiple .csv files with the same structure into a single .csv file, whilst optionally filtering on specific columns.

## 0. Usage
```bash
python3 combine_csv.py --data [--output] [--filter]
```

**data**

1. Comma separated list of .csv files
2. Path to folder with trailing '/' that contains .csv files

**output**

Path to the output file. Defaults to 'combined_files.csv' in current folder.

**filter**

Comma separated list of filters.

Possible comparisons:

* column_name __IN__ "list|of|things"
* column_name __>__ 300
* column_name __>=__ 100
* column_name __<__ 200
* column_name __<=__ 800
* column_name __==__ "thing"
* column_name __!=__ "thing"
