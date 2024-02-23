# -*- coding: utf-8 -*-
"""
Created on Tue Feb 20 12:02:07 2024

@author: KX S
"""

import urlManager as u
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd

info = pd.DataFrame(columns=['title', 'time', 'texts','link'])
urls = u.UrlManager()
head = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"}
root_url = "https://www.vwvortex.com/search/2488162/?q=polestar&o=relevance"
urls.add_new_url(root_url)
a=0

for start_num in range(2,25):
    # print(start_num)
    add_link = f"page={start_num}"
    root_url1 = f"https://www.vwvortex.com/search/2488162/?{add_link}&q=polestar&c[searchProfileName]=control&o=relevance"
    print(root_url1)
    urls.add_new_url(root_url1)




while urls.has_new_url():
    curr_url = urls.get_url()
    r = requests.get(curr_url, headers=head, timeout=10)
    r.encoding = 'utf-8' 
    if r.status_code != 200:
        print("Error in ", curr_url)
        continue
    soup = BeautifulSoup(r.text,"html.parser")
    pattern = re.compile(r'^post\d+$')
    tboxs = soup.find_all("div", class_="contentRow-main")
    print(len(tboxs))
    for tbox in tboxs:
        time_ = tbox.find("time")
        if time_ is None:
            continue
        time = time_.string
        
       # Convert formats like "3h ago" and "7d ago" to time format
        from datetime import datetime, timedelta
        # Define a regular expression to match the time format
        pattern = re.compile(r'^(\d+)([hd])\s+ago$')
        
        def parse_time_ago(string):
            # Match using regular expression
            match = pattern.match(string)
            if match:
                # Get the time and unit
                value = int(match.group(1))
                unit = match.group(2)
                
                # Calculate time delta based on the unit
                if unit == 'h':
                    delta = timedelta(hours=value)
                elif unit == 'd':
                    delta = timedelta(days=value)
                
                # Calculate the past time
                past_time = datetime.now() - delta
                return past_time
            else:
                return string
        
        time = parse_time_ago(time)
        time = pd.to_datetime(time)
        print(time)
        if time >= pd.Timestamp('2023-01-01') and time <= pd.Timestamp('2024-2-20'):
            a=a+1
            title = tbox.find("h3", class_="contentRow-title").get_text()
            print(time, "\n", title)
            post_url_re = tbox.find("a").get("href")# Relative link
            print(post_url_re)
            post_url = f"https://www.vwvortex.com/{post_url_re}"
            print(post_url)
            p1 = requests.get(post_url, headers=head, timeout=10)
            s1 = BeautifulSoup(p1.text, "html.parser")
            print(post_url[-14:])
            texts1 = s1.find('article', id=f"js-{post_url[-14:]}")
            if texts1 is None:
                texts1 = s1.find("div", id=f"js-{post_url[-14:]}")
                print(texts1)
            texts_ = texts1.find('div', class_='bbCodeBlock-expandContent')
            if texts_ is None:
                texts_ = texts1.find('div', class_="bbWrapper")
                print(texts_)
            texts = texts_.get_text()
            print(texts)
            new_info = {'title':title, 'time':time, 'texts':texts,'link':post_url}
            info = info._append(new_info, ignore_index=True)
        

info.to_excel('VWVortex.xlsx', index=False)
print(a)