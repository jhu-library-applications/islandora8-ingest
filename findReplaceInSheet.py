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
if args.file2:
    filename2 = args.file2
else:
    filename2 = input('Enter metadata filename (including \'.csv\'): ')

metadata = pd.read_csv(filename)
find_replace = pd.read_csv(filename2)
columnsToSearch = ['genre', 'digital_publisher']

for index, row in find_replace.iterrows():
    to_delete = row['to_delete']
    to_keep = row['to_keep']
    for column in columnsToSearch:
        metadata[column] = metadata[column].str.replace(to_delete, to_keep, regex=False)

# Create CSV for new DataFrame.
filename = filename[:-4]
dt = datetime.now().strftime('%Y-%m-%d%H.%M.%S')
metadata.to_csv('wReplacements_'+filename+'_'+dt+'.csv')