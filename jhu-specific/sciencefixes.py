import pandas as pd
import argparse
from datetime import datetime

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--file')

args = parser.parse_args()

if args.file:
    filename = args.file
else:
    filename = input('Enter metadata filename (including \'.csv\'): ')

prefixColumns = {'Interviewer': 'relators:ivr;', 'Interviewee': 'relators:ive;'}
textColumns = ['abstract']

# Split any string columns to list.
df_1 = pd.read_csv(filename, header=0)
all_items = []
for count, row in df_1.iterrows():
    row = row
    for column in prefixColumns:
        columnValue = row[column]
        if pd.notnull(columnValue):
            newValueList = []
            valueList = str(columnValue).split('|')
            for item in valueList:
                prefix = prefixColumns.get(column)
                item = prefix+item
                newValueList.append(item)
            row[column] = newValueList
    for column in textColumns:
        value = row[column]
        if pd.notnull(value):
            value = value+';eng'
            row[column] = value
    all_items.append(row)
df_1 = pd.DataFrame.from_dict(all_items)

all_contributors = []
for count, row in df_1.iterrows():
    contributors = []
    for column in prefixColumns:
        columnValue = row[column]
        if isinstance(columnValue, list):
            for value in columnValue:
                contributors.append(value)
    all_contributors.append(contributors)

df_1['contributors'] = all_contributors
df_1.contributors = df_1.contributors.str.join('|')

# Create CSV for new DataFrame.
dt = datetime.now().strftime('%Y-%m-%d %H.%M.%S')
df_1.to_csv('updated_'+dt+'.csv')
