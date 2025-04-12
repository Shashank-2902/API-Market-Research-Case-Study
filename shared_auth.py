import requests

CLIENT_ID = 'ed11b3f1-7f7f-48d6-bcc5-91338efdf48a'
CLIENT_SECRET = 'ahTUd7hT1S8tVm4LYYrPJJ4_HMazJOJGmfHV'

def get_access_token():
    token_url = 'https://identity.nexar.com/connect/token'
    payload = {
        'grant_type': 'client_credentials',
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'scope': 'supply.domain'
    }
    response = requests.post(token_url, data=payload)
    if response.status_code == 200:
        return response.json().get('access_token')
    else:
        raise Exception(f"Failed to retrieve token: {response.status_code}, {response.text}")
