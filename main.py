import requests
from bs4 import BeautifulSoup
from datetime import datetime

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
        title_element = title_element.get_text(strip=True)
        return(f"\nProduct {title_element}")
    else:
        return("Could not find title")
def check_price(price_element):
    if price_element:
        print(f"\nFound price element!")
        price_text = price_element.get_text(strip=True)
        print(f"Raw text: {price_text}")
    
        clean_price = price_text.replace('$', '').replace(',','')
   
        price = float(clean_price)
    
        return(f"\nCurrent price: ${price}")
    else:
        return("Could not find price element.")
current_time = datetime.now()
print(check_title(title_element), check_price(price_element))
print(f"Checked at {current_time}")