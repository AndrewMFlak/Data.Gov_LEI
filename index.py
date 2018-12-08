import pandas as pd
import time
import datetime
from bs4 import BeautifulSoup
import urllib.request, urllib.parse, urllib.error
# import substring
#===================SQLite3====================================>
import sqlite3
# connection = sqlite3.connect('LEIscrape.db.sqlite')
connection = sqlite3.connect('TEST.db.sqlite')
cursor = connection.cursor()
cursor.execute('DROP TABLE IF EXISTS lei')
cursor.execute('''CREATE TABLE IF NOT EXISTS Lei(id TEXT, EntityStatus TEXT, Country TEXT, InferredJurisdiction TEXT, RegisteredAddress TEXT, HeadquarteredAddress TEXT, LeiIdentifier TEXT, Name TEXT, RegistrationStatus TEXT, LegalForm TEXT, BusinessRegistryName TEXT, BusinessRegistryAlert TEXT, RegisteredBy TEXT, AssignmentDate TEXT, RecordLastUpdate TEXT, NextRenewalDate TEXT, ItemCount INTEGER, ItemTag TEXT , LoadTime TEXT)''')

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
# ts = time.time()


#=====================================================================>

#========misc variable===========================================>
live = []
nonLive = []
records = []
Total = ''
Finished = False
End = 0
page = 44078
itemCount = 0
itemTag = ''
LEIlist = []
# dataFrame definition
#===========================iterate Variables====================================>
item = ''
# main = ''
# iterateScrape = ''
itemContainer = ''
LeiIdentifier = ''
entityStatus = ''
country = ''
inferredJurisdiction = ''
registeredAddress = ''
headquarterAddress = ''
name = ''
registrationStatus = ''
legalForm = ''
businessRegistryName = ''
businessRegistryAlert = ''
registeredBy = ''
assignmentDate = ''
recordLastUpdate = ''
nextRenewalDate = ''
itemCount = 0
loadTime = ''
#========================= Commit to Pandas Dataframe ==============================>
df = pd.DataFrame(columns=['id', 'EntityStatus','Country', 'InferredJurisdiction','RegisteredAddress', 'HeadquarteredAddress', 'LEI' ,'Name' , 'RegistrationStatus', 'LegalForm', 'BusinessRegistryName', 'BusinessRegistryAlert', 'RegisteredBy', 'AssignmentDate', 'RecordLastUpdate', 'NextRenewalDate', 'ItemCount','ItemTag','LoadTime'])
#======================================================>

#==============================Get of End Value===================================>
def endGet(page, End):
        url = 'http://openleis.com/legal_entities/search/page/' + str(page)
        html = urllib.request.urlopen(url,context=ctx).read()
        soup = BeautifulSoup(html, 'html.parser')
        parentDiv = soup.find('section', {'class':'results row'})
        contentContainer = parentDiv.find('ul', {'class':'results-list with-flags'})
        itemContainer = contentContainer('li')
        try:
                endChild = parentDiv.find('a', {'class':'next_page'})
                EndNode = endChild.find_previous_sibling()
                endGet.End = int(EndNode.text)
        except:
                print('scrape END value GET failed.  Check HTML for cause.')
        return page, End, itemContainer

        #====================== Scrape Functions ================================>
         
