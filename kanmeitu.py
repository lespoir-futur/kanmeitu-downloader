import requests
import sys
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import os
import sys

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
baseurl = sys.argv[1]

for i in range(2,100):
    url = baseurl + str(i) + '.html'
    try:
        response = requests.get(url)
        response.raise_for_status()  # check for HTTP errors
    except requests.exceptions.RequestException as e:
        print(e)
        exit(1)
    
    soup = BeautifulSoup(response.content,'html.parser')
    img_tags = soup.find_all('img')
    img_urls = [img['src'] for img in img_tags if 'src' in img.attrs]
    for img_url in img_urls:
        img_url = urljoin(url, img_url)
  
        try:
            response = requests.get(img_url, headers=headers)
            response.raise_for_status()  
        except requests.exceptions.RequestException as e:
            print(e)
            continue 
    
        filename = '{}.{}'.format(os.path.splitext(url.split('/')[-1])[0], response.headers['Content-Type'].split('/')[1])
        with open(filename, 'wb') as f:
            f.write(response.content)


