import requests

baseURL = 'https://test.digital.library.jhu.edu//jsonapi/taxonomy_term/'
taxonomies = ['access_rights', 'copyright_and_use', 'corporate_body',
              'family', 'genre', 'geo_location', 'islandora_access',
              'islandora_display', 'islandora_media_use', 'islandora_models',
              'language', 'person', 'resource_types', 'subject']

for taxonomy in taxonomies:
    print(taxonomy)
    r = requests.get(baseURL+taxonomy).json()
    data = r.get('data')
    print(len(data))
    for term in data:
        attributes = term.get('attributes')
        name = attributes.get('name')
        print(name)
    print('')
