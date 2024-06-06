"""
title: Web Scraper for Python
author: Ayaan Merchant
date: 2024-06-05
"""

from urllib.request import urlopen
from bs4 import BeautifulSoup
import ssl

# DEFINE THE URLS - if you input url, remove "" from inside the url
urlAKUDiscovery = "https://eds.p.ebscohost.com/eds/results?vid=1&sid=f4727b24-52ba-4979-ad9a-83971d0fbe18%40redis&bquery=(AI+OR+%22Artificial+Intelligence%22+OR+%22AI+Robotics%22+OR+%22AI+Automation%22)+AND+(%22Early+Childhood+Education%22+OR+%22Early+Years+Education%22+OR+ECE)+AND+(%22AI+Applications%22+OR+%22AI+Uses%22+OR+%22AI+Usefulness%22+OR+%22AI+Educational+Technology%22)&bdata=JkF1dGhUeXBlPXNzbyZ0eXBlPTAmc2VhcmNoTW9kZT1BbmQmc2l0ZT1lZHMtbGl2ZQ%3d%3d"

context = ssl._create_unverified_context() #make an unverified SSL context to bypass ssl certification as needed

#GET HTML CONTENTS FROM WEBSITES
html = urlopen(urlAKUDiscovery, context=context)
soup = BeautifulSoup(html, 'html.parser')

page_number = 1
while True:
    # Find all divs with the class 'result-list'
    result_list_divs = soup.find_all('div', class_='result-list-record')