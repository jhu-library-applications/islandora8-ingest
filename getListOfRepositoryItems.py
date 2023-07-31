import requests
import pandas as pd

baseURL = 'https://digital.library.jhu.edu//jsonapi/node'
item = '/islandora_object'
collection = '/collection_object'
search_filter = '?filter[field_member_of.id][value]='


def get_data(json_data, member_of):
    if json_data:
        for term in json_data:
            term_dict = {}
            unique_id = term['id']
            attributes = term['attributes']
            item_title = attributes['title']
            uri = attributes['field_citable_url']['uri']
            term_dict['member_of'] = member_of
            term_dict['uri'] = uri
            term_dict['title'] = item_title
            term_dict['uuid'] = unique_id
            field_model_dictionary = term['relationships']['field_model']
            field_model = field_model_dictionary['data']['id']
            if field_model == 'a2b7d7d5-7b68-4bbf-98d2-c684205bc89b':
                search_again[unique_id] = item_title
            all_items.append(term_dict)


def search_api(dictionary_to_search):
    for item_uuid, name in dictionary_to_search.items():
        print(uuid, name)
        more_links = True
        next_list = []
        while more_links:
            if not next_list:
                item_link = baseURL+item+search_filter+item_uuid+'&page[limit=50]'
                item_response = requests.get(item_link).json()
            else:
                next_links = next_list[0]
                item_response = requests.get(next_links).json()
            data = item_response.get('data')
            print(len(data))
            get_data(data, name)
            next_list.clear()
            links = item_response.get('links')
            next_dict = links.get('next')
            if next_dict:
                next_links = next_dict.get('href')
                next_list.append(next_links)
            else:
                break
        print('')


item_dict = {}
link = baseURL+collection
r = requests.get(link).json()
data = r.get('data')
for collection in data:
    uuid = collection['id']
    title = collection['attributes']['title']
    item_dict[uuid] = title

search_again = {}
all_items = []
search_api(item_dict)
search_api(search_again)


all_items = pd.DataFrame.from_dict(all_items)
all_items.to_csv('listOfAllRepositoryItems_.csv', index=False)