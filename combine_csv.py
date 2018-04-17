# import modules
import time
import glob
import argparse
import re
import operator
import sys

# parse options given to script
parser = argparse.ArgumentParser()
parser.add_argument("-d", "--data", help="The folder that contains the to be combined .csv files (with trailing '/')", metavar="", default="")
parser.add_argument("-o", "--output", help="The output file to be generated, defaults to 'combined_files.csv'", metavar="", default="combined_files.csv")
parser.add_argument("-f", "--filter", help="Filters applied to the rows in the source files (comma seperated)", metavar="", default="")
options = parser.parse_args()

input_datafile = options.data
input_outputfile = options.output
input_filter = options.filter

# start timer
timer = time.time()

# output that we're doing something
print("\nPreparing everything... (The script can be aborted by pressing ctrl+c)")

# split the given filters and put them in a list
input_filters = input_filter.split(",") if input_filter != "" else []

# create a new empty list
filters = []

# operator lookup
operators = {
    ">": operator.gt,
    ">=": operator.ge,
    "<": operator.lt,
    "<=": operator.le,
    "=": operator.eq,
    "==": operator.eq,
    "!=": operator.ne,
    "<>": operator.ne,
    "IN": operator.contains
}

# loop through all given filters
for filter in input_filters:

    # match them against a regular expression
    match = re.fullmatch("\s?(\w+)\s?(>=?|<=?|==?|!=|<>|IN)\s?(?:\'|\")?(.*[^\'\"])?(?:\'|\")?\s?", filter)

    # assume the value is not a number
    number = False
    value = match.group(3) or ""

    # try to interpret it as a number
    try:
        value = int(value)
    except ValueError:
        pass
    else:
        number = True

    # save the filter to the filter list
    filters.append({
        "column": match.group(1),
        "operator": operators[match.group(2)],
        "value": value,
        "number": number
    })

# open a new file that we will fill
combined = open(input_outputfile, "w")

# init counter
counter = 0

# start with empty file list
file_list = []

# fill the list of data files
if "," in input_datafile:
    file_list.extend(input_datafile.split(","))
elif options.data[-1:] == "/":
    file_list.extend(glob.glob(input_datafile + "*.csv"))

# list all files in directory
for i, name in enumerate(file_list):

    # update counter
    counter += 1

    # open file
    f = open(name, "r")

    # skip first line if not first file
    if (i != 0):
        next(f)

    # loop through lines
    for j, line in enumerate(f):

        # save the column names
        if (i == 0 and j == 0):
            columns = line.split(",")

        # check if the line should be filtered
        if (len(filters) > 0 and (i != 0 or j!= 0)):

            # save values from line in list
            values = line.split(",")

            # start with not filtering it
            filter_row = False

            # loop through filters
            for k, filter in enumerate(filters):

                value = values[columns.index(filter["column"])]

                # if it should be a number and is not missing
                if filter["number"] is True and value is not "":

                    # try to interpret it as a number
                    try:
                        value = int(value)
                    except ValueError:
                        sys.exit("Error: Value in column appears to be not a number, which it should be.")

                # change order of filter values for IN operator
                if filter["operator"] == operator.contains:
                    value1 = filter["value"]
                    value2 = value
                else:
                    value1 = value
                    value2 = filter["value"]

                # filter the value
                if (value is "" and filter["number"] is False or value is not "") and not filter["operator"](value1, value2):
                    filter_row = True

            # should the row be filtered, then go to next row
            if filter_row == True:
                continue

        # write the line to the end file
        combined.write(line)

    # close file
    f.close()

    # print info
    print("\rFiles combined: " + str(counter), end="")

# close file
combined.close()

# write the final number of rows written
print("\rFiles combined: " + str(counter))

# print duration of script execution
print("Finished in " + str(round(time.time() - timer, 2)) + " seconds\n")
print("\a")
