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

textColumns = ['abstract', 'description']

# Split any string columns to list.
df_1 = pd.read_csv(filename, header=0)
all_items = []
for count, row in df_1.iterrows():
    row = row
    description = row['description']
    other_ids = row['other_ids']
    if pd.notnull(other_ids):
        if other_ids in description:
            description = description.replace(other_ids, '')
            row['new_description'] = description
    all_items.append(row)
df_1 = pd.DataFrame.from_dict(all_items)


# Create CSV for new DataFrame.
dt = datetime.now().strftime('%Y-%m-%d %H.%M.%S')
df_1.to_csv('updated_'+dt+'.csv')
