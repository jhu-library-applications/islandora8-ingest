import requests
import pandas as pd
from datetime import datetime

# Your baseURL: https://islandoralink.edu+//jsonapi/taxonomy_term/
baseURL = 'https://digital.library.jhu.edu//jsonapi/taxonomy_term/'

# Machine names of taxonomies for your islandora 8 instance.
taxonomies = ['corporate_body', 'family', 'genre', 'geo_location', 'islandora_access',
              'language', 'person', 'subject', 'access_rights', 'copyright_and_use',
              'islandora_display', 'islandora_media_use', 'islandora_models', 'resource_types']


# Function grabs name and uris from taxonomy terms.
def fetch_data(data):
    for count, term in enumerate(data):
        tax_dict = {}
        skip = ['field_authority_link', 'description']
        tax_dict['taxonomy'] = term.get('type')
        attributes = term.get('attributes')
        for k, v in attributes.items():
            if k not in skip:
                k = k.replace('field_', '')
                if isinstance(v, list):
                    if v:
                        v = '||'.join(v)
                        tax_dict[k] = v
                    else:
                        tax_dict[k] = None
                else:
                    tax_dict[k] = v
        description = attributes.get('description')
        if description:
            description_value = description.get('value')
            tax_dict['description'] = description_value
        authorities = attributes.get('field_authority_link')
        if authorities:
            all_authorities = []
            for authority in authorities:
                uri = authority.get('uri')
                source = authority.get('source')
                if uri is not None:
                    tax_dict[source] = uri
                    authority_string = uri+';'+source
                    all_authorities.append(authority_string)
            all_authorities = '||'.join(all_authorities)
            tax_dict['authority'] = all_authorities
        allTax.append(tax_dict)


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
            next_links = nextList[0]
            r = requests.get(next_links).json()
        data = r.get('data')
        print(len(data))
        fetch_data(data)
        nextList.clear()
        links = r.get('links')
        nextDict = links.get('next')
        if nextDict:
            next_links = nextDict.get('href')
            nextList.append(next_links)
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