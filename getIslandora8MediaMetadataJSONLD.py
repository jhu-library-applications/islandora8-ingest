import pandas as pd
import argparse
from rdflib import Graph
import os

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--file')
args = parser.parse_args()

if args.file:
    filename = args.file
else:
    filename = input('Enter metadata filename (including \'.csv\'): ')

metadata = pd.read_csv(filename)

directory = '/Users/michelle/Documents/GitHub/metadata-export/media/jsonld'
baseURL = 'https://digital.library.jhu.edu/media/'


for index, row in metadata.iterrows():
    mid = row['mid']
    mid = str(mid)
    unique_id = row.get('unique_id')
    print(index, unique_id)
    url = baseURL+mid+'?_format=jsonld'
    g = Graph()
    g.parse(url)
    v = g.serialize(format='json-ld')
    if pd.notnull(unique_id):
        new_file = 'media_'+unique_id+'.jsonld'
    else:
        new_file = 'media_'+mid+'.jsonld'
    full_file = os.path.join(directory, new_file)
    with open(full_file, 'w') as f:
        f.write(v)
        f.close()