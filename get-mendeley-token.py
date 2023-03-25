import requests

client_id = 'YOUR-CLIENT-ID'
client_secret = 'YOUR-CLIENT-SECRET'
authorization_code = 'YOUR-AUTHORIZATION-CODE'

data = {
    'grant_type': 'authorization_code',
    'client_id': client_id,
    'client_secret': client_secret,
    'code': authorization_code,
    'redirect_uri': 'http://localhost',
}

response = requests.post('https://api.mendeley.com/oauth/token', data=data)

if response.status_code == 200:
    access_token = response.json()['access_token']
    print('Access token:', access_token)
else:
    print('Error:', response.status_code, response.text)

