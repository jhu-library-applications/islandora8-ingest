import requests
import secret
import pandas as pd
import argparse
import json

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--file')
args = parser.parse_args()

if args.file:
    filename = args.file
else:
    filename = input('Enter metadata filename (including \'.csv\'): ')

df = pd.read_csv(filename)
all_links = df.repo_item.tolist()
print(len(all_links))

# Your baseURL: https://islandoralink.edu+//jsonapi/node/islandora_object'
baseURL = 'https://digital.library.jhu.edu/'
objectURL = '/jsonapi/node/islandora_object'

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
all_items = []
for count, link in enumerate(all_links):
    media_link = link+'/media?_format=json'
    if count % 100 == 0:
        print(count)
    r = s.get(media_link).json()
    for media in r:
        uuid_value = media['uuid'][0]
        uuid = uuid_value['value']
        mime_type_value = media['field_mime_type'][0]
        mime_type = mime_type_value['value']
        mime_type = mime_type.replace('/', '_')
        new_file = mime_type+'_'+uuid+'.json'
        with open(new_file, 'w') as f:
            json.dump(media, f)