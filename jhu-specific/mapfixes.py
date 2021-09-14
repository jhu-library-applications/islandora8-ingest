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
genreColumns = ['dc.format.medium', 'genre']


df_1 = pd.read_csv(filename, header=0)
child_items = []
parent_items = []
single_items = []
for count, row in df_1.iterrows():
    row = row
    jhir = row['jhir_uri']
    type = row['type']
    if type == 'child':
        child_items.append(row)
    elif type == 'parent':
        parent_items.append(row)
    else:
        single_items.append(row)

child_items = pd.DataFrame.from_dict(child_items)
parent_items = pd.DataFrame.from_dict(parent_items)
single_items = pd.DataFrame.from_dict(single_items)

# Create CSV for new DataFrame.
dt = datetime.now().strftime('%Y-%m-%d %H.%M.%S')
child_items.to_csv('childItems_'+dt+'.csv')
parent_items.to_csv('parentItems_'+dt+'.csv')
single_items.to_csv('single_item_'+dt+'.csv')
