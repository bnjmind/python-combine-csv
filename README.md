# python-combine-csv
Combine multiple .csv files with the same structure into a single .csv file, whilst optionally filtering specific location IDs.

## 0. Usage
```
python3 combine_csv.py --folder "path/to/folder" [--output "output/file.csv"] [--id "id1,id2,id3"]
```
Where '--folder' is a relative path to a folder containing the .csv files, '--output' is a relative path to a .csv file, and '--id' is a comma separated string with location IDs.
