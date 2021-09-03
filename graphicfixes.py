import pandas as pd
import argparse
import re
from datetime import datetime

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--file')

args = parser.parse_args()

if args.file:
    filename = args.file
else:
    filename = input('Enter metadata filename (including \'.csv\'): ')

textColumns = ['abstract', 'description', 'alternative_title']
identifierColumns = ['digital_identifier', 'digital_identifier_1']
prefixColumns = {'photographer': 'relators:pht;', 'artist': 'relators:art;',
                 'architect': 'relators:arc;', 'landscape architect':
                 'relators:Isa;', 'cartoonist': 'relators:art;',
                 'lithographer': 'relators:ltg;', 'sculptor': 'relators:scl;',
                 'engraver': 'relators:egr;', 'lyricist': 'relators:lyr;'}

# Split any string columns to list.
df_1 = pd.read_csv(filename, header=0)
all_items = []
for count, row in df_1.iterrows():
    row = row
    idList = []
    for column in textColumns:
        value = row[column]
        if pd.notnull(value):
            value = value.strip()
            value = value.replace('  ', ' ')
            if value[-6:] != ';;eng':
                value = value+';;eng'
            print(value)
            row[column] = value
    for column in identifierColumns:
        value = row[column]
        if pd.notnull(value):
            value = value.strip()
            value = value.split('|')
            for x in value:
                idList.append(x)
    if idList:
        print(idList)
        row['allDigIds'] = "||".join(idList)
    all_items.append(row)

df_1 = pd.DataFrame.from_dict(all_items)

all_contributors = []
for count, row in df_1.iterrows():
    contributors = []
    for key, value in prefixColumns.items():
        columnValue = row[key]
        if pd.notnull(columnValue):
            print(columnValue)
            columnValue = columnValue.split('|')
            if isinstance(columnValue, list):
                for x in columnValue:
                    x = value+x
                    contributors.append(x)
            else:
                x = columnValue+x
                contributors.append(value)
    print(contributors)
    all_contributors.append(contributors)

df_1['contributors'] = all_contributors
df_1.contributors = df_1.contributors.str.join('||')

# Create CSV for new DataFrame.
dt = datetime.now().strftime('%Y-%m-%d %H.%M.%S')
df_1.to_csv('updated_'+dt+'.csv')
