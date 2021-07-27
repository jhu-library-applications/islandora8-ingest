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

textColumns = ['abstract', 'description']
genreColumns = ['dc.format.medium', 'genre']

# Split any string columns to list.
df_1 = pd.read_csv(filename, header=0)
all_items = []
for count, row in df_1.iterrows():
    row = row
    genreList = []
    row['access_rights'] = 'Public Digital Access'
    row['copyright'] = 'Not Evaluated'
    row['featured_item'] = '0'
    row['title_language'] = 'English'
    row['model'] = 'Image'
    for column in textColumns:
        value = row[column]
        if pd.notnull(value):
            value = value.strip()
            match1 = re.search(r'\w$', value)
            match2 = re.search(r'\.\s[a-z]', value)
            if match1:
                newValue = value+"."
                row[column] = newValue
            if match2:
                print(value)
                row['check'] = 'yes'
    for column in genreColumns:
        value = row[column]
        if pd.notnull(value):
            value = value.strip()
            values = value.split('|')
            for lvalue in values:
                if lvalue not in genreList:
                    genreList.append(lvalue)
    if genreList:
        print(genreList)
        row['newGenre'] = "|".join(genreList)
    all_items.append(row)
df_1 = pd.DataFrame.from_dict(all_items)


# Create CSV for new DataFrame.
dt = datetime.now().strftime('%Y-%m-%d %H.%M.%S')
df_1.to_csv('updated_'+dt+'.csv')
