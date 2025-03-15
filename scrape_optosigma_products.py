# -*- coding: utf-8 -*-
"""
Created on Wed Mar 12 19:35:43 2025

@author: Lukas Krauß
"""

import requests
from bs4 import BeautifulSoup
import json

# Define the target URL
url = "https://www.optosigma.com/eu_en/optics/lenses/spherical-lenses/plano-convex-spherical-lenses/n-bk7-plano-convex-lenses-ar-400-700nm-SLB-P-M.html"

# Send HTTP GET request to the URL
response = requests.get(url)
if response.status_code != 200:
    print("Error fetching webpage:", response.status_code)
    exit()

# Retrieve HTML content as text
html_content = response.text

# Parse the HTML using BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

# Find all product rows by selecting <tr> elements with class "grouped-item"
product_rows = soup.find_all('tr', class_='grouped-item')

# Dictionary to store product data in the format:
# { "ProductCode": { "Spec1": "Value1", "Spec2": "Value2", ... } }
product_data = {}

# Iterate over each product row to extract data
for row in product_rows:
    # Finds the product code within the product row  
    # The code is located in an <a> tag inside a <div> container  
    sku_wrapper = row.find('div', class_='product-sku-wrapper')
    if sku_wrapper:
        a_tag = sku_wrapper.find('a', class_='link')
        product_code = a_tag.get_text(strip=True) if a_tag else None
    else:
        product_code = None

    if not product_code:
        continue

    specs = {}

    # Extract simple atributes (e.g., Diameter and Focal Length) from <td> elements with data-label attribute
    diameter_td = row.find('td', attrs={'data-label': lambda x: x and 'Diameter' in x})
    focal_td = row.find('td', attrs={'data-label': 'Focal length'})
    
    if diameter_td:
        specs['Diameter'] = diameter_td.get_text(strip=True)
    if focal_td:
        specs['Focal Length'] = focal_td.get_text(strip=True)
  
    # Extract the price from <td> with class "grouped-item-cell-price"
    price_td = row.find('td', class_='grouped-item-cell grouped-item-cell-price')
    if price_td:
        price_span = price_td.find('span', class_='price')
        if price_span:
            specs['Price'] = price_span.get_text(strip=True)

    # Extract delivery time from <td> with class "product-dw grouped-item-cell grouped-item-cell-dw"
    delivery_td = row.find('td', class_='product-dw grouped-item-cell grouped-item-cell-dw')
    if delivery_td:
        delivery_div = delivery_td.find('div', class_='delivery')
        if delivery_div:
            specs['Delivery'] = delivery_div.get_text(strip=True)

    # Extract detailed product specifications from <td> with class "grouped-item-spec"
    spec_td = row.find('td', class_='grouped-item-spec')
    if spec_td:
        table = spec_td.find('table')
        if table:
            for tr in table.find_all('tr'):
                th = tr.find('th')
                td = tr.find('td')
                if th and td:
                    key = th.get_text(strip=True)
                    value = td.get_text(separator=" ", strip=True)
                    specs[key] = value

    product_data[product_code] = specs

# Save the product data as a JSON file
with open('products.json', 'w', encoding='utf-8') as f:
    json.dump(product_data, f, ensure_ascii=False, indent=4)

print("Data successfully saved to products.json!")
