import requests
import pandas as pd

url = "https://api.github.com/users/arabinowe/repos"

payload={}
headers = {}

response = requests.request("GET", url, headers=headers, data=payload).json()

df = pd.DataFrame(response)
df.head()

df.to_csv('C:\\Users\\arbin\\OneDrive\\Documents\\GitHub\\For-Recruiters\\Python Scripts\\REST API Examples\\Aaron\'s Public Repo.csv')
