import pandas as pd
import argparse
from datetime import datetime
from relatorColumns import relatorPrefixes

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--file')
parser.add_argument('-r', '--addRelators')

args = parser.parse_args()

if args.file:
    filename = args.file
else:
    filename = input('Enter metadata filename (including \'.csv\'): ')
if args.addRelators:
    addRelators = args.addRelators
else:
    addRelators = input('Enter Yes or No: ')

df = pd.read_csv(filename, header=0)

all_contributors = []
for count, row in df.iterrows():
    contributors = []
    for key, value in relatorPrefixes.items():
        columnValue = row.get(key)
        if columnValue is not None:
            if pd.notnull(columnValue):
                columnValue = columnValue.split('|')
                if addRelators == 'Yes':
                    for x in columnValue:
                        x = value+x
                        print(x)
                        contributors.append(x)
                else:
                    for x in columnValue:
                        print(x)
                        contributors.append(x)
    print(contributors)
    all_contributors.append(contributors)

df['contributors'] = all_contributors
df.contributors = df.contributors.str.join('||')

# Create CSV for new DataFrame.
dt = datetime.now().strftime('%Y-%m-%d %H.%M.%S')
df.to_csv('relatorsCombined_'+dt+'.csv')