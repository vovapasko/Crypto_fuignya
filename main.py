import requests

# api-endpoint
from UrlBuilder import *

# URL = "https://api.coinmarketcap.com/v2/ticker/?limit=20"
URL1 = get_url_all_currency()
URL2 = get_url_ticker(15, 2, "rank")
URL3 = get_url_specific_currency(2)

# sending get request and saving the response as response object
r1 = requests.get(url=URL1)
r2 = requests.get(url=URL2)
r3 = requests.get(url=URL3)

# extracting data in json format
data1 = r1.json()
data2 = r2.json()
data3 = r3.json()

# print(data['data'])


# # printing the output
print("-----------------------------------------")

for element in data1['data']:
    print(element)
print(data1['metadata'])

print("-----------------------------------------")

for element in data2['data']:
    print(element + " :: ", end='')
    print(data2['data'][str(element)])
print(data2['metadata'])

print("-----------------------------------------")

for element in data3['data']:
    print(element + " :: ", end='')
    print(data3['data'][str(element)])
print(data2['metadata'])
