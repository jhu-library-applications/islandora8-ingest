import requests
import secret
import pandas as pd
import argparse
from datetime import datetime

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
        little_dictionary = {'media_link': media_link}
        for key, value_list in media.items():
            if isinstance(value_list, list):
                if value_list:
                    for value in value_list:
                        for subkey, sub_value in value.items():
                            new_key = key + '_' + subkey
                            existing_sub_value = little_dictionary.get(new_key)
                            if existing_sub_value is not None:
                                new_sub_value = str(existing_sub_value)+'|'+str(sub_value)
                                little_dictionary[new_key] = new_sub_value
                            else:
                                little_dictionary[new_key] = sub_value
                else:
                    pass
            else:
                print('hey!')
                print(key, value)
        all_items.append(little_dictionary)

media_records = pd.DataFrame.from_dict(all_items)
media_records.drop(columns=['revision_created_format', 'created_format', 'changed_format'], inplace=True)
media_records.dropna(axis=1, how='all', inplace=True)

print(media_records)

# Create CSV for new DataFrame.
dt = datetime.now().strftime('%Y-%m-%d%H.%M.%S')
media_records.to_csv('media_records'+dt+'.csv', index=False)