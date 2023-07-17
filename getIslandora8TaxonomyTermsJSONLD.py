import pandas as pd
import argparse
from rdflib import Graph

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--file')
args = parser.parse_args()

if args.file:
    filename = args.file
else:
    filename = input('Enter metadata filename (including \'.csv\'): ')

metadata = pd.read_csv(filename)

baseURL = 'https://digital.library.jhu.edu/taxonomy/term/'


for index, row in metadata.iterrows():
    mime_type = metadata['field_mime_type']
    mime_type = mime_type.replace('/', '_')
    tid = row['tid']
    tid = str(tid)
    unique_id = row.get('unique_id')
    print(unique_id)
    url = baseURL+tid+'?_format=jsonld'
    print(url)
    g = Graph()
    g.parse(url)
    v = g.serialize(format='json-ld')
    if pd.notnull(unique_id):
        new_file = mime_type+'_'+unique_id+'.jsonld'
    else:
        new_file = mime_type+'_'+tid+'.jsonld'
    with open(new_file, 'w') as f:
        f.write(v)
        f.close()
    print(index)