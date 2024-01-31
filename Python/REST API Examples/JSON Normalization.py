import requests
import pandas as pd

url = "https://api.github.com/repositories"

payload = requests.request("GET", url, headers=headers).json()

payload_df = pd.json_normalize(payload)

payload_df