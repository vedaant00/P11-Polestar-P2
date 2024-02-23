# -*- coding: utf-8 -*-
"""
Created on Thu Feb 22 23:37:08 2024

@author: KX S
"""

import pandas as pd
import re

data = pd.read_excel('merged_data.xlsx')

keywords = [
    "seat", "Leather", "chair", "Driver’s seat", "Passenger seat", "Rear seat", "Headliner", "Roof lining", "overhead interior", "interior", "Footwells",
    "pillar", "A pillar", "B Pillar", "C Pillar", "Frunk", "Trunk", "Lighting",
    "Steering wheel", "Dashboard", " instrument", "panel", "Airbags", "HMI screen",
    "Centre arm rest", "holder", "Cup holder", "Phone holder", "Door panel", "door",
    "Door arm rest", "Door bin", "materials", "interior","color","looking","design","screen","camera","arm rest","Pillar",
    "HID", "High-Intensity Discharge","AC","Air Conditioning","LED", "Light Emitting Diode", 
    "HVAC", "Heating, Ventilation, and Air Conditioning", "LCD", "Liquid Crystal Display", "HUD", "Head-Up Display"
]

def check_keywords(text, keywords):
    text = text if pd.notna(text) else ""  # If the text is not NaN, set it to empty string
    pattern = '|'.join(keywords)  # Create a regular expression pattern to match keywords
    return bool(re.search(pattern, text, flags=re.IGNORECASE))  # Perform a fuzzy search, ignoring case

data['keywords_present'] = data['texts'].apply(lambda text: check_keywords(text, keywords))

entries_to_drop = data[~data['keywords_present']].index
filtered_data = data.drop(entries_to_drop).reset_index(drop=True)
original_shape = data.shape
filtered_shape = filtered_data.shape
filtered_data = filtered_data.drop_duplicates()
filtered_data = filtered_data[["texts", "Source_File"]]

print(filtered_data.info)
filtered_data.to_excel('filtered_data_4forums.xlsx', index=False)