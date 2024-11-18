import requests
from requests.auth import HTTPBasicAuth

# Credentials
APP_ID = 'Ul69YTbEBV4VRwcBoajwrQ'
APP_SECRET = '2c7AHY2u1_sncFMJZbvAUARMrQ-a6w'
BASE_URL = 'https://www.reddit.com/'

# OAuth2 Token request
auth = HTTPBasicAuth(APP_ID, APP_SECRET)
data = {'grant_type': 'client_credentials'}
headers = {'User-Agent': 'travel-explorer by Immediate-Ship9951'}

r = requests.post(f'{BASE_URL}api/v1/access_token', data=data, headers=headers, auth=auth)
d = r.json()

if 'access_token' in d:
    access_token = d['access_token']
    print("Access token:", access_token)
else:
    print("Error:", d)
