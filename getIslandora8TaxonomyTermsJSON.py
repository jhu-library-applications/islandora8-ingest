import requests
import json

# Your baseURL: https://islandoralink.edu+//jsonapi/taxonomy_term/
baseURL = 'https://digital.library.jhu.edu//jsonapi/taxonomy_term/'

# Machine names of taxonomies for your islandora 8 instance.
taxonomies = ['corporate_body', 'family', 'genre', 'geo_location', 'islandora_access',
              'language', 'person', 'subject', 'access_rights', 'copyright_and_use',
              'islandora_display', 'islandora_media_use', 'islandora_models', 'resource_types']


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
        for term in data:
            unique_id = term['id']
            new_file = taxonomy+'_'+unique_id+'.json'
            with open(new_file, 'w') as f:
                json.dump(term, f)
        nextList.clear()
        links = r.get('links')
        nextDict = links.get('next')
        if nextDict:
            next_links = nextDict.get('href')
            nextList.append(next_links)
        else:
            break
    print('')