import os
from dotenv import load_dotenv
load_dotenv()

import urllib.request, json

json_url = urllib.request.urlopen("https://min-api.cryptocompare.com/data/price?fsym=ETH&tsyms=BTC,USD,EUR&api_key=os.getenv('cryptocompare_api_key')")

data = json.loads(json_url.read())

print (data)
