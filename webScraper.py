from flask import Flask, request
import requests
import time
app = Flask(__name__)



@app.route('/callback', methods=['GET'])
def callback():
    # Handle the authorization code received from the OAuth provider
    authorization_code = request.args.get('code')

while(True):
    client_id = 'slisealtradescraper'
    client_secret = ''
    grant_type = 'client_credentials'
    scope = 'service:psapi'
    version = '1.0.0'
    contact = 'marsandnoa@gmail.com'
    # Request payload

    payload = {
        'client_id': client_id,
        'client_secret': client_secret,
        'grant_type': grant_type,
        'scope': scope
    }

    headers = {
        'User-Agent': f'OAuth {client_id}/{version} (contact: {contact}) StrictMode'
    }

    response = requests.post('https://www.pathofexile.com/oauth/token', data=payload,headers=headers)

    if response.status_code == 200:
        # Access token obtained successfully
        response_data = response.json()
        access_token = response_data['access_token']
        expires_in = response_data['expires_in']
        token_type = response_data['token_type']
        username = response_data['username']
        sub = response_data['sub']
        scope = response_data['scope']
    else:
        print("error on access fetch")

    headers = {
        'Authorization': f'Bearer {access_token}',
        'User-Agent': f'OAuth {client_id}/{version} (contact: {contact}) StrictMode'
    }

    base_url = 'https://api.pathofexile.com'
    endpoint = '/public-stash-tabs'
    url = f"{base_url}{endpoint}"
    response = requests.get(url, headers=headers)


    #target item format, see API for list of item keys
    TargetItem={'name':"Chin Sol"}

    # Check the response status code
    if response.status_code == 200:
        data = response.json()
        next_change_id = data['next_change_id']  # Pagination code for the next request

        while next_change_id:
            stashes = data['stashes']
            for stash in stashes:
                stash_id = stash['id']
                public = stash['public']
                for item in stash['items']:
                    isidentical=True
                    for key in TargetItem.keys():
                        if(TargetItem[key]):
                            if TargetItem[key] != item[key]:
                                isidentical=False;
                    if(isidentical):
                        #need to implement stuff when target item found
                        print(item)

            next_url = f"{base_url}{endpoint}/{next_change_id}"
            next_response = requests.get(next_url, headers=headers)
            time.sleep(.5)
            if(next_response.status_code!=403):
                data = next_response.json()
                if(data['next_change_id']):
                    next_change_id = data['next_change_id']

    # End of the stream
        print("Reached the end of the stream.")
    else:
        print("error on item fetch")
    time.sleep(30)
