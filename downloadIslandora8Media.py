import shutil

import requests
import pandas as pd
import secret
from datetime import datetime

# Your baseURL: https://islandoralink.edu+//jsonapi/node/islandora_object'
baseURL = 'https://digital.library.jhu.edu/'
objectURL = '/jsonapi/node/islandora_object'
# Filter by collection node.
search_filter = '?filter[field_member_of.id][value]=d66cfc50-160c-4283-a148-bc10284727f7'
# Function grabs name from islandora_object.


username = secret.username
password = secret.password

# Authenticate to Drupal site, get token
s = requests.Session()
header = {'Content-entity_type': 'application/json'}
data = {'name': username, 'pass': password}
session = s.post(baseURL+'user/login?_format=json', headers=header,
                 json=data).json()
token = session['csrf_token']

s.headers.update({'Accept': 'application/vnd.api+json', 'Content-Type':
                  'application/vnd.api+json', 'X-CSRF-Token': token})
# Loop through islandora_objects and grab all items, chuck into DataFrame.
all_links = []
more_links = True
nextList = []
total = 0
while more_links:
    if not nextList:
        link = baseURL+objectURL+search_filter+'&page[limit=50]'
        print(link)
        r = requests.get(link).json()
    else:
        next_link = nextList[0]
        r = s.get(next_link).json()
    all_data = r.get('data')
    total = total + (len(all_data))
    print(total)
    for data in all_data:
        attributes = data['attributes']
        uri = attributes['field_citable_url']['uri']
        all_links.append(uri)
    nextList.clear()
    links = r.get('links')
    nextDict = links.get('next')
    if nextDict:
        next_link = nextDict.get('href')
        nextList.append(next_link)
    else:
        break
print('')

all_items = []
for link in all_links:
    media_link = link+'/media?_format=json'
    print(media_link)
    r = s.get(media_link).json()
    for file in r:
        little_dictionary = {}
        name = file['name'][0]['value']
        field_media_image = file.get('field_media_image')
        if field_media_image:
            field_media_image_link = field_media_image[0]['url']
        use = file['field_media_use'][0]['url']
        little_dictionary['name'] = name
        little_dictionary['uri'] = field_media_image_link
        file_response = s.get(field_media_image_link, stream=True)
        file_location = 'downloads/'+name
        if use == '/taxonomy/term/17':
            all_items.append(little_dictionary)
            with open(file_location, 'wb') as out_file:
                shutil.copyfileobj(file_response.raw, out_file)

print(little_dictionary)
# Create CSV for new DataFrame.
dt = datetime.now().strftime('%Y-%m-%d%H.%M.%S')
all_items = pd.DataFrame.from_dict(all_items)
all_items.to_csv('downloadedMedia_'+dt+'.csv', index=False)