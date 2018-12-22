import pandas as pd
import time
import datetime
from bs4 import BeautifulSoup
import urllib.request, urllib.parse, urllib.error
# import substring
#===================MongoDB====================================>
import pymongo
try:
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")

except pymongo.errors.ConnectionFailure as e:
    print(e)

# collection defined
mydb = myclient["openleis"]
# mydb.drop_collection("LEIs")
mycol = mydb["LEIs"]
mycol.create_index("_id")
# mycol.create_index("id")

#check out SSL
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
itemTag = ''
# main functions
LeiIdentifier = []
LeiIdentifierValue = ''
status = []
entityStatus = []
entityStatusValue = ''
countryList = []
inferredJurisdiction = []
registeredAddress = []
headquarterAddress = []
nameList = []
registrationStatus = []
legalForm = []
businessRegistryName = []
businessRegistryAlert = []
registeredBy = []
assignmentDate = []
recordLastUpdate = []
nextRenewalDate = []
itemCountList = []
itemTag = []
loadTime = []
loopDictionary = {}
loopCollection = []
# dataFrame definition
#===========================iterate Variables====================================>
item = ''
# main = ''
itemContainer = ''

#==============================Get request of End Value===================================>
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
except:
        print('scrape END value GET failed.  Check HTML for cause.')


