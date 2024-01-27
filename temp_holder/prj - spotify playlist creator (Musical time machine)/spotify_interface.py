import requests
from urllib.parse import urlencode
import base64
import webbrowser


CLIENT_ID="af485c4ab2004acb8761e72d64d5cd5f"
CLIENT_SECRET="dfc2c963aa9a4ee3a4c7241d1dfcd5c8"




auth_headers = {
    "client_id": CLIENT_ID,
    "response_type": "code",
    "redirect_uri": "http://localhost:7777/callback",
    "scope": "user-library-read"
}

chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
webbrowser.open("https://accounts.spotify.com/authorize?" + urlencode(auth_headers),new=2)



code = "3Daf485c4ab2004acb8761e72d64d5cd5f"


encoded_credentials = base64.b64encode(CLIENT_ID.encode() + b':' + CLIENT_SECRET.encode()).decode("utf-8")

token_headers = {
    "Authorization": "Basic " + encoded_credentials,
    "Content-Type": "application/x-www-form-urlencoded"
}

token_data = {
    "grant_type": "authorization_code",
    "code": code,
    "redirect_uri": "http://localhost:7777/callback"
}

r = requests.post("https://accounts.spotify.com/api/token", data=token_data, headers=token_headers)


token = r.json()["access_token"]

print(token)