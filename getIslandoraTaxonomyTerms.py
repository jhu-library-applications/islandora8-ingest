import requests
import pandas as pd
from datetime import datetime

baseURL = 'https://test.digital.library.jhu.edu//jsonapi/taxonomy_term/'
# taxonomies = ['access_rights', 'copyright_and_use', 'corporate_body',
#               'family', 'genre', 'geo_location', 'islandora_access',
#               'islandora_display', 'islandora_media_use', 'islandora_models',
#               'language', 'person', 'resource_types', 'subject']
taxonomies = ['person', 'subject']
allTax = []
for taxonomy in taxonomies:
    print(taxonomy)
    r = requests.get(baseURL+taxonomy+'?page[limit=50]').json()
    data = r.get('data')
    print(data)
    print(len(data))
    for count, term in enumerate(data):
        print(count)
        if count == 0:
            print(term)
        attributes = term.get('attributes')
        name = attributes.get('name')
        uri = attributes.get('field_authority_link')
        taxDict = {'taxonomy': taxonomy, 'name': name, 'uri': uri}
        allTax.append(taxDict)
    print('')

existingTax = pd.DataFrame.from_dict(allTax)
print(existingTax.head)

# Create CSV for new DataFrame.
dt = datetime.now().strftime('%Y-%m-%d%H.%M.%S')
existingTax.to_csv('existingTaxonomies_'+dt+'.csv')
