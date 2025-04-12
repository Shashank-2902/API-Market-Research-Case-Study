# generic_search.py

import requests
import shared_auth

def generic_search():
    # Authenticate
    token = shared_auth.get_access_token()
    api_url = 'https://api.nexar.com/graphql'

    # Define GraphQL query
    # keyword = "Arduino Uno"  # Replace with your search term in q below
    query = '''
     query partSearch {
          supSearch (
            q: "Arduino Uno", 
            limit: 1
          ){
            hits
            results {
              part {
                id
                name
                mpn        
                manufacturer {
                  id
                  name
                }
              }
            }
          }
        }
    '''
    
    # Set Headers Including Access Token
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    # Make the Request and Handle the Response
    response = requests.post(api_url, json={'query': query}, headers=headers)


    if response.status_code == 200:
        data = response.json()
        return data['data']['supSearch']['results']
        # print(data)
    else:
        raise Exception(f"GraphQL Error: {response.status_code}, {response.text}")