def iterateScrape(page, item, itemCount, itemTag, LeiIdentifier):
        try:
                noteContainer = item.find('span', attrs = {'class':'note'})
                LeiIdentifier = noteContainer.a.text
                iterateScrape.LeiIdentifier = LeiIdentifier

        except:
                iterateScrape.LeiIdentifier = "error retrieving LEI value"
                iterateScrape.LeiIdentifier = LeiIdentifier

        # status
        try:
                statusContainer = item['class']
                status = str(statusContainer[0])
                iterateScrape.status = status
        except:
                status = "error retrieving status value"
                iterateScrape.status = status
        # country       
        try:

                container = item.find('a' , attrs = {'class':'flag'})
                country = container['href']
                country = country[-2:]
                iterateScrape.country = country
        except:
                country = "error retrieving country value"
                iterateScrape.country = country
        # name
        try:
                nameContainer = item.find('a' , attrs = {'class':'label'})
                name = nameContainer.text
                name = name.replace('"','')
                name = name.strip()
                iterateScrape.name = name

        except:
                name = "error retrieving name value"
                iterateScrape.name = name
        # registrationStatus
        try:
                statusContainer = item.find('span', attrs = {'title':'Lei Registration Status'})
                registrationStatus = str(statusContainer.text)
                iterateScrape.registrationStatus = registrationStatus

        except:
                registrationStatus = "error retrieving status value"
                iterateScrape.registrationStatus = registrationStatus

        # entityStatus
        try:
                entityStatusContainer = item.find('span', attrs = {'title':'Entity Status'})
                entityStatus = entityStatusContainer.text
                iterateScrape.entityStatus = entityStatus
        except:
                entityStatus = "error retrieving entity status value"
                iterateScrape.entityStatus = entityStatus
                
        # itemCount
        try:
                itemCount = itemCount + 1
                iterateScrape.itemCount = itemCount 
        except:
                itemCount = "error retrieving item count value"
                iterateScrape.itemCount = itemCount

        # itemTag
        try:
                itemTag = str(page) + ' ' + str(itemCount)
                iterateScrape.itemTag = itemTag
        except:
                itemTag = "error retrieving item tag value"
                iterateScrape.itemTag = itemTag
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
        #=================== Attribute Div Items ========================================>
        # legalForm
        try:
                LEI_legal_form = LEI_Div.find('dd', {'class':'legal_form'})
                # print('legal-form: ', LEI_legal_form.text)
                legalForm = LEI_legal_form.text
                iterateScrape.legalForm = legalForm
        except: 
                legalForm = "error retrieving legal form value"
                iterateScrape.legalForm = legalForm

        # registeredAddress
        try:
                LEI_registered_address = LEI_Div.find('dd', {'class':'registered_address'})
                registeredAddress = LEI_registered_address.text
                iterateScrape.registeredAddress = registeredAddress
        except:
                registeredAddress = "error retrieving registered address value"
                iterateScrape.registeredAddress = registeredAddress

        # headquarterAddress
        try:
                LEI_headquartered_address = LEI_Div.find('dd', {'class':'headquarter_address'})
                headquarterAddress = LEI_headquartered_address.text
                iterateScrape.headquarterAddress = headquarterAddress
        except:
                headquarterAddress = "error retrieving headquarter address value"
                iterateScrape.headquarterAddress = headquarterAddress

        # inferredJurisdiction
        try:
                LEI_inferredJurisdiction = LEI_Div.find('dd', {'class':'inferred_jurisdiction'})
                inferredJurisdiction = LEI_inferredJurisdiction.text
                iterateScrape.inferredJurisdiction = inferredJurisdiction
        except:
                inferredJurisdiction = "error retrieving inferred jurisdiction value"
                iterateScrape.inferredJurisdiction = inferredJurisdiction


        # businessRegistryName
        try:
                LEI_businessRegistryName = LEI_Div.find('dd', {'class':'business_registry_name'})
                businessRegistryName = LEI_businessRegistryName.text
                iterateScrape.businessRegistryName = businessRegistryName
        except: 
                businessRegistryName = "error retrieving business registry name value"
                iterateScrape.businessRegistryName = businessRegistryName

        #businessRegistryAlert
        try:
                LEI_businessRegistryAlert = LEI_Div.find('dd', {'class':'business_registry_identifier alert'})
                businessRegistryAlert = LEI_businessRegistryAlert.text
                iterateScrape.businessRegistryAlert = businessRegistryAlert
        except:
                businessRegistryAlert = "error retrieving business registry alert value"
                iterateScrape.businessRegistryAlert = businessRegistryAlert

        #recordLastUpdate
        try:
                LEI_recordLastUpdate = LEI_Div.find('dd', {'class':'record_last_update'})
                recordLastUpdate = LEI_recordLastUpdate.text
                iterateScrape.recordLastUpdate = recordLastUpdate
        except:
                recordLastUpdate = "error retrieving record last update value"
                iterateScrape.recordLastUpdate = recordLastUpdate

        # nextRenewalDate
        try:
                LEI_nextRenewalDate = LEI_Div.find('dd', {'class':'next_renewal_date'})
                nextRenewalDate = LEI_nextRenewalDate.text
                iterateScrape.nextRenewalDate = nextRenewalDate
        except:
                nextRenewalDate = "error retrieving next renewal date value"
                iterateScrape.nextRenewalDate = nextRenewalDate

        # LoadTime
        try:
                ts = time.time()
                st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S.%f')[:-1]
                loadTime = (str(st) +' EST')
                iterateScrape.loadTime = loadTime

        except:
                loadTime = "error retrieving load time values"
                iterateScrape.loadTime = loadTime
        #=================== Attribute Div Items Completed =============================>

        #=================== Detail Attribute Div Items ========================================>
        # LEI_dl2 = LEI_Div.find('dl', {'class':'attributes'})
        # print(LEI_dl2)
        # print(LEI_Div)
        try:
                LEI_registeredBy = LEI_Div.find('dd', {'class':'registered_by'})
                registeredBy = LEI_registeredBy.text
                iterateScrape.registeredBy = registeredBy
        except:
                registeredBy = "error retrieving registered by value"
                iterateScrape.registeredBy = registeredBy
        # print('RegisteredBy: ', registeredBy)
        try:
                LEI_assignmentDate = LEI_Div.find('dd', {'class':'assignment_date'})
                assignmentDate = LEI_assignmentDate.text
                iterateScrape.assignmentDate = assignmentDate
        except: 
                assignmentDate = "error retrieving assignment date value"
                iterateScrape.assignmentDate = assignmentDate
        return LeiIdentifier, entityStatus, country, inferredJurisdiction, registeredAddress, headquarterAddress, name, registrationStatus, legalForm, businessRegistryName, businessRegistryAlert, registeredBy, assignmentDate, recordLastUpdate, nextRenewalDate, itemCount, itemTag, loadTime
                #=================== Detail Attribute Items Completed ==============================>

