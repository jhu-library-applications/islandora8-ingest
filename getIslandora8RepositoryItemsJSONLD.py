import os
import pandas as pd
import argparse
from rdflib import Graph
import http.client
http.client._MAXHEADERS = 1000


parser = argparse.ArgumentParser()
parser.add_argument('-f', '--file')
args = parser.parse_args()

if args.file:
    filename = args.file
else:
    filename = input('Enter metadata filename (including \'.csv\'): ')

repo_items = pd.read_csv(filename)

directory = '/Users/michelle/Documents/GitHub/metadata-export/repository-items/jsonld'

for count, row in repo_items.iterrows():
    member_of = row['member_of']
    uri = row['uri']
    uuid = row['uuid']
    print(count, uri)
    folder = os.path.join(directory, member_of)
    os.makedirs(folder, exist_ok=True)
    url = uri+'?_format=jsonld'
    g = Graph()
    g.parse(url)
    v = g.serialize(format='json-ld')
    new_file = uuid+'.jsonld'
    full_file = os.path.join(folder, new_file)
    with open(full_file, 'w') as f:
        f.write(v)
        f.close()