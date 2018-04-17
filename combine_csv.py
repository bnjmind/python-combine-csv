# import modules
import time
import glob
import argparse
import os

# parse options given to script
parser = argparse.ArgumentParser()
parser.add_argument("-f", "--folder", help="The folder that contains the to be combined .csv files", metavar="", default="")
parser.add_argument("-o", "--output", help="The output file to be generated, defaults to 'combined_files.csv'", metavar="", default="combined_files.csv")
parser.add_argument("-i", "--id", help="ID's to filter the data on (comma separated)", metavar="", default="")
options = parser.parse_args()

# start timer
timer = time.time()

# output that we're doing something
print("\nPreparing everything... (The script can be aborted by pressing ctrl+c)")

# open a new file that we will fill
combined = open(options.output, "w")

# init counter
counter = 0

# list all files in directory
for i, name in enumerate(glob.glob(options.folder + "/*.csv")):

    # update counter
    counter += 1

    # open file
    f = open(name, "r")

    # skip first line if not first file
    if (i != 0):
        next(f)

    # loop through lines
    for j, line in enumerate(f):

        # check if id should be filtered
        if (options.id != "" and (i != 0 or j != 0)):

            if (line.split(",")[2] not in options.id.split(",")):

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
os.system('say "Bliep"')
