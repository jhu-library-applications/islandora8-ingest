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

coll = {'oralHistory': 5, 'scienceReview': 4, 'graphicPictorial': 3, 'newsLetters': 2, 'mapsAtlases': 1}
collReverse = {5: 'oralHistory', 4: 'scienceReview', 3: 'graphicPictorial', 2: 'newsLetters', 1: 'mapsAtlases'}

df = pd.read_csv(filename)
df['duplicates'] = df.duplicated(['authority'], keep=False)
print(df.columns)

new_list = []
for index, row in df.iterrows():
    duplicates = row['duplicates']
    name = row['authority']
    if duplicates is True:
        if name not in new_list:
            new_list.append(name)
print(new_list)
duplicate_list = []
for x in new_list:
    littleDict = {'authority': x}
    duplicate_list.append(littleDict)

for i, row in df.iterrows():
    name = row.get('authority')
    sheet = row.get('sheet')
    unique_id = row.get('unique_id')
    for entry in duplicate_list:
        if entry.get('authority') == name:
            entry[sheet] = unique_id

all_items = []
for entry in duplicate_list:
    print(entry)
    to_keep = {}
    to_delete = []
    del entry['authority']
    for key, value in entry.items():
        print(key, value)
        sheet = key
        unique_id = value
        ranking = coll.get(sheet)
        other_ranking = to_keep.get('ranking')
        other_id = to_keep.get('unique_id')
        if other_ranking is None:
            to_keep = {'ranking': ranking, 'unique_id': unique_id}
        elif ranking > other_ranking:
            to_keep['ranking'] = ranking
            to_keep['unique_id'] = unique_id
            to_delete.append({'ranking': other_ranking, 'unique_id': other_id})
        else:
            to_delete.append({'ranking': ranking, 'unique_id': unique_id})
        print('to_delete '+str(to_delete))
        print('to_keep '+str(to_keep))
        print('')
    for x in to_delete:
        to_keep_x = to_keep.get('unique_id')
        to_delete_x = x.get('unique_id')
        sheet = x.get('ranking')
        sheet = collReverse.get(sheet)
        newPair = {'sheet': sheet, 'to_delete': to_delete_x, 'to_keep': to_keep_x}
        all_items.append(newPair)

to_deleteto_keep = pd.DataFrame.from_dict(all_items)
print(to_deleteto_keep.head)

# Create CSV for new DataFrame.
dt = datetime.now().strftime('%Y-%m-%d%H.%M.%S')
to_deleteto_keep.to_csv('to_deleteto_keep_'+dt+'.csv')
