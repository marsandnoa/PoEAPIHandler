from flask import Flask, request
import requests

app = Flask(__name__)



@app.route('/callback', methods=['GET'])
def callback():
    # Handle the authorization code received from the OAuth provider
    authorization_code = request.args.get('code')

    # Make a POST request to the token endpoint to exchange the authorization code for an access token
client_id = 'slisealtradescraper'
client_secret = 'zFq9C5h0RNMA'
grant_type = 'client_credentials'
scope = 'service:psapi'

# Request payload
payload = {
    'client_id': client_id,
    'client_secret': client_secret,
    'grant_type': grant_type,
    'scope': scope
}

client_id = 'slisealtradescraper'
version = '1.0.0'
contact = 'marsandnoa@gmail.com'

headers = {
    'User-Agent': f'OAuth {client_id}/{version} (contact: {contact}) StrictMode'
}

response = requests.post('https://www.pathofexile.com/oauth/token', data=payload,headers=headers)

# Access the response headers
headers = response.headers

# Print the response headers
print(response.status_code)
for header, value in headers.items():
    print(header + ": " + value)

if response.status_code == 200:
    # Access token obtained successfully
    response_data = response.json()
    access_token = response_data['access_token']
    expires_in = response_data['expires_in']
    token_type = response_data['token_type']
    username = response_data['username']
    sub = response_data['sub']
    scope = response_data['scope']

    # Handle the obtained access token as needed
    # Store it securely, use it to make authenticated API requests, etc.
    print(f'Access Token: {access_token}')
else:
    # Handle token request failure
    print('Token request failed')

headers = {
    'Authorization': f'Bearer {access_token}',
    'User-Agent': f'OAuth {client_id}/{version} (contact: {contact}) StrictMode'
}

base_url = 'https://api.pathofexile.com'
endpoint = '/public-stash-tabs'

# Construct the URL
url = f"{base_url}{endpoint}"

# Send the GET request
response = requests.get(url, headers=headers)

# Check the response status code
if response.status_code == 200:
    # Request successful, handle the response data
    data = response.json()
    # Process the data as needed
else:
    # Request failed, handle the error
    print(f"Request failed with status code: {response.status_code}")

print(data)