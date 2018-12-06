import pandas as pd
import time
import datetime
from bs4 import BeautifulSoup
import urllib.request, urllib.parse, urllib.error
import substring
#===================SQLite3====================================>
import sqlite3
# connection = sqlite3.connect('LEIscrape.db.sqlite')
connection = sqlite3.connect('TEST.db.sqlite')
cursor = connection.cursor()
cursor.execute('DROP TABLE IF EXISTS lei')
cursor.execute('''CREATE TABLE IF NOT EXISTS Lei(id TEXT UNIQUE, EntityStatus TEXT, Country TEXT, InferredJurisdiction TEXT, RegisteredAddress TEXT, HeadquarteredAddress TEXT, LeiIdentifier TEXT, Name TEXT, RegistrationStatus TEXT, LegalForm TEXT, BusinessRegistryName TEXT, BusinessRegistryAlert TEXT, RegisteredBy TEXT, AssignmentDate TEXT, RecordLastUpdate TEXT, NextRenewalDate TEXT, RecordCount INTEGER, LoadTime TEXT)''')

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

#========================TIME variables===============================>
ts = time.time()


#=====================================================================>

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
df = pd.DataFrame(columns=['id', 'EntityStatus','Country', 'InferredJurisdiction','RegisteredAddress', 'HeadquarteredAddress', 'LEI' ,'Name' , 'RegistrationStatus', 'LegalForm', 'BusinessRegistryName', 'BusinessRegistryAlert', 'RegisteredBy', 'AssignmentDate', 'RecordLastUpdate', 'NextRenewalDate', 'RecordCount','LoadTime'])
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
                # print('<===================== Search Page Content =====================>')
                # LeiIdentifier
                try:
                        noteContainer = item.find('span', attrs = {'class':'note'})
                        LeiIdentifier = noteContainer.a.text
                        # print('1. ',LeiIdentifier)

                except:
                        LeiIdentifier = "error retrieving LEI value"

                # status
                try:
                        statusContainer = item['class']
                        status = str(statusContainer[0])
                        # print('1. ',status)
                except:
                        status = "error retrieving status value"

                # country       
                try:

                        container = item.find('a' , attrs = {'class':'flag'})
                        country = container['href']
                        country = country[-2:]
                        # print('2. ',country)
                except:
                        country = "error retrieving country value"

                # name
                try:
                        nameContainer = item.find('a' , attrs = {'class':'label'})
                        name = nameContainer.text
                        name = name.replace('"','')
                        name = name.strip()
                except:
                        name = "error retrieving name value"
                        # print('3. ',name)

                # registrationStatus
                try:
                        statusContainer = item.find('span', attrs = {'title':'Lei Registration Status'})
                        registrationStatus = str(statusContainer.text)
                        # print('4. ',registrationStatus)

                except:
                        registrationStatus = "error retrieving status value"

                # entityStatus
                try:
                        entityStatusContainer = item.find('span', attrs = {'title':'Entity Status'})
                        entityStatus = entityStatusContainer.text
                        # print('5. ',entityStatus)

                except:
                        entityStatus = "error retrieving entity status value"

                
                
                # itemCount
                itemCount = itemCount + 1
                # print('7. ',liveItemCount)
                # print('<===================== Search Page Content Complete =====================>')
                # print('')
                # print('')
                # ====================================== LEI Legal Entity details ===================================>
                LEI_url = 'http://openleis.com/legal_entities/' + str(LeiIdentifier)
                LEI_html = urllib.request.urlopen(LEI_url,context=ctx).read()
                soup = BeautifulSoup(LEI_html, 'html.parser')
                LEI_Container = soup.find('section', {'class':'row entity-details'})
                LEI_Div = LEI_Container.find('div', {'class':'main'})
                # LEI_dl = LEI_Div.find('dl', {'class':'attributes first'})
                #=================== Detail Items ========================================>
                # legalForm
                try:
                        LEI_legal_form = LEI_Div.find('dd', {'class':'legal_form'})
                        # print('legal-form: ', LEI_legal_form.text)
                        legalForm = LEI_legal_form.text
                except: 
                        legalForm = "error retrieving legal form value"

                # registeredAddress
                try:
                        LEI_registered_address = LEI_Div.find('dd', {'class':'registered_address'})
                        registeredAddress = LEI_registered_address.text
                        # print('registered-address: ', registeredAddress)
                except:
                        registeredAddress = "error retrieving registered address value"

                # headquarterAddress
                try:
                        LEI_headquartered_address = LEI_Div.find('dd', {'class':'headquarter_address'})
                        headquarterAddress = LEI_headquartered_address.text
                        # print('headquarterd-address: ', headquarterAddress)
                except:
                        headquarterAddress = "error retrieving headquarter address value"

                # inferredJurisdiction
                try:
                        LEI_inferredJurisdiction = LEI_Div.find('dd', {'class':'inferred_jurisdiction'})
                        inferredJurisdiction = LEI_inferredJurisdiction.text
                        # print('inferredJurisdiction: ', inferredJurisdiction)
                except:
                        inferredJurisdiction = "error retrieving inferred jurisdiction value"

                # businessRegistryName
                try:
                        LEI_businessRegistryName = LEI_Div.find('dd', {'class':'business_registry_name'})
                        businessRegistryName = LEI_businessRegistryName.text
                        # print('businessRegistryName: ',businessRegistryName)
                except: 
                        businessRegistryName = "error retrieving business registry name value"

                #businessRegistryAlert
                try:
                        LEI_businessRegistryAlert = LEI_Div.find('dd', {'class':'business_registry_identifier alert'})
                        businessRegistryAlert = LEI_businessRegistryAlert.text
                        # print('businessRegistryAlert: ', businessRegistryAlert)
                except:
                        businessRegistryAlert = "error retrieving business registry alert value"

                #recordLastUpdate
                try:
                        LEI_recordLastUpdate = LEI_Div.find('dd', {'class':'record_last_update'})
                        recordLastUpdate = LEI_recordLastUpdate.text
                except:
                        recordLastUpdate = "error retrieving record last update value"

                # nextRenewalDate
                try:
                        LEI_nextRenewalDate = LEI_Div.find('dd', {'class':'next_renewal_date'})
                        nextRenewalDate = LEI_nextRenewalDate.text
                except:
                        nextRenewalDate = "error retrieving next renewal date value"

                # LoadTime
                try:
                        st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S.%f')[:-5]
                        loadTime = st
                except:
                        loadTime = "error retrieving load time values"
                #=================== Detail Items Completed =============================>

                #=================== Detail Attribute Items ========================================>
                # LEI_dl2 = LEI_Div.find('dl', {'class':'attributes'})
                # print(LEI_dl2)
                # print(LEI_Div)
                LEI_registeredBy = LEI_Div.find('dd', {'class':'registered_by'})
                registeredBy = LEI_registeredBy.text
                # print('RegisteredBy: ', registeredBy)
                LEI_assignmentDate = LEI_Div.find('dd', {'class':'assignment_date'})
                assignmentDate = LEI_assignmentDate.text
                # print('AssignmentDate: ', assignmentDate)



                #=================== Detail Attribute Items Completed ==============================>



                
                
                df = df.append({'id':LeiIdentifier, 'EntityStatus':entityStatus, 'Country':country, 'InferredJurisdiction':inferredJurisdiction ,'RegisteredAddress':registeredAddress, 'HeadquarteredAddress':headquarterAddress ,'LEI':LeiIdentifier, 'Name':name ,'RegistrationStatus':registrationStatus, 'LegalForm':legalForm, 'BusinessRegistryName': businessRegistryName, 'BusinessRegistryAlert': businessRegistryAlert, 'RegisteredBy':registeredBy, 'AssignmentDate':assignmentDate , 'RecordLastUpdate': recordLastUpdate, 'NextRenewalDate': nextRenewalDate,'RecordCount':itemCount, 'LoadTime':loadTime},ignore_index=True)
                print(df)
                cursor.execute('''INSERT OR REPLACE INTO Lei(id, EntityStatus, Country, InferredJurisdiction, RegisteredAddress, HeadquarteredAddress, LeiIdentifier, Name, RegistrationStatus, LegalForm, BusinessRegistryName, BusinessRegistryAlert, RegisteredBy, AssignmentDate, RecordLastUpdate, NextRenewalDate, RecordCount, LoadTime) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', (LeiIdentifier, entityStatus, country, inferredJurisdiction, registeredAddress, headquarterAddress, LeiIdentifier, name, registrationStatus, legalForm, businessRegistryName, businessRegistryAlert, registeredBy, assignmentDate, recordLastUpdate, nextRenewalDate, itemCount, loadTime))
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


