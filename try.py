import pandas as pd
import argparse
import os
from datetime import datetime
import mappingTaxonomy as mt

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--file')
args = parser.parse_args()

if args.file:
    filename = args.file
else:
    filename = input('Enter metadata filename (including \'.csv\'): ')


# Split any string columns to list.
df_1 = pd.read_csv(filename, header=0)
all_items = []
for count, row in df_1.iterrows():
    row = row
    subject = row['Subject']
    if pd.notnull(subject):
        genreList = []
        subjectList = []
        subject = str(subject).split('|')
        subject = set(subject)
        for item in subject:
            if 'genre' in item:
                genreList.append(item)
            else:
                subjectList.append(item)
        row['Genre'] = "|".join(genreList)
        row['Subject'] = "|".join(subjectList)
    all_items.append(row)
df_1 = pd.DataFrame.from_dict(all_items)
print(df_1.head)


# Create CSV for new DataFrame.
dt = datetime.now().strftime('%Y-%m-%d %H.%M.%S')
df_1.to_csv('updated_'+dt+'.csv')
