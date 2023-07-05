from flask import Flask, request
import requests

app = Flask(__name__)

@app.route('/callback', methods=['GET'])
def callback():
    # Handle the authorization code received from the OAuth provider
    authorization_code = request.args.get('code')

    # Make a POST request to the token endpoint to exchange the authorization code for an access token
client_id = 'example'
client_secret = 'verysecret'
grant_type = 'client_credentials'
scope = 'service:psapi'

# Request payload
payload = {
    'client_id': client_id,
    'client_secret': client_secret,
    'grant_type': grant_type,
    'scope': scope
}

response = requests.post('https://www.pathofexile.com/oauth/token', data=payload)

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
