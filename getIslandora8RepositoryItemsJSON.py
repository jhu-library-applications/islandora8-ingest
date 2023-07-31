import requests
import json
import os
import pandas as pd
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--file')
args = parser.parse_args()

if args.file:
    filename = args.file
else:
    filename = input('Enter metadata filename (including \'.csv\'): ')

directory = '/Users/michelle/Documents/GitHub/metadata-export/repository-items/json'

baseURL = 'https://digital.library.jhu.edu//jsonapi/node'
item = '/islandora_object/'

repo_items = pd.read_csv(filename)

for count, row in repo_items.iterrows():
    member_of = row['member_of']
    uuid = row['uuid']
    print(count, uuid)
    folder = os.path.join(directory, member_of)
    os.makedirs(folder, exist_ok=True)
    link = baseURL+item+uuid
    r = requests.get(link).json()
    data = r.get('data')
    unique_id = data['id']
    new_file = 'repositoryItem_'+unique_id+'.json'
    print(new_file)
    full_path = os.path.join(folder, new_file)
    with open(full_path, 'w') as f:
        json.dump(r, f)