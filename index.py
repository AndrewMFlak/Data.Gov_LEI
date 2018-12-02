import pandas as pd
from bs4 import BeautifulSoup
import urllib.request, urllib.parse, urllib.error
import substring
#check out 
#===================SSL certificate errors=====================>
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

#data.gov API key not necessary
# dgAPIkey=os.getenv('dataGovAPI')
# print(dgAPIkey)
#==============================================================>


#========misc variable===========================================>
live = []
nonLive = []
records = []
Total = ''
Finished = False
end = 5
page = 1
url = 'http://openleis.com/legal_entities/search/page/' + str(page)
#======================================================>
# .read() extracts all data from url provided
# context=ctx to bypass SSL ERROR
#=========WHERE TO PUT THIS SHIT==================================>
# while page <= end:
#         try:    
html = urllib.request.urlopen(url,context=ctx).read()
soup = BeautifulSoup(html, 'html.parser')
paginationContainer = soup.find('div', {'class':'pagination'})
pageTurner = 'http://openleis.com'
pathFiller = '/legal_entities/search/page/'

#================================================================>



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
liveItems = ''
not_liveItems = ''
liveItemCount = 0
notLiveItemCount = 0
df = []
contentContainer = parentDiv.find('ul', {'class':'results-list with-flags'})
itemContainer = contentContainer('li')
# print(itemContainer)
liveItems = contentContainer.find_all('li', {'class':'live'})
# print(liveItems)
not_liveItems = contentContainer.find_all('li',{'class':'not_live'})


#=============================Item Iterate==============================>
for item in itemContainer:
# for liveItem in liveItems:
        print('<=====================New Record=====================>')
        statusContainer = item['class']
        status = str(statusContainer[0])
        print('1. ',status)
        container = item.find('a' , attrs = {'class':'flag'})
        country = container['href']
        country = country[-2:]
        print('2. ',country)
        nameContainer = item.find('a' , attrs = {'class':'label'})
        name = nameContainer.text
        name = name.replace('"','')
        name = name.strip()
        print('3. ',name)
        statusContainer = item.find('span', attrs = {'title':'Lei Registration Status'})
        print('4. ',statusContainer.text)
        entityStatusContainer = item.find('span', attrs = {'title':'Entity Status'})
        entityStatus = entityStatusContainer.text
        print('5. ',entityStatus)
        noteContainer = item.find('span', attrs = {'class':'note'})
        LEI = noteContainer.a.text
        print('6. ',LEI)
        liveItemCount = liveItemCount + 1
        print('7. ',liveItemCount)
        print('<===================Record Complete===================>')
        print('')
        print('')
#=======================================================================>
#
#
#
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


