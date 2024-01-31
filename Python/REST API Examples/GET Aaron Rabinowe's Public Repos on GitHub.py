import requests

url = "https://api.github.com/users/arabinowe/repos"

payload={}
headers = {}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)
