"""
PC Price Tracker
Tracks Pc part prices and History over time.
"""

import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json
import os

#Configuration
PRODUCT_URL = "https://www.newegg.com/gigabyte-gv-n5090gaming-oc-32gd-geforce-rtx-5090-32gb-graphics-card-triple-fans/p/N82E16814932761"
PRICE_HISTORY_FILE = "price_history.json"
HEADERS = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

#Functions
def fetch_page(url):
    """Fetch the product page"""
    print("Fetching product page...")
    response = requests.get(url, headers=HEADERS)

    if response.status_code == 200:
        print("Webpage found")
        return response
    else:
        print(f"Failed. Status code: {response.status_code}")
        exit()

def extract_title(soup):
    """Extracts product title from webpage."""
    title_element = soup.find('h1',class_='product-title')
    
    if title_element:
        print(f"\nFound title element")
        title_text = title_element.get_text(strip=True)
        return title_text
    else:
        print("x Could not find title")
        return None
    
def extract_price(soup):
    """Extracts product price from webpage"""
    price_element = soup.find('div', class_='price-current')
    if price_element:
        print(f"\nFound price element!")
        price_text = price_element.get_text(strip=True)
        print(f"Raw text: {price_text}")
    
        clean_price = price_text.replace('$', '').replace(',','')
        price = float(clean_price)
    
        print(f"\nCurrent price: ${price}")
        return price
    else:
        print("x Could not find price element.")
        return None
     
def extract_stock_status(soup):
    """Check if product is in stock by checking Add to cart"""
    add_to_cart_button = soup.find('button', class_='btn-primary')
    
    if add_to_cart_button and 'Add to cart' in add_to_cart_button.get_text():
        print("Product is in Stock")
        return "In Stock"
    else:
        print("Product is out of stock")
        return "Out of stock"
    
def load_price_history(filename):
    """Checks for and loads existing price history from JSON file"""
    if os.path.exists(filename):
        try:
            with open(filename, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            print("Warning: Corrupted JSON file, starting fresh")
            return []
        return []

def save_price_history(filename, data):
    """Save price history to JSON file"""
    with open(filename,'w')as f:
        json.dump(data,f ,indent=4)
    print(f"n\ Price saved to {filename}")
    print(f" Total entries: {len(data)}")
    
# Main Execution
def main():
    """Main function to run price scraper"""
    response = fetch_page(PRODUCT_URL)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    title = extract_title(soup)
    price = extract_price(soup)
    stock_status = extract_stock_status(soup)
    current_time = datetime.now()
    
    print(f"n\Checked at: {current_time}")
    
    price_data ={
        "product": title,
        "price": price,
        "stock_status": stock_status,
        "timestamp": str(current_time),
        "url": PRODUCT_URL
    }

    all_prices = load_price_history(PRICE_HISTORY_FILE)
    all_prices.append(price_data)
    save_price_history(PRICE_HISTORY_FILE, all_prices)
    
if __name__ == "__main__":
    main()
