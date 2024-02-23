# -*- coding: utf-8 -*-
"""
Created on Sun Feb 18 12:48:31 2024

@author: a27810ks
"""

import urlManager as u
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd

info = pd.DataFrame(columns=['title', 'time', 'texts','link'])

root_url = "https://mbworld.org/forums/search.php?searchid=30693924"
head = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0"}

urls = u.UrlManager()
urls.add_new_url(root_url)


while urls.has_new_url():
    curr_url = urls.get_url()
    r = requests.get(curr_url, headers=head, timeout=10)
    r.encoding = 'utf-8' 
    if r.status_code != 200:
        print("Error in ", curr_url)
        continue
    soup = BeautifulSoup(r.text,"html.parser")
    pattern = re.compile(r'^post\d+$')
    tboxs = soup.find_all("div", class_="tbox", id=pattern)
    print(len(tboxs))
    for tbox in tboxs:
        time = tbox.find("span", attrs={"style":"vertical-align: middle;"}).string[:10]
        time = pd.to_datetime(time)
        # print(time)  time >= pd.Timestamp('2023-01-01') and
        if time >= pd.Timestamp('2023-01-01') and time <= pd.Timestamp('2024-2-19'):
            title = tbox.find("div", class_="tcell alt1").find("a").string
            print(time, "\n", title)
            post_url_re = tbox.find("em").find("a").get("href")# Relative link
            post_url = f"\nhttps://mbworld.org/forums/{post_url_re}"
            if post_url[-7:-3] == "8787" or post_url[-7:] == "8791773" or post_url[-7:] == "8791585":
                print("1111")
                continue
            print(f"\nhttps://mbworld.org/forums/{post_url_re}")
            p1 = requests.get(post_url, headers=head, timeout=10)
            s1 = BeautifulSoup(p1.text, "html.parser")
            texts1 = s1.find("div", id=f"post_message_{post_url[-7:]}")
            if texts1 is None:
                texts1 = s1.find("div", id=f"td_post_{post_url[-7:]}")
            texts = texts1.get_text()
            print(texts)
            new_info = pd.DataFrame({'title': [title], 'time': [time], 'texts': [texts], 'link': [post_url]})
            info = pd.concat([info, new_info], ignore_index=True)
        else:
            continue

info.to_excel('MBWORD_Output.xlsx', index=False)
 
# time = soup.find("div", attrs={"class":"tbox"}).find("div").find("div").find("span")
#     fout.write("%s,%s\n"%(curr_url, title))
#     fout.flush() #鍗充娇鎶婃洿鏂板啓鍏ョ鐩�
#     print("success: %s, %s, %d"%(curr_url, title, len(urls.new_urls)))
    
#     links = soup.findAll("a")
#     for link in links:
#         href = link.get("href")
#         if href is None:
#             continue
#         # 姝ｅ垯琛ㄨ揪寮弐e--閫氳繃瑙傚療缃戦〉閾炬帴寰楀埌,\d+鏄涓暟瀛楋紝$鏄粨鏉熺
#         pattern = r'^http://www.crazyant.net/\d+.html$'
#         if re.match(pattern,href):
#             urls.add_new_url(href)

