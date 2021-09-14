import requests
import pandas as pd
from datetime import datetime

# Your baseURL: https://islandoralink.edu+//jsonapi/taxonomy_term/
baseURL = 'https://test.digital.library.jhu.edu//jsonapi/taxonomy_term/'

# Machine names of taxonomies for your islandora 8 instance.
taxonomies = ['access_rights', 'copyright_and_use', 'corporate_body',
              'family', 'genre', 'geo_location', 'islandora_access',
              'islandora_display', 'islandora_media_use', 'islandora_models',
              'language', 'person', 'resource_types', 'subject']

# Function grabs name and uris from taonomy terms.
def fetchData(data):
    for count, term in enumerate(data):
        taxDict = {}
        attributes = term.get('attributes')
        name = attributes.get('name')
        taxDict['taxonomy'] = taxonomy
        taxDict['name'] = name
        authorities = attributes.get('field_authority_link')
        if authorities:
            for authority in authorities:
                uri = authority.get('uri')
                source = authority.get('source')
                if uri is not None:
                    taxDict[source] = uri
        allTax.append(taxDict)


# Loop through taxonomies and grab all taxonomy terms, chuck into DataFrame.
allTax = []
for taxonomy in taxonomies:
    print(taxonomy)
    more_links = True
    nextList = []
    while more_links:
        if not nextList:
            r = requests.get(baseURL+taxonomy+'?page[limit=50]').json()
        else:
            next = nextList[0]
            r = requests.get(next).json()
        data = r.get('data')
        print(len(data))
        fetchData(data)
        nextList.clear()
        links = r.get('links')
        nextDict = links.get('next')
        if nextDict:
            next = nextDict.get('href')
            nextList.append(next)
        else:
            break
    print('')

existingTax = pd.DataFrame.from_dict(allTax)
print(existingTax.head)

# Create CSV for DataFrame containing all taxonomy terms.
dt = datetime.now().strftime('%Y-%m-%d%H.%M.%S')
filename = 'allExistingTaxonomies_'+dt+'.csv'
existingTax.to_csv(filename, index=False)

# Creates CSV for each different taxonomy (subject, person, etc).
df = pd.read_csv(filename)
unique = df['taxonomy'].unique()
print(unique)
for value in unique:
    newDF = df.loc[df['taxonomy'] == value]
    newDF = newDF.dropna(axis=1, how='all')  # Deletes blank columns.
    newFile = value+'_'+dt+'.csv'
    newDF.to_csv(newFile, index=False)