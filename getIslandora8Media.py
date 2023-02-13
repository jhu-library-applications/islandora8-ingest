import requests
import pandas as pd
from datetime import datetime

# Your baseURL: https://islandoralink.edu+//jsonapi/media/
baseURL = 'https://digital.library.jhu.edu//jsonapi/media/'

# Machine names of media for your islandora 8 instance.
media_types = ['image', 'document']


# Function grabs name and uris from media terms.
def fetch_data(data):
    for count, term in enumerate(data):
        media_dict = {}
        attributes_skip = ['changed', 'drupal_internal__mid', 'drupal_internal__vid', 'langcode',
                           'revision_created', 'revision_log_message', 'revision_translation_affected', 'status',
                           'created', 'changed', 'default_langcode', 'content_translation_source',
                           'content_translation_outdated', 'content_translation_created']
        relations_skip = ['bundle', 'revision_user', 'uid', 'thumbnail']
        media_dict['media'] = term.get('type')
        attributes = term.get('attributes')
        for k, v in attributes.items():
            if k not in attributes_skip:
                k = k.replace('field_', '')
                if isinstance(v, list):
                    if v:
                        v = '||'.join(v)
                        media_dict[k] = v
                    else:
                        media_dict[k] = None
                else:
                    media_dict[k] = v
        relationships = term.get('relationships')
        for k, v in relationships.items():
            if k not in relations_skip:
                relation_data = v.get('data')
                k = k.replace('field', '')
                if relation_data:
                    if isinstance(relation_data, list):
                        all_relations = []
                        for relation in relation_data:
                            r_id = relation.get('id')
                            all_relations.append(r_id)
                        all_relations = '||'.join(all_relations)
                        media_dict[k] = all_relations
                    else:
                        media_dict['k'] = relation_data.get('id')
                    
        allMedia.append(media_dict)


# Loop through taxonomies and grab all media terms, chuck into DataFrame.
allMedia = []
for media in media_types:
    print(media)
    more_links = True
    nextList = []
    while more_links:
        if not nextList:
            r = requests.get(baseURL+media+'?page[limit=50]').json()
        else:
            next_links = nextList[0]
            r = requests.get(next_links).json()
        data = r.get('data')
        print(len(data))
        fetch_data(data)
        nextList.clear()
        links = r.get('links')
        nextDict = links.get('next')
        if nextDict:
            next_links = nextDict.get('href')
            nextList.append(next_links)
        else:
            break
    print('')

existingMedia = pd.DataFrame.from_dict(allMedia)
print(existingMedia.head)

# Create CSV for DataFrame containing all media terms.
dt = datetime.now().strftime('%Y-%m-%d%H.%M.%S')
filename = 'allExistingMedia_'+dt+'.csv'
existingMedia.to_csv(filename, index=False)

# Creates CSV for each different media (subject, person, etc).
df = pd.read_csv(filename)
unique = df['media'].unique()
print(unique)
for value in unique:
    newDF = df.loc[df['media'] == value]
    newDF = newDF.dropna(axis=1, how='all')  # Deletes blank columns.
    newFile = value+'_'+dt+'.csv'
    newDF.to_csv(newFile, index=False)