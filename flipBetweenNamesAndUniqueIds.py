import pandas as pd
import argparse
import os
from datetime import datetime
import mappingTaxonomiesAndRelators as mt

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--file')
parser.add_argument('-d', '--directory')
args = parser.parse_args()

if args.file:
    filename = args.file
else:
    filename = input('Enter metadata filename (including \'.csv\'): ')
if args.directory:
    directory = args.directory
else:
    directory = input('Enter directory with taxonomies: ')


def makeDataFrame(frame, filename):
    frame = pd.read_csv(filename)
    frames.append(frame)


def removeRelatorAndBundle(listValue):
    package = [listValue, None]
    for bundle in mt.bundles:
        if bundle in listValue:
            listValue = listValue.replace(bundle, '')
            package[0] = listValue
    for relator in mt.relators:
        listValue = package[0]
        if relator in listValue:
            listValue = listValue.replace(relator, '')
            package[0] = listValue
            package[1] = relator
        else:
            pass
    return package


def addRelatorAndBundle(component, package):
    print(package, bundle, key)
    if (package[1] is not None) and (bundle is not None) and (key == 'addPrefixes'):
        component = package[1]+bundle+component
    elif (bundle is not None) and (key == 'addPrefixes'):
        component = bundle+component
    else:
        component = ':::'+component
    return component


# Split any string columns to list.
df_1 = pd.read_csv(filename, header=0)
all_items = []
for count, row in df_1.iterrows():
    row = row
    for key, value in mt.columnDict.items():
        for column in value:
            columnValue = row[column]
            if pd.notnull(columnValue):
                row[column] = str(columnValue).split('||')
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
        id = row.get('unique_id')
        label = row.get('name')
        bundle = row.get('bundle')
        dict = {'id': id, 'label': label, 'bundle': bundle}
        taxonomies.append(dict)
taxonomies = pd.DataFrame.from_dict(taxonomies)
print(taxonomies.head)

# Find and replace using dict with labels and ids.
all_items = []
for index, row in df_1.iterrows():
    print(index)
    row = row
    for key, value in mt.columnDict.items():
        for column in value:
            dataValue = row.get(column)
            if dataValue is not None:
                for i, listValue in enumerate(dataValue):
                    print(listValue)
                    package = removeRelatorAndBundle(listValue)
                    listValue = package[0]
                    print(listValue)
                    for index, taxRow in taxonomies.iterrows():
                        id = taxRow['id']
                        label = taxRow['label']
                        bundle = taxRow['bundle']
                        # if listValue == id:
                        #     label = addRelatorAndBundle(label, package)
                        #     print(label)
                        #     dataValue[i] = label
                        #     row[column] = dataValue
                        if listValue == id or listValue == label:
                            id = addRelatorAndBundle(id, package)
                            dataValue[i] = id
                            print(dataValue[i])
                            row[column] = dataValue
            if dataValue is not None:
                row[column] = '||'.join(dataValue)
    all_items.append(row)
new = pd.DataFrame.from_dict(all_items)
print(new.head)

# Create CSV for new DataFrame.
dt = datetime.now().strftime('%Y-%m-%d %H.%M.%S')
new.to_csv('flip_'+dt+'.csv')