#===============================================================================>
#============================= Scrape Iterate Item ==============================>
while Finished == False:
        try:
                url = 'http://openleis.com/legal_entities/search/page/' + str(page)
                html = urllib.request.urlopen(url,context=ctx).read()
                soup = BeautifulSoup(html, 'html.parser')
                parentDiv = soup.find('section', {'class':'results row'})
                contentContainer = parentDiv.find('ul', {'class':'results-list with-flags'})
                itemContainer = contentContainer.find_all('li')
                try:
                        myclient = pymongo.MongoClient("mongodb://localhost:27017/")

                except pymongo.errors.ConnectionFailure as e:
                        print(e)

                # collection defined
                mydb = myclient["openleis"]
                mycol = mydb["LEIs"]
                # mycol.create_index("_id")


                # print(itemContainer)
                for item in itemContainer:
                        try:
                                noteContainer = item.find('span', attrs = {'class':'note'})
                                LeiIdentifierValue = noteContainer.a.text
                                LeiIdentifier.append(LeiIdentifierValue)
                                # print(LeiIdentifier)

                        except:
                                LeiIdentifierValue = "error retrieving LEI value"
                                LeiIdentifier.append(LeiIdentifierValue)

                        # status
                        try:
                                statusContainer = item['class']
                                statusValue = statusContainer[0]
                                status.append(statusValue)
                        except:
                                statusValue = "error retrieving status value"
                                status.append(statusValue)

                        # country       
                        try:
                                container = item.find('a' , attrs = {'class':'flag'})
                                country = container['href']
                                countryValue = country[-2:]
                                countryList.append(countryValue)

                        except:
                                countryValue = "error retrieving country value"
                                countryList.append(countryValue)

                        # name
                        try:
                                nameContainer = item.find('a' , attrs = {'class':'label'})
                                name = nameContainer.text
                                name = name.replace('"','')
                                nameValue = name.strip()
                                nameList.append(nameValue)
                        except:
                                nameValue = "error retrieving name value"
                                nameList.append(nameValue)

                        # registrationStatus
                        try:
                                statusContainer = item.find('span', attrs = {'title':'Lei Registration Status'})
                                registrationStatusValue = statusContainer.text
                                registrationStatus.append(registrationStatusValue)

                        except:
                                registrationStatusValue = "error retrieving status value"
                                registrationStatus.append(registrationStatusValue)

                        # entityStatus
                        try:
                                entityStatusContainer = item.find('span', attrs = {'title':'Entity Status'})
                                entityStatusValue = entityStatusContainer.text
                                entityStatus.append(entityStatusValue)

                        except:
                                entityStatusValue = "error retrieving entity status value"
                                entityStatus.append(entityStatusValue)
                
                        # itemCount
                        try:
                                itemCount = itemCount + 1
                                itemCountList.append(itemCount)
                                # print(LeiIdentifierValue, str(itemCount))
                        except:
                                itemCount = "error retrieving item count value"
                                itemCountList.append(itemCount)

                        # itemTag
                        # try: 
                        #         itemTagValue = 'page. ' + str(page) + " - " + str(itemCount)
                        #         itemTag.append(itemTagValue)

                        # except:
                        #         itemTagValue = "error retrieving item tag value"
                        #         itemTag.append(itemTagValue)
                   
                
                        # print('<===================== Search Page Content Complete =====================>')
                        # print('')
                        # ====================================== LEI Legal Entity details ===================================>
                        LEI_url = 'http://openleis.com/legal_entities/' + str(LeiIdentifierValue)
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
                                legalFormValue = LEI_legal_form.text
                                legalForm.append(legalFormValue)

                        except: 
                                legalFormValue = "error retrieving legal form value"
                                legalForm.append(legalFormValue)

                        # registeredAddress
                        try:
                                LEI_registered_address = LEI_Div.find('dd', {'class':'registered_address'})
                                registeredAddressValue = LEI_registered_address.text
                                registeredAddress.append(registeredAddressValue)

                        except:
                                registeredAddressValue = "error retrieving registered address value"
                                registeredAddress.append(registeredAddressValue)

                        # headquarterAddress
                        try:
                                LEI_headquartered_address = LEI_Div.find('dd', {'class':'headquarter_address'})
                                headquarterAddressValue = LEI_headquartered_address.text
                                headquarterAddress.append(headquarterAddressValue)

                        except:
                                headquarterAddressValue = "error retrieving headquarter address value"
                                headquarterAddress.append(headquarterAddressValue)

                        # inferredJurisdiction
                        try:
                                LEI_inferredJurisdiction = LEI_Div.find('dd', {'class':'inferred_jurisdiction'})
                                inferredJurisdictionValue = LEI_inferredJurisdiction.text
                                inferredJurisdiction.append(inferredJurisdictionValue)

                        except:
                                inferredJurisdictionValue = "United States"
                                inferredJurisdiction.append(inferredJurisdictionValue)

                        # businessRegistryName
                        try:
                                LEI_businessRegistryName = LEI_Div.find('dd', {'class':'business_registry_name'})
                                businessRegistryNameValue = LEI_businessRegistryName.text
                                businessRegistryName.append(businessRegistryNameValue)

                        except: 
                                businessRegistryNameValue = "error retrieving business registry name value"
                                businessRegistryName.append(businessRegistryNameValue)

                        #businessRegistryAlert
                        try:
                                LEI_businessRegistryAlert = LEI_Div.find('dd', {'class':'business_registry_identifier alert'})
                                businessRegistryAlertValue = LEI_businessRegistryAlert.text
                                businessRegistryAlert.append(businessRegistryAlertValue)
                        except:
                                businessRegistryAlertValue = "error retrieving business registry alert value"
                                businessRegistryAlert.append(businessRegistryAlertValue)

                        #recordLastUpdate
                        try:
                                LEI_recordLastUpdate = LEI_Div.find('dd', {'class':'record_last_update'})
                                recordLastUpdateValue = LEI_recordLastUpdate.text
                                recordLastUpdate.append(recordLastUpdateValue)

                        except:
                                recordLastUpdateValue = "error retrieving record last update value"
                                recordLastUpdate.append(recordLastUpdateValue)

                        # nextRenewalDate
                        try:
                                LEI_nextRenewalDate = LEI_Div.find('dd', {'class':'next_renewal_date'})
                                nextRenewalDateValue = LEI_nextRenewalDate.text
                                nextRenewalDate.append(nextRenewalDateValue)
                        except:
                                nextRenewalDateValue = "error retrieving next renewal date value"
                                nextRenewalDate.append(nextRenewalDateValue)

                        # LoadTime
                        try:
                                ts = time.time()
                                st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S.%f')[:-1]
                                loadTimeValue = str(st) +" EST"
                                loadTime.append(loadTimeValue)

                        except:
                                loadTimeValue = "error retrieving load time values"
                                loadTime.append(loadTimeValue)
       
                        #=================== Attribute Div Items Completed =============================>

                        #=================== Detail Attribute Div Items ========================================>
                        try:
                                LEI_registeredBy = LEI_Div.find('dd', {'class':'registered_by'})
                                registeredByValue = LEI_registeredBy.text
                                registeredBy.append(registeredByValue)
                        except:
                                registeredByValue = "error retrieving registered by value"
                                registeredBy.append(registeredByValue)

                        try:
                                LEI_assignmentDate = LEI_Div.find('dd', {'class':'assignment_date'})
                                assignmentDateValue = LEI_assignmentDate.text
                                assignmentDate.append(assignmentDateValue)
                        except: 
                                assignmentDateValue = "error retrieving assignment date value"
                                assignmentDate.append(assignmentDateValue)
                        

                        loopDictionary = {
                        "_id":LeiIdentifierValue,
                        "EntityStatus":entityStatusValue,
                        "Country":countryValue, 
                        "InferredJurisdiction":inferredJurisdictionValue,
                        "RegisteredAddress":registeredAddressValue,   
                        "HeadquarteredAddress":headquarterAddressValue, 
                        "LEI":LeiIdentifierValue,
                        "Name":name, 
                        "RegistrationStatus":registrationStatusValue, 
                        "LegalForm":legalFormValue, 
                        "BusinessRegistryName":businessRegistryNameValue,        
                        "BusinessRegistryAlert":businessRegistryAlertValue, 
                        "RegisteredBy":registeredAddressValue, 
                        "AssignmentDate":assignmentDateValue, 
                        "RecordLastUpdate":recordLastUpdateValue, 
                        "NextRenewalDate":nextRenewalDateValue, 
                        "ItemCount":itemCount,
                        # "ItemTag":itemTagValue,
                        "LoadTime":loadTimeValue
                        }
                        # collection build while looping through records
                        loopCollection.append(loopDictionary)
                
                # below loop to issue upsert command to update or insert depending on if existing record or not.
                try:         
                        # loop collection is an array of dictionaries
                        for iterloop in loopCollection:
                                # the update or insert of dictionary items into mongo
                                mydb.LEIs.update_one({'_id':iterloop['_id']}, {'$set':iterloop}, upsert=True)

                except: 
                        print("mongodb exception thrown on insert operation")
                        print(e)

                #====================================================================>
                print('last page scrape completed: ', page)
        
                page = page + 1
                if page > End:
                        print('Data.gov scrape complete.')
                        Finished = True
                        exit()
                else:
                        continue

        except KeyboardInterrupt:
                print('')
                print('Program interrupted by user...')
                Finished = True
                break

        except Exception as ex:
                if Exception == '[Errno 54] Connection reset by peer':
                        continue
                else:
                        print("An error was encountered in code please see below for error.")
                        print(ex)
                        exit()
# ======================= Scrape Iterate Item End ===============================>
#
