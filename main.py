import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json
import os

url = "https://www.newegg.com/gigabyte-gv-n5090gaming-oc-32gd-geforce-rtx-5090-32gb-graphics-card-triple-fans/p/N82E16814932761"

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

print("Fetching Newegg product page...")
response = requests.get(url, headers=headers)

if response.status_code == 200:
    print("Webpage found")
else:
    print(f"Failed. Status code: {response.status_code}")
    exit()

soup = BeautifulSoup(response.content, 'html.parser')

price_element = soup.find('div', class_='price-current')
title_element = soup.find('h1', class_='product-title')
def check_title(title_element):
    if title_element:
        print(f"\nFound title element")
        title_text = title_element.get_text(strip=True)
        return title_text
    else:
        print("Could not find title")
        return None
    
    
def check_price(price_element):
    if price_element:
        print(f"\nFound price element!")
        price_text = price_element.get_text(strip=True)
        print(f"Raw text: {price_text}")
    
        clean_price = price_text.replace('$', '').replace(',','')
   
        price = float(clean_price)
    
        print(f"\nCurrent price: ${price}")
        return price
    else:
        print("Could not find price element.")
        return None
current_time = datetime.now()
print(check_title(title_element), check_price(price_element))
print(f"Checked at {current_time}")
title_text = check_title(title_element)
price = check_price(price_element)

price_data ={
    "product": title_text,
    "price": price,
    "timestamp": str(current_time),
    "url": url
}

file_name = "price_history.json"
if os.path.exists(file_name):
    with open(file_name, "r") as f:
        all_prices = json.load(f)
else:
    all_prices = []
    
all_prices.append(price_data)

with open(file_name, 'w') as f:
    json.dump(all_prices, f, indent=4)
    
print(f"\n Price Saved to {file_name}")
print(f"Total entries: {len(all_prices)}")