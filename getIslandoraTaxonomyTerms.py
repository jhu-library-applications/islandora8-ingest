import requests
import pandas as pd
from datetime import datetime

baseURL = 'https://test.digital.library.jhu.edu//jsonapi/taxonomy_term/'
# taxonomies = ['access_rights', 'copyright_and_use', 'corporate_body',
#               'family', 'genre', 'geo_location', 'islandora_access',
#               'islandora_display', 'islandora_media_use', 'islandora_models',
#               'language', 'person', 'resource_types', 'subject']
taxonomies = ['person', 'subject']


def fetchData(data):
    for count, term in enumerate(data):
        taxDict = {}
        attributes = term.get('attributes')
        name = attributes.get('name')
        taxDict['taxonomy'] = taxonomy
        taxDict['name'] = name
        authorities = attributes.get('field_authority_link')
        for authority in authorities:
            uri = authority.get('uri')
            source = authority.get('source')
            if uri is not None:
                taxDict[source] = uri
        allTax.append(taxDict)


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

# Create CSV for new DataFrame.
dt = datetime.now().strftime('%Y-%m-%d%H.%M.%S')
existingTax.to_csv('existingTaxonomies_'+dt+'.csv')
