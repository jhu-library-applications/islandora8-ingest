import requests
import pandas as pd
from datetime import datetime
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--file')
args = parser.parse_args()

if args.file:
    filename = args.file
else:
    filename = input('Enter metadata filename (including \'.csv\'): ')


df = pd.read_csv(filename, header=0)
uuids = df.unique_id.tolist()

# Your baseURL: https://islandoralink.edu+//jsonapi/node/islandora_object'
baseURL = 'https://digital.library.jhu.edu//jsonapi/node/islandora_object'
search_filter = '?filter[field_member_of.id][value]='
skip_fields = ['drupal_internal__nid', 'drupal_internal__vid', 'langcode',
               'promote', 'sticky', 'default_langcode', 'revision_translation_affected',
               'content_translation_source', 'content_translation_outdated', 'node_type',
               'revision_uid', 'uid', 'status', 'revision_timestamp']
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
included_relationships = '&include='+joined_fields

key_list = ['uri']


find_replace = {}


def fetch_data(json_data):
    for item in json_data:
        relationships = item.get('relationships')
        attributes = item.get('attributes')
        url = attributes['field_citable_url']['uri']
        uuid = item['id']
        item_dict = {'url': url, 'uuid': uuid}
        for field, field_value in attributes.items():
            if field not in skip_fields:
                if field_value:
                    if isinstance(field_value, str) or isinstance(field_value, bool):
                        item_dict[field] = field_value
                    elif isinstance(field_value, list):
                        new_list = []
                        for part_field_value in field_value:
                            if isinstance(part_field_value, dict):
                                part_field_value = part_field_value.get('uri')
                            else:
                                part_field_value = part_field_value
                            new_list.append(part_field_value)
                        new_list = "||".join(new_list)
                        item_dict[field] = new_list
                    else:
                        pass
        for rel_field, rel_value in relationships.items():
            if rel_field in tax_field_list:
                data_to_grab = rel_value['data']
                new_list = []
                if data_to_grab:
                    if isinstance(data_to_grab, list):
                        for item_part in data_to_grab:
                            drupal_uuid = item_part['id']
                            new_list.append(drupal_uuid)
                    else:
                        drupal_uuid = data_to_grab['id']
                        new_list.append(drupal_uuid)
                    new_list = "||".join(new_list)
                    item_dict[rel_field] = new_list
            elif rel_field in string_field_list:
                data_to_grab = rel_value['data']
                new_list = []
                if data_to_grab:
                    for item_part in data_to_grab:
                        string_value = item_part['meta']['value']
                        new_list.append(string_value)
                    new_list = "||".join(new_list)
                    item_dict[rel_field] = new_list
            elif rel_field in relator_field_list:
                data_to_grab = rel_value['data']
                new_list = []
                if data_to_grab:
                    for item_part in data_to_grab:
                        drupal_uuid = item_part['id']
                        relator = item_part['meta']['rel_type']
                        new_value = relator+':'+drupal_uuid
                        new_list.append(new_value)
                    new_list = "||".join(new_list)
                    item_dict[rel_field] = new_list
            else:
                pass

        all_items.append(item_dict)


# Loop through islandora_objects and grab all items, chuck into DataFrame.
def find_items_by_uuid(uuid_list, total_uuids):
    for count, uuid in enumerate(uuid_list):
        print('Retrieving items for {}. {} out of {}'.format(uuid, count+1, total_uuids))
        more_links = True
        next_list = []
        total = 0
        while more_links:
            if not next_list:
                link = baseURL+search_filter+uuid+included_relationships+'&page[limit=50]'
                r = requests.get(link).json()
            else:
                next_link = next_list[0]
                r = requests.get(next_link).json()
            data = r.get('data')
            total = total + (len(data))
            print(total)
            included = r.get('included')
            if included:
                for include in included:
                    name = include['attributes']['name']
                    unique_id = include['id']
                    find_replace[unique_id] = name
            fetch_data(data)
            next_list.clear()
            links = r.get('links')
            next_dict = links.get('next')
            if next_dict:
                next_link = next_dict.get('href')
                next_list.append(next_link)
            else:
                break
        print('')


all_items = []
first_uuids = len(uuids)
find_items_by_uuid(uuids, first_uuids)
paged_content_uuids = []
for item in all_items:
    model = item['field_model']
    pc_uuid = item['uuid']
    if model == 'a2b7d7d5-7b68-4bbf-98d2-c684205bc89b':
        paged_content_uuids.append(pc_uuid)
second_uuids = len(paged_content_uuids)
if paged_content_uuids:
    find_items_by_uuid(paged_content_uuids, second_uuids)
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