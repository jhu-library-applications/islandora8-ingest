import pandas as pd
import argparse
import os
from datetime import datetime
import mapping2 as mt

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--file')
parser.add_argument('-d', '--directory')
parser.add_argument('-fl', '--flip')
args = parser.parse_args()

if args.file:
    filename = args.file
else:
    filename = input('Enter metadata filename (including \'.csv\'): ')
if args.directory:
    directory = args.directory
else:
    directory = input('Enter directory with taxonomies: ')
if args.flip:
    flip = args.flip
else:
    flip = input('Enter either "id2lab" or "lab2id": ')


def makeDataFrame(frame, filename):
    frame = pd.read_csv(filename)
    frames.append(frame)


# Split any string columns to list.
df_1 = pd.read_csv(filename, header=0)
all_items = []
for count, row in df_1.iterrows():
    row = row
    for column in mt.columnDict:
        columnValue = row[column]
        if pd.notnull(columnValue):
            row[column] = str(columnValue).split('|')
        else:
            row[column] = None
    all_items.append(row)
df_1 = pd.DataFrame.from_dict(all_items)
print(df_1.head)

# Create DataFrames from taxonomy spreadsheets.
frames = []
chart = {}
for count, file in enumerate(os.listdir(directory)):
    file = directory + "/" + file
    if file.endswith('.csv'):
        makeDataFrame("df_{}".format(count), file)
        chart[file] = count

# Get identifiers and labels from taxonomy DataFrames.
taxonomies = []
for frame in frames:
    for count, row in frame.iterrows():
        unique_id = row.get('unique_id')
        local_id = row.get('local_id')
        dict = {'unique_id': unique_id, 'local_id': local_id}
        taxonomies.append(dict)
taxonomies = pd.DataFrame.from_dict(taxonomies)
print(taxonomies.head)

# Find and replace using new_dict with labels and ids.
all_items = []
for index, row in df_1.iterrows():
    print(index)
    row = row
    for column in mt.columnDict:
        dataValue = row.get(column)
        if dataValue is not None:
            for i, listValue in enumerate(dataValue):
                for index, taxRow in taxonomies.iterrows():
                    unique_id = taxRow['unique_id']
                    local_id = taxRow['local_id']
                    if listValue == local_id:
                        dataValue[i] = unique_id
                        row[column] = dataValue
                        print(dataValue)
        if dataValue is not None:
            row[column] = '|'.join(dataValue)
    all_items.append(row)
new = pd.DataFrame.from_dict(all_items)
print(new.head)

# Create CSV for new DataFrame.
dt = datetime.now().strftime('%Y-%m-%d %H.%M.%S')
new.to_csv(flip+'_'+dt+'.csv')