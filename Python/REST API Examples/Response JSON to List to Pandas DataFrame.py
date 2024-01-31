import requests
import pandas as pd

url = "https://api.github.com/users/arabinowe/repos"

payload={}
headers = {}

response = requests.request("GET", url, headers=headers, data=payload).json()

df = pd.DataFrame(response)
df.head()