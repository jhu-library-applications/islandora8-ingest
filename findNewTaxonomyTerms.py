import pandas as pd
import argparse
from datetime import datetime

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--file')
parser.add_argument('-f2', '--file2')
args = parser.parse_args()

if args.file:
    filename = args.file
else:
    filename = input('Enter metadata filename (including \'.csv\'): ')
if args.file:
    filename2 = args.file2
else:
    filename2 = input('Enter metadata filename (including \'.csv\'): ')

collection_tax = pd.read_csv(filename, header=0)
existing_tax = pd.read_csv(filename2, header=0)

collection_tax['name'] = collection_tax['name'].astype(str)
collection_tax['name'] = collection_tax['name'].str.strip()
existing_tax['name'] = existing_tax['name'].astype(str)
existing_tax['name'] = existing_tax['name'].str.strip()

existing_tax['existing'] = True

frame = pd.merge(collection_tax, existing_tax, how='left', on=['name'], suffixes=('_1', '_2'))

frame = frame.reindex(sorted(frame.columns), axis=1)
frame.drop_duplicates(inplace=True)
print(frame.columns)
print(frame.head)
dt = datetime.now().strftime('%Y-%m-%d')
frame.to_csv('existingTaxonomiesResults'+'_'+dt+'.csv', index=False)