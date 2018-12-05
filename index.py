import pandas as pd
from bs4 import BeautifulSoup
import urllib.request, urllib.parse, urllib.error
import substring
#===================SQLite3====================================>
import sqlite3
connection = sqlite3.connect('LEIscrape.db.sqlite')
cursor = connection.cursor()
cursor.execute('DROP TABLE IF EXISTS lei')
cursor.execute('''CREATE TABLE IF NOT EXISTS Lei    (id TEXT UNIQUE, EntityStatus TEXT,            Country TEXT, LeiIdentifier TEXT, Name TEXT,     RegistrationStatus TEXT, RecordCount INTEGER)''')

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
End = 0
page = 1
itemCount = 0
LEIlist = []
# dataFrame definition
df = pd.DataFrame(columns=['id', 'EntityStatus','Country', 'LEI' ,'Name' , 'RegistrationStatus', 'RecordCount'])
#======================================================>


while Finished == False:
    try:
        url = 'http://openleis.com/legal_entities/search/page/' + str(page)
# .read() extracts all data from url provided

#=========WHERE TO PUT THIS SHIT==================================>
# context is equal to ctx. Is used to bypass SSL ERROR
        html = urllib.request.urlopen(url,context=ctx).read()
        soup = BeautifulSoup(html, 'html.parser')
        paginationContainer = soup.find('div', {'class':'pagination'})
        pageTurner = 'http://openleis.com'
        pathFiller = '/legal_entities/search/page/'

#================================================================>



#==================== ParentDiv parse ============================>
        parentDiv = soup.find('section', {'class':'results row'})
        # print(parentDiv)
#===============================================================>



#====================itemInfo parse==============================>
#soup row containing all content to scrape
        contentContainer = parentDiv.find('ul', {'class':'results-list with-flags'})
        # print(contentContainer)
        itemContainer = contentContainer('li')

#====================store total pages to scrape==================>
        try:
            endChild = parentDiv.find('a', {'class':'next_page'})
            EndNode = endChild.find_previous_sibling()
            End = int(EndNode.text)
            # print(End)
        except:
            print('Total end value GET failed.  Check HTML for cause.')
            
#=================================================================>


#====================TotalValue parse============================>
        #TOTAL LEI GET NOT WORKING.  need scrub output.
        # totalContainer = parentDiv.find_all('h1')
        # for line in totalContainer:
        #         # print(type(line))
        #         Total=line.get_text()
        #         print(Total)
#===============================================================>

#============================= Scrape Iterate Item ==============================>
        for item in itemContainer:
                # print('<=====================New Record=====================>')
                statusContainer = item['class']
                status = str(statusContainer[0])
                # print('1. ',status)
                container = item.find('a' , attrs = {'class':'flag'})
                country = container['href']
                country = country[-2:]
                # print('2. ',country)
                nameContainer = item.find('a' , attrs = {'class':'label'})
                name = nameContainer.text
                name = name.replace('"','')
                name = name.strip()
                # print('3. ',name)
                statusContainer = item.find('span', attrs = {'title':'Lei Registration Status'})
                registrationStatus = str(statusContainer.text)
                # print('4. ',registrationStatus)
                entityStatusContainer = item.find('span', attrs = {'title':'Entity Status'})
                entityStatus = entityStatusContainer.text
                # print('5. ',entityStatus)
                noteContainer = item.find('span', attrs = {'class':'note'})
                LeiIdentifier = noteContainer.a.text
                # print('6. ',LeiIdentifier)
                itemCount = itemCount + 1
                # print('7. ',liveItemCount)
                # print('<===================Record Complete===================>')
                # print('')
                # print('')
                df = df.append({'id':LeiIdentifier,'EntityStatus':entityStatus,'Country':country, 'LEI':LeiIdentifier ,'Name':name, 'RegistrationStatus':registrationStatus, 'RecordCount':itemCount},ignore_index=True)
                cursor.execute('''INSERT OR REPLACE INTO Lei(id, EntityStatus, Country, LeiIdentifier, Name, RegistrationStatus, RecordCount) 
                VALUES (?, ?, ?, ?, ?, ?, ?)''', (LeiIdentifier, entityStatus, country, LeiIdentifier, name, registrationStatus, itemCount))
        connection.commit()
        print('last page scrape completed: ', page)
        page = page + 1



        # print(df)
        if page > End:
            print('Data.gov scrape complete.')
            Finished = True
            exit()

    except KeyboardInterrupt:
        print('')
        print('Program interrupted by user...')
        Finished = True
        break

    except Exception as ex:
        print("An error was encountered in code please see below for error.")
        # print error
        print(ex)
        cursor.close()
        exit()
#======================= Scrape Iterate Item End ===============================>
#

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

# testTotal = soup.find('p', {'class':'map-hed'})
# print(testTotal.get_text())
# spanTotal = testTotal.findChildren('span')
# print(spanTotal)
#check out 


