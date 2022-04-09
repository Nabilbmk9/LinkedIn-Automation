import requests
 
from connection_api import auth, headers
 
def user_info(headers):
    '''
    Get user information from Linkedin
    '''
    response = requests.get('https://api.linkedin.com/v2/me', headers = headers)
    user_info = response.json()
    return user_info
 
if __name__ == '__main__':
    credentials = r'C:\Users\boulm\Python_file\DJANGO\Publication_Linkedin\src\Publication_Linkedin\Linkedin_API\credentials.json'
    access_token = auth(credentials) # Authenticate the API
    headers = headers(access_token) # Make the headers to attach to the API call.
    user_information = user_info(headers) # Get user info
    print(user_information)