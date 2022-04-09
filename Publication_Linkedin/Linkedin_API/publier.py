import requests

from connection_api import auth, headers

credentials = r'C:\Users\boulm\Python_file\DJANGO\Publication_Linkedin\src\Publication_Linkedin\Linkedin_API\credentials.json'
access_token = auth(credentials) # Authenticate the API
headers = headers(access_token) # Make the headers to attach to the API call.

def user_info(headers):
    '''
    Get user information from Linkedin
    '''
    response = requests.get('https://api.linkedin.com/v2/me', headers = headers)
    user_info = response.json()
    return user_info
 
# Get user id to make a UGC post
user_information = user_info(headers)
urn = user_information['id']
author = f'urn:li:person:{urn}'

api_url = 'https://api.linkedin.com/v2/ugcPosts'
message = "Test, message envoyé depuis l'api Linkedn"

post_data = {
    "author": author,
    "lifecycleState": "PUBLISHED",
    "specificContent": {
        "com.linkedin.ugc.ShareContent": {
            "shareCommentary": {
                "text": message
            },
            "shareMediaCategory": "NONE"
        }
    },
    "visibility": {
        "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
    }
}

if __name__ == '__main__':
    r = requests.post(api_url, headers=headers, json=post_data)
    r.json()

