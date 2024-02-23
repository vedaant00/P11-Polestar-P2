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
head = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0"}
root_url = "https://www.insideevsforum.com/community/index.php?search/138799403/&q=polestar&o=date"
urls.add_new_url(root_url)
new_info = {}

for start_num in range(1,11):
    # print(start_num)
    add_link = f"&page={start_num}"
    root_url1 = f"https://www.insideevsforum.com/community/index.php?search/138799403/{add_link}&q=polestar&o=date"
    # print(root_url1)
    urls.add_new_url(root_url1)

a=0


while urls.has_new_url():
    curr_url = urls.get_url()
    r = requests.get(curr_url, headers=head, timeout=10)
    r.encoding = 'utf-8' 
    if r.status_code != 200:
        print("Error in ", curr_url)
        continue
    soup = BeautifulSoup(r.text,"html.parser")
    pattern = re.compile(r'^post\d+$')
    tboxs = soup.find_all("div", class_="listBlock main")
    print(len(tboxs))
    for tbox in tboxs:
        time_ = tbox.find("span", attrs={"class":"DateTime"})
        if time_ is None:
            continue
        time = time_.string
        time = pd.to_datetime(time)
        # print(time)
        if time >= pd.Timestamp('2023-01-01') and time <= pd.Timestamp('2024-2-20'):
            a=a+1
            title = tbox.find("a").get_text()
            print(time, "\n", title)
            post_url_re = tbox.find("a").get("href")# Relative link
            print(post_url_re)
            post_url = f"https://www.insideevsforum.com/community/{post_url_re}"
            print(post_url)
            # print(f"\nhttps://mbworld.org/forums/{post_url_re}")
            p1 = requests.get(post_url, headers=head, timeout=10)
            s1 = BeautifulSoup(p1.text, "html.parser")
            print(post_url[-7:-1])
            texts1 = s1.find("li", id=f"post-{post_url[-7:-1]}")
            if texts1 is None:
                texts1 = soup.find('blockquote', class_="messageText SelectQuoteContainer ugc baseHtml")
            #     # print(texts1)
            #     continue
            texts = texts1.find('div', class_='messageContent').get_text()
            print(texts)
            new_info = {'title':title, 'time':time, 'texts':texts,'link':post_url}
            new_info = pd.DataFrame({'title': [title], 'time': [time], 'texts': [texts], 'link': [post_url]})
            info = pd.concat([info, new_info], ignore_index=True)
 
print(a)
info = info.drop_duplicates()
info.to_excel('InsideEV_Output_nodup.xlsx', index=False)