# 檔案名稱: baidu_domain_extractor.py

import requests
from bs4 import BeautifulSoup
import re

def get_domains_from_baidu(query):
    # 構建搜索URL
    search_url = f"https://www.baidu.com/s?wd={query}"
    
    # 發送GET請求
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(search_url, headers=headers)
    
    # 檢查請求是否成功
    if response.status_code != 200:
        print("Failed to retrieve the page")
        return []
    
    # 解析HTML內容
    soup = BeautifulSoup(response.text, "html.parser")
    
    # 提取搜索結果中的網址
    domains = []
    for link in soup.find_all('a', href=True):
        url = link['href']
        # 只提取搜索結果中的有效鏈接
        if url.startswith("http://") or url.startswith("https://"):
            domain = re.findall(r'://([^/]+)/?', url)
            if domain:
                domains.append(domain[0])
    
    # 移除重複的域名
    unique_domains = list(set(domains))
    
    return unique_domains

if __name__ == "__main__":
    query = "Python 教程"
    domains = get_domains_from_baidu(query)
    for domain in domains:
        print(domain)
