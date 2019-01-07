import pandas as pd
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
from dotenv import load_dotenv
dotenv_path = join(dirname(__file__),'../.env')
load_dotenv(dotenv_path)

# data.gov details committed to variables
username=os.getenv('dGovUsername')
password=os.getenv('dGovPassword')

#======================================================>

#=========================MongoDB=========================>
import pymongo

#bulk upload
def write_df_to_mongoDB(
    my_df,\
    database_name = 'OpenLeisJSON',\
    collection_name = 'leisJSON',\
    server = 'localhost',\
    mongodb_port = 27017,\
    chunk_size = 100):
    client = pymongo.MongoClient('localhost',int(mongodb_port))
    db = client[database_name]
    collection = db[collection_name]
    # To write
    collection.delete_many({})  # Destroy the collection
    #aux_df=aux_df.drop_duplicates(subset=None, keep='last') # To avoid repetitions
    my_list = my_df.to_dict('records')
    l =  len(my_list)
    ran = range(l)
    steps=ran[chunk_size::chunk_size]
    steps.extend([l])

    # Inser chunks of the dataframe
    i = 0
    for j in steps:
        print(j)
        collection.insert_many(my_list[i:j]) # fill de collection
        i = j

    print('Done')
    return

#DISCARDED MONGODB WORKFLOW
# try: 
#     myclient = pymongo.MongoClient("mongodb://localhost:27017/")
# except pymongo.errors.ConnectionsFailure as e:
#     print(e)

# mydb = myclient["openLeisJSON"]
# mydb.drop_collection("leisJSON")
# mycol = mydb["leisJSON"]

# mycol.create_index("_id")



#==========================================================>

#This should be the base url you wanted to access.
baseurl = 'http://openleis.com'
path = '/legal_entities.csv'
pathJSON = '/legal_entities.json'
# page 1 sample
# http://openleis.com/legal_entities.json
# http://openleis.com/legal_entities/search/page/1.json
# page 2 sample
# http://openleis.com/legal_entities/search/page/2.json
# r = requests.get(baseurl + path, auth=(username,password))

#=====================variables==========================>
Finished = False
countItem = 1
#=============================================================>

while Finished == False:

    try:
        urlData = urllib.request.urlopen(baseurl + pathJSON)
        data = urlData.read()
        extractedContent = json.loads(data)
        # encoding = urlData.info().get_content_charset('utf-8')
        # decoding = data.decode(encoding)
        Finished = True

        # df = pd.DataFrame([extractedContent])
        # def dict_to_df

    except Exception as e:
        print(str(e))
    
    # print(df.head())
my_df = pd.DataFrame.from_dict(json_normalize(extractedContent),orient='columns')

# for item in extractedContent:
#     print(item)
#     print(countItem)
#     countItem + 1
print(my_df.head())
print("Finished Running")



# 'http://openleis.com/legal_entities.json'