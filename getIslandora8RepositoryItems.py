import requests
import pandas as pd
from datetime import datetime

# Your baseURL: https://islandoralink.edu+//jsonapi/node/islandora_object'
baseURL = 'https://test.digital.library.jhu.edu//jsonapi/node/islandora_object'

# Function grabs name from islandora_object.
def fetchData(data):
    for count, item in enumerate(data):
        itemDict = {}
        attributes = item.get('attributes')
        for key, value in attributes.items():
            print(key, value)
        title = attributes.get('title')
        itemDict['title'] = title
        all_items.append(itemDict)


# Loop through islandora_objects and grab all items, chuck into DataFrame.
all_items = []
more_links = True
nextList = []
while more_links:
    if not nextList:
        r = requests.get(baseURL+'?page[limit=50]').json()
    else:
        next = nextList[0]
        r = requests.get(next).json()
    data = r.get('data')
    print(len(data))
    fetchData(data)
    nextList.clear()
    links = r.get('links')
    nextDict = links.get('next')
    if nextDict:
        next = nextDict.get('href')
        nextList.append(next)
    else:
        break
print('')

all_items = pd.DataFrame.from_dict(all_items)
print(all_items.head)

# Create CSV for new DataFrame.
dt = datetime.now().strftime('%Y-%m-%d%H.%M.%S')
all_items.to_csv('existingRepositoryItems_'+dt+'.csv')
