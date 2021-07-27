import pandas as pd
import argparse
import os
from datetime import datetime
import mappingTaxonomy as mt

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


def addprefix(flip, a, b):
    keyList = mt.prefixes.keys()
    if flip == 'id2lab':
        for key in keyList:
            print(key, b)
            if key in b:
                prefix = mt.prefixes.get(key)
                print(prefix)
                a = a.strip()
                print(a)
                a = prefix+a
                return(a)
    elif flip == 'lab2id':
        for key in keyList:
            if key in a:
                prefix = mt.prefixes.get(key)
                print(prefix)
                b = b.strip()
                print(b)
                b = prefix+b
                return(b)

# Split any string columns to list.
df_1 = pd.read_csv(filename, header=0)
all_items = []
for count, row in df_1.iterrows():
    row = row
    for column in mt.columnList:
        columnValue = row[column]
        if pd.notnull(columnValue):
            row[column] = str(columnValue).split('|')
    for column in mt.prefixColumns:
        columnValue = row[column]
        if pd.notnull(columnValue):
            row[column] = str(columnValue).split('|')
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
dict = {}
for frame in frames:
    for count, row in frame.iterrows():
        id = row['local_id']
        label = row['name']
        if flip == 'id2lab':
            dict[id] = label
        elif flip == 'lab2id':
            dict[label] = id
        else:
            print('error')

# Find and replace using dict with labels and ids.
all_items = []
for count, row in df_1.iterrows():
    row = row
    for column in mt.columnList:
        value = row[column]
        if isinstance(value, list):
            for i, x in enumerate(value):
                if dict.get(x):
                    value[i] = dict[x]
                    row[column] = value
            row[column] = '|'.join(value)
    for column in mt.prefixColumns:
        value = row[column]
        if value:
            if isinstance(value, list):
                for i, x in enumerate(value):
                    if dict.get(x):
                        dvalue = dict.get(x)
                        print(dvalue)
                        print(x)
                        new_value = addprefix(flip, dvalue, x)
                        print(new_value)
                        value[i] = new_value
                        row[column] = value
                row[column] = '|'.join(value)
    all_items.append(row)
new = pd.DataFrame.from_dict(all_items)
print(new.head)

# Create CSV for new DataFrame.
dt = datetime.now().strftime('%Y-%m-%d %H.%M.%S')
new.to_csv(flip+'_'+dt+'.csv')
