# Imports
import json
import requests

# Anilist API URL
AnilistURL = 'https://graphql.anilist.co'


query = '''
query ($id: Int) { 
    Media (id: $id, type: ANIME) {
        id
        coverImage { large }
    }
}
'''

varQuery = { 
    'id': 15125
}

response = requests.post(AnilistURL, json={'query': query, 'variables': varQuery})
X = json.loads(response.content)
Y = X["data"]["Media"]["coverImage"]["large"]
print(Y)