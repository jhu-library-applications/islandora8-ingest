import requests
import pandas as pd
from datetime import datetime

# Your baseURL: https://islandoralink.edu+//jsonapi/node/islandora_object'
baseURL = 'https://digital.library.jhu.edu//jsonapi/node/islandora_object'
# Filter by collection node.
search_filter = '?filter[field_member_of.id][value]=8b877ddf-ba4b-4d90-a482-0bc613a4a6d8'
# Function grabs name from islandora_object.

tax_field_list = ['field_access_rights', 'field_access_terms', 'field_access_rights',
                  'field_copyright_and_use', 'field_copyright_holder', 'field_digital_publisher', 'field_genre',
                  'field_language', 'field_model', 'field_publisher',
                  'field_publisher_country', 'field_resource_type', 'field_spatial_coverage',
                  'field_subject', 'field_title_language']

relator_field_list = ['field_contributor', 'field_creator']

string_field_list = ['field_abstract', 'field_alternative_title', 'field_custodial_history',
                     'field_description', 'field_table_of_contents']

joined_fields = tax_field_list+relator_field_list

joined_fields = ','.join(joined_fields)

include = '&include='+joined_fields

key_list = ['uri']

skip_fields = ['drupal_internal__nid', 'drupal_internal__vid', 'langcode',
               'promote', 'sticky', 'default_langcode', 'revision_translation_affected',
               'content_translation_source', 'content_translation_outdated', 'node_type',
               'revision_uid', 'uid', 'status', 'revision_timestamp']

find_replace = {}


def fetch_data(json_data):
    for count, item in enumerate(json_data):
        relationships = item.get('relationships')
        attributes = item.get('attributes')
        url = attributes['field_citable_url']['uri']
        item_dict = {'url': url}
        for key, value in attributes.items():
            if key not in skip_fields:
                if value:
                    if isinstance(value, str) or isinstance(value, bool):
                        item_dict[key] = value
                    elif isinstance(value, list):
                        new_list = []
                        for part_value in value:
                            if isinstance(part_value, dict):
                                part_value = part_value.get('uri')
                            else:
                                part_value = part_value
                            new_list.append(part_value)
                        new_list = "||".join(new_list)
                        item_dict[key] = new_list
                    else:
                        pass
        for key, value in relationships.items():
            if key in tax_field_list:
                data_to_grab = value['data']
                new_list = []
                if data_to_grab:
                    if isinstance(data_to_grab, list):
                        for item_part in data_to_grab:
                            unique_id = item_part['id']
                            new_list.append(unique_id)
                    else:
                        unique_id = data_to_grab['id']
                        new_list.append(unique_id)
                    new_list = "||".join(new_list)
                    item_dict[key] = new_list
            elif key in string_field_list:
                data_to_grab = value['data']
                new_list = []
                if data_to_grab:
                    for item_part in data_to_grab:
                        string_value = item_part['meta']['value']
                        new_list.append(string_value)
                    new_list = "||".join(new_list)
                    item_dict[key] = new_list
            elif key in relator_field_list:
                data_to_grab = value['data']
                new_list = []
                if data_to_grab:
                    for item_part in data_to_grab:
                        unique_id = item_part['id']
                        relator = item_part['meta']['rel_type']
                        new_value = relator+':'+unique_id
                        new_list.append(new_value)
                    new_list = "||".join(new_list)
                    item_dict[key] = new_list
            else:
                pass

        all_items.append(item_dict)


# Loop through islandora_objects and grab all items, chuck into DataFrame.
all_items = []
more_links = True
nextList = []
total = 0
while more_links:
    if not nextList:
        link = baseURL+search_filter+include+'&'+'page[limit=50]'
        print(link)
        r = requests.get(link).json()
    else:
        next_link = nextList[0]
        r = requests.get(next_link).json()
    data = r.get('data')
    total = total + (len(data))
    print(total)
    included = r.get('included')
    for include in included:
        name = include['attributes']['name']
        unique_id = include['id']
        find_replace[unique_id] = name
    fetch_data(data)
    nextList.clear()
    links = r.get('links')
    nextDict = links.get('next')
    if nextDict:
        next_link = nextDict.get('href')
        nextList.append(next_link)
    else:
        break
print('')

all_items = pd.DataFrame.from_dict(all_items)

for key, value in find_replace.items():
    for field in tax_field_list:
        try:
            all_items[field] = all_items[field].str.replace(key, value, regex=False)
        except KeyError:
            pass
    for field in relator_field_list:
        try:
            all_items[field] = all_items[field].str.replace(key, value, regex=False)
        except KeyError:
            pass

# Create CSV for new DataFrame.
dt = datetime.now().strftime('%Y-%m-%d%H.%M.%S')
all_items.to_csv('existingRepositoryItems_'+dt+'.csv', index=False)