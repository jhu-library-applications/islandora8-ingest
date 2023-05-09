import pandas as pd
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--file')

args = parser.parse_args()

if args.file:
    filename = args.file
else:
    filename = input('Enter metadata filename (including \'.csv\'): ')


# taxonomyColumns = ['contributor', 'printer', 'creator', 'digital_publisher', 'publisher', 'subject',
#                   'spatial_coverage', 'title_language', 'language', 'genre', 'geographer',
#                   'illustrator', 'editor', 'surveyor', 'cartographer', 'engraver']

taxonomyColumns = ['Broker', 'Captains', 'Ship Owners/Investors']

df = pd.read_csv(filename, header=0)

uniqueTerms = {}
for column in taxonomyColumns:
    for count, row in df.iterrows():
        termList = row.get(column)
        if termList is not None:
            if pd.notnull(termList):
                termList = termList.split('|')
                for term in termList:
                    keysList = list(uniqueTerms.keys())
                    term = term.strip()
                    if term not in keysList:
                        uniqueTerms[term] = column
                    else:
                        pass
print(uniqueTerms)
df_terms = pd.DataFrame.from_dict(uniqueTerms, orient='index')
df_terms.to_csv('uniqueTaxonomyTermsFromMetadataSheet.csv')