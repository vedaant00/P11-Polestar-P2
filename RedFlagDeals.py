# -*- coding: utf-8 -*-
"""
Created on Tue Feb 20 00:30:20 2024

@author: KX S
"""

import urlManager as u
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd

info = pd.DataFrame(columns=['title', 'time', 'texts','link'])
urls = u.UrlManager()
head = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0"}
root_url = "https://forums.redflagdeals.com/search.php?st=0&sk=t&sd=d&sr=posts&keywords=polestar&submit=Search"
urls.add_new_url(root_url)

for start_num in range(20,1120,20):
    add_link = f"&start={start_num}"
    root_url1 = f"https://forums.redflagdeals.com/search.php?st=0&sk=t&sd=d&sr=posts&keywords=polestar&submit=Search{add_link}"
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
    tboxs = soup.find_all("li", class_="row post_item")
    print(len(tboxs))
    for tbox in tboxs:
        time = tbox.find("li", attrs={"class":"post_meta_small_post_date"}).string[:14]
        time = pd.to_datetime(time)
        # print(time)
        if time >= pd.Timestamp('2023-01-01') and time <= pd.Timestamp('2024-2-18'):
            title = tbox.find("a").get_text()
            print(time, "\n", title)
            post_url_re = tbox.find("a").get("href")# Relative link
            # print(post_url_re)
            post_url = f"\nhttps://forums.redflagdeals.com/{post_url_re}"
            print(post_url)
            # print(f"\nhttps://mbworld.org/forums/{post_url_re}")
            p1 = requests.get(post_url, headers=head, timeout=10)
            s1 = BeautifulSoup(p1.text, "html.parser")
            texts = s1.find("article", id=f"{post_url[-9:]}").find('section', class_='post_body').text
            print(texts)
            new_info = {'title':title, 'time':time, 'texts':texts,'link':post_url}
            info = info.append(new_info, ignore_index=True)
        else:
            continue

info.to_excel('RFD_Output1.xlsx', index=False)
