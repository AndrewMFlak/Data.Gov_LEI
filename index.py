import pandas as pd
from bs4 import BeautifulSoup
import urllib.request, urllib.parse, urllib.error
#check out 
#ignores SSL certificate errors
import ssl
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

#==================ENV processing=============================>
import os
from os.path import join, dirname
from dotenv import load_dotenv
dotenv_path = join(dirname(__file__),'.env')
load_dotenv(dotenv_path)

dgAPIkey=os.getenv('dataGovAPI')
# print(dgAPIkey)
#==============================================================>

# placeholder = 'www.p-lei.org'
# placeholder = 'http://openleis.com/legal_entities'


# url = input('Enter URL to GET please....')
# if url != '':
#     url = url
# else:
#     url = placeholder


#request/open/get html content
# html = urllib.request.urlopen(placeholder).read()

# soup = BeautifulSoup(html,'html.parser')

# tags = soup('a')
# print(soup)


#======================================================>
url = 'http://openleis.com/legal_entities'
filePath = '/search/page/'
page = 2
#======================================================>
# could add stop=None
# could modify to `while i != stop:`
def enumerate(collection, start=0):
    i = start
    it = iter(collection)
    while 1:
        yield (i,next(it))
        i += 1

def scrape():
    print('some shit')

def live():
        print('live actions to take')

def not_live():
        print('not_live actions to take')

live = []
nonLive = []
records = []
Total = ''
Finished = False

# .read() extracts all data from url provided
# context=ctx to bypass SSL ERROR
html = urllib.request.urlopen(url,context=ctx).read()
soup = BeautifulSoup(html, 'html.parser')
#====================ParentDiv parse============================>
parentDiv = soup.find('section', {'class':'results row'})
#===============================================================>


#====================TotalValue parse============================>
totalContainer = parentDiv.find_all('h1')
for line in totalContainer:
        # print(type(line))
        Total=line.get_text()
        print(Total)
#===============================================================>


#====================itemInfo parse==============================>
liveItemCount = 0
liveItems = ''
not_liveItems = ''
contentContainer = parentDiv.find('ul', {'class':'results-list with-flags'})
itemContainer = contentContainer('li')
# print(itemContainer)
liveItems = contentContainer.find_all('li', {'class':'live'})
# print(liveItems)
not_liveItems = contentContainer.find_all('li',{'class':'not_live'})
#=============================Live======================================>
for liveItem in liveItems:
        item
#=======================================================================>

#============================Not_Live===================================>
for not_liveItem in not_liveItems:
        print(not_liveItem)
#=======================================================================>

# liveItems.append(itemContainer.find_all('li',{'class':'live'}))
# not_liveItems.append(itemContainer.find_all('li',{'class':'not_live'}))
# print(not_liveItems)
# for item in itemContainer:
#         liveItems.append()
#         print('live: ',liveItems)
#         not_liveItems.append()
#         print('not_live: ',not_liveItems)

        # if item.find('li', {'class'}) == 'live':
        #         print('live:',item)
        # elif item.find('li',{'class'}) == 'not_live':
        #         print('not_live: ',item)
        # else:
        #         break
        #Filter live/non_live first
        # itemCount = itemCount + 1
        # print(item)
#===============================================================>


# for child in parentDiv.descendants:
#     print(child)

# totalDiv = soup.find('section', {'class':'results row'})
# totalContainer = soup.find('h1')

# 
    # while Total == '':
    #     totCondition = child.find('h1')
    #     print(totCondition.contents)
    #     Total = 1

        # total = totCondition.find_next_sibling("em")
        # print(total)
    # child.find('li', {'class':'results-list with-flags'})
# r# for child in ParentDiv.children:
#     print(child)

# for child in children:
#     print(child)


# for node in container:
#     print(node)
    # try:
    #     totalRecord = container.find('h1')
    #     print(node)
    # except:
    #     print('h1 scrape fail')

    # try:
    #     leiRecords = container.find_all('li')
    # except:
    #     print('li scrape fail')
    

# for singleRecord in leiRecords:
#     print('sr: ',leiRecords)


# live = soup.find_all('li', {'class':'live'})
# nonLive = soup.find_all('li', {'class':'not_live'})

#===================Total LEI count================================>
# for tr in totalRecord:
#     print('tr: ',tr)

# Total = soup.find('em').text
# print('Total: ',Total)

#==================================================================>

# count = 0
# for em in ems:
#     print(count + 1,':', em)


#sanity check
# url = 'https://www.financialresearch.gov/data/legal-entity-identifier/'
#.read() extracts all data from url provided
#context=ctx to bypass SSL ERROR
# html = urllib.request.urlopen(url,context=ctx).read()

# soup = BeautifulSoup(html,'html.parser')
# print(soup.prettify())
# pTags = soup('p')
# for p in pTags:
#     print('')
# spanTags = soup('span')
#====================basic workflow model========================>
# while Finished == False:
#     try:
#         scrape()
#     except:
#         print('LEI scrape complete')

#================================================================>

# testTotal = soup.find('p', {'class':'map-hed'})
# print(testTotal.get_text())
# spanTotal = testTotal.findChildren('span')
# print(spanTotal)
#check out 


