import requests
import json
import os

directory = '/Users/michelle/Documents/GitHub/metadata-export/repository-items/json'

baseURL = 'https://digital.library.jhu.edu//jsonapi/node'
item = '/islandora_object'
collection = '/collection_object'
search_filter = '?filter[field_member_of.id][value]='
tax_field_list = ['field_access_rights', 'field_access_terms', 'field_access_rights',
                  'field_copyright_and_use', 'field_copyright_holder', 'field_digital_publisher', 'field_genre',
                  'field_language', 'field_model', 'field_publisher',
                  'field_publisher_country', 'field_resource_type', 'field_spatial_coverage',
                  'field_subject', 'field_title_language']
relator_field_list = ['field_contributor', 'field_creator']
joined_fields = tax_field_list+relator_field_list
joined_fields = ','.join(joined_fields)
included_relationships = '&include='+joined_fields

collections = {}
link = baseURL+collection
r = requests.get(link).json()
data = r.get('data')
for collection in data:
    unique_id = collection['id']
    title = collection['attributes']['title']
    collections[unique_id] = title
    new_file = 'collection_'+unique_id+'.json'
    with open(new_file, 'w') as f:
        json.dump(collection, f)

print(collections)

for uuid, name in collections.items():
    name = name.replace('Johns Hopkins University', '')
    name = name.lower()
    name = name.replace(' ', '_')
    name = name.replace('-', '_')
    folder = os.path.join(directory, name)
    os.makedirs(folder, exist_ok=True)
    print(uuid, name)
    more_links = True
    nextList = []
    while more_links:
        if not nextList:
            link = baseURL+item+search_filter+uuid+included_relationships+'&page[limit=50]'
            r = requests.get(link).json()
        else:
            next_links = nextList[0]
            r = requests.get(next_links).json()
        data = r.get('data')
        for term in data:
            unique_id = term['id']
            new_file = 'repositoryItem_'+unique_id+'.json'
            print(new_file)
            full_path = os.path.join(folder, new_file)
            with open(full_path, 'w') as f:
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