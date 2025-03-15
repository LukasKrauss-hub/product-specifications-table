# -*- coding: utf-8 -*-
"""
Created on Fri Mar 14 06:29:51 2025


@author: Lukas Krauß
"""

import json
import re

# Load the JSON data from a file
with open('products.json', 'r', encoding='utf-8') as f:
    product_data = json.load(f)

# Define the most important specs
important_specs = ['Diameter', 'Focal Length', 'Price', 'Delivery']

# A mapping from the JSON file's keys to our standard specification names
spec_name_mapping = {
    'Diameter φD': 'Diameter',
    'Focal length f': 'Focal Length',
    # "Price" and "Delivery" are already in the desired format.
}

# Function to separate the number and unit from a string (e.g., "25mm" => "25", "mm")
def split_value_and_unit(text):
    """
    Splits the numeric value and unit from a string.
    Example:
       "25mm"     => ("25", "mm")
       "42,50 €"  => ("42,50", "€")
    If no match is found, returns the original text and an empty string.
    """
    # This regex pattern splits the value from the unit, supporting decimal numbers and various units
    pattern = r"^\s*([0-9]+(?:[.,][0-9]+)?)\s*([^0-9\s]*)\s*$"
    match = re.match(pattern, text)
    if match:
        number = match.group(1)  # Get the number part
        unit = match.group(2) if match.group(2) is not None else ""  # Get the unit part
        return number, unit
    else:
        return text, ""  # If no match, return the original text and an empty unit

# Create and print the table header with column names
header = f"{'Product Code':<20}"
for spec in important_specs:
    header += f"{spec:<25}"
print(header)
print("-" * len(header))  # Print a separator line for the header

# Iterate over each product in the loaded data and print their information
for product_code, specs in product_data.items():
    row = f"{product_code:<20}"  # Start the row with the product code
    for spec in important_specs:
        original_key = None
        # Check through all keys in the product's specification
        for key in specs.keys():
            # Remove extra spaces and convert the key and spec name to lowercase for comparison
            key_clean = key.strip().lower()
            spec_clean = spec.strip().lower()
            # If the key matches the standard specification name, use it
            if key_clean == spec_clean:
                original_key = key
                break
            # If the key can be mapped to the standard specification name, use it
            elif key.strip() in spec_name_mapping:
                mapped = spec_name_mapping[key.strip()].strip().lower()
                if mapped == spec_clean:
                    original_key = key
                    break

        # If the specification was not found, set it to "N/A"
        value = specs.get(original_key, "N/A")
        if value != "N/A":
            # If there is a valid value, split it into a number and unit if possible
            number, unit = split_value_and_unit(value)
            if unit:
                cell = f"{number} {unit}"  # Show both number and unit
            else:
                cell = number  # If no unit, show just the number
        else:
            cell = value  # If no value, show "N/A"

        row += f"{cell:<25}"  # Add the value for the specification to the row
    print(row)  # Print the row for the current product