def captureValues(LeiIdentifier, entityStatus, country, inferredJurisdiction, registeredAddress, headquarterAddress, name, registrationStatus, legalForm, businessRegistryName, businessRegistryAlert, registeredBy, assignmentDate, recordLastUpdate, nextRenewalDate, itemCount, itemTag, loadTime):
        df.append({'id':iterateScrape.LeiIdentifier, 'EntityStatus':iterateScrape.entityStatus, 'Country':iterateScrape.country, 'InferredJurisdiction':iterateScrape.inferredJurisdiction ,'RegisteredAddress':iterateScrape.registeredAddress, 'HeadquarteredAddress':iterateScrape.headquarterAddress ,'LEI':iterateScrape.LeiIdentifier, 'Name':iterateScrape.name ,'RegistrationStatus':iterateScrape.registrationStatus, 'LegalForm':iterateScrape.legalForm, 'BusinessRegistryName': iterateScrape.businessRegistryName, 'BusinessRegistryAlert': iterateScrape.businessRegistryAlert, 'RegisteredBy':iterateScrape.registeredBy, 'AssignmentDate':iterateScrape.assignmentDate , 'RecordLastUpdate': iterateScrape.recordLastUpdate, 'NextRenewalDate': iterateScrape.nextRenewalDate,
        'ItemCount':itemCount,
        'ItemTag':itemTag,
         'LoadTime':iterateScrape.loadTime},ignore_index=True)
        cursor.execute('''INSERT OR REPLACE INTO Lei(id, EntityStatus, Country, InferredJurisdiction, RegisteredAddress, HeadquarteredAddress, LeiIdentifier, Name, RegistrationStatus, LegalForm, BusinessRegistryName, BusinessRegistryAlert, RegisteredBy, AssignmentDate, RecordLastUpdate, NextRenewalDate, ItemCount, ItemTag, LoadTime) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', (iterateScrape.LeiIdentifier, iterateScrape.entityStatus, iterateScrape.country, iterateScrape.inferredJurisdiction, iterateScrape.registeredAddress, iterateScrape.headquarterAddress, iterateScrape.LeiIdentifier, iterateScrape.name, iterateScrape.registrationStatus, iterateScrape.legalForm, iterateScrape.businessRegistryName, iterateScrape.businessRegistryAlert, iterateScrape.registeredBy, iterateScrape.assignmentDate, iterateScrape.recordLastUpdate, iterateScrape.nextRenewalDate, itemCount, itemTag, iterateScrape.loadTime))
        connection.commit()


#============================= Scrape Iterate Item ==============================>
def main(page, End, itemContainer, item, itemTag,itemCount):

        url = 'http://openleis.com/legal_entities/search/page/' + str(page)
        html = urllib.request.urlopen(url,context=ctx).read()
        soup = BeautifulSoup(html, 'html.parser')
        parentDiv = soup.find('section', {'class':'results row'})
        contentContainer = parentDiv.find('ul', {'class':'results-list with-flags'})
        itemContainer = contentContainer('li')
        try:
                endChild = parentDiv.find('a', {'class':'next_page'})
                EndNode = endChild.find_previous_sibling()
                End = int(EndNode.text)
                print('Main End: ', End)
        except:
                print('scrape value GET failed.  This message should populate on second to last page or is change in HTML.')
        for item in itemContainer:
                iterateScrape(page, item, itemCount, itemTag, LeiIdentifier)
                itemCount = iterateScrape.itemCount
                itemTag = iterateScrape.itemTag
                print(iterateScrape.LeiIdentifier, ' ', itemTag)
        captureValues(LeiIdentifier, entityStatus, country, inferredJurisdiction, registeredAddress, headquarterAddress, name, registrationStatus, legalForm, businessRegistryName, businessRegistryAlert, registeredBy, assignmentDate, recordLastUpdate, nextRenewalDate, itemCount, itemTag, loadTime)
        print('last page scrape completed: ', page)
        # page = page + 1
        # print('page: ',page)
        # print('end: ',End)
        # if page > End:
        #         print('Data.gov scrape complete.')
        #         Finished = True
        #         exit()

                # page update and flow through scraper
        return page, End, itemContainer, item, itemTag, itemCount 
        
while Finished == False:
        try:
                endGet(page, End)
                main(page, End, itemContainer, item, itemCount, Finished)
                page = page + 1
                # print('page: ',page)
                # print('end: ',endGet.End)
                if page > endGet.End:
                        print('Data.gov scrape complete.')
                        Finished = True
                        exit()

        except KeyboardInterrupt:
                print('')
                print('Program interrupted by user...')
                Finished = True
                break

        # except TimeoutError:

        # except ConnectionResetError:
        #         continue

        # except Exception as ex:
        #         print("An error was encountered in code please see below for error.")
        #         print(ex)
        #         cursor.close()
        #         exit()

        except Exception as ex:
                if Exception == '[Errno 54] Connection reset by peer':
                        continue
                else:
                        print("An error was encountered in code please see below for error.")
                        print(ex)
                        cursor.close()
                        exit()
#======================= Scrape Iterate Item End ===============================>
#

