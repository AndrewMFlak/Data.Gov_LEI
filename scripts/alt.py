import pandas as pd
from bs4 import BeautifulSoup
import time
import datetime
import io
import urllib.request
import urllib.parse
from urllib.request import urlopen
import json
from pandas.io.json import json_normalize

#===============SSL certificate errors===============>
import ssl
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

#=======================.ENV========================>
import os
from os.path import join, dirname
import dotenv
from dotenv import load_dotenv
dotenv_path = join(dirname(__file__),'../.env')
load_dotenv(dotenv_path)

# data.gov details committed to variables
username=os.getenv('dGovUsername')
password=os.getenv('dGovPassword')

#======================================================>

#=========================MongoDB=========================>
import pymongo
# from pymongo import MongoClient
try:
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
except pymongo.errors.ConnectionFailure as e:
    print(e)
my_list = []
my_df = ''
steps = []
listLength= 0
db = myclient["openLeisJSON"]
col = db["leisJSON"]

# count variables not used
ct = 0
# workflow page variable
lastPage = 0
End = 0
#FUNCTIONS

def getEnd(page):
    url = 'http://openleis.com/legal_entities/search/page/' + str(page)
    html = urllib.request.urlopen(url,context=ctx).read()
    soup = BeautifulSoup(html, 'html.parser')
    parentDiv = soup.find('section', {'class':'results row'})
    try:
        endChild = parentDiv.find('a', {'class':'next_page'})
        EndNode = endChild.find_previous_sibling()
        End = int(EndNode.text)
    except:
        print('scrape END value GET failed.  Check HTML for cause.')
        End = 69
    return End

#Write dataframe from openLeis JSON and push to MongoDB
def write_df_to_mongoDB(
    my_df = my_df,\
    database_name = 'openLeisJSON',\
    collection_name = 'leisJSON',\
    server = 'localhost',\
    mongodb_port = 27017,\
    chunk_size = 30):
    # End = getEnd().End):
    col.create_index("_id")
    # To write

    # collection.delete_many({})  
    # Destroy the collection
    #aux_df=aux_df.drop_duplicates(subset=None, keep='last') # To avoid repetitions
    my_list = my_df.to_dict('records')
       
    for item in my_list:
        # print(item)
        try:
            db.leisJSON.update_one({'_id':item['lei']}, {'$set':item},upsert=True)
        except pymongo.errors.ConnectionFailure as e: 
            print("Insert_OneError:",e)
    

#==========================================================>


#=====================variables==========================>
Finished = False
countItem = 1
page = 1

#=============================================================>
# Get this work started!!!!
# Start of getEnd function
while End == 0:
    try:
        # End get value and declare as variable
        # End = getEnd(page)
        End = 30
        # print("End: ",End)

    except Exception as e:
        print("getEnd function failed")
        End = 1
# begin 
while Finished == False:
    try:
        #This should be the base url you wanted to access.
        baseurl = 'http://openleis.com'
        # path = '/legal_entities.csv'
        # sample = http://openleis.com/legal_entities/search/page/1.json
        pathJSON = '/legal_entities/search/page/' + str(page) + '.json'
        urlData = urllib.request.urlopen(baseurl + pathJSON)
        data = urlData.read()
        extractedContent = json.loads(data)
        print(extractedContent)
        # encoding = urlData.info().get_content_charset('utf-8')
        # decoding = data.decode(encoding)
        # Finished = True

        # df = pd.DataFrame([extractedContent])
        # def dict_to_df

    except Exception as e:
        print(str(e))
    
    # print(df.head())
    my_df = pd.DataFrame.from_dict(json_normalize(extractedContent),orient='columns')
    my_df.rename(columns=lambda x: x.replace('.', ''), inplace=True)

    # Function call and iterate up
    write_df_to_mongoDB(my_df)
    lastPage = page
    print("last page completed:",lastPage)
    # page End check to see if we should continue
    if page > End:
        print('Data.gov scrape complete.')
        Finished = True
        exit
    else: 
        page = page + 1
        Finished = False


# Call dataFrame to MongoDB formula
# WORKFLOW

print("Script Finished Running")
print("Last ditch fail catch")
Finished = True




# 'http://openleis.com/legal_entities.json'