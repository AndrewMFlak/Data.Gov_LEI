import csv
import urllib2
import sys
import re
import base64
from urlparse import urlparse
import pandas as pd
import io


#==================ENV processing=============================>
import os
from os.path import join, dirname
from dotenv import load_dotenv
dotenv_path = join(dirname(__file__),'.env')
load_dotenv(dotenv_path)




# url path to open leis site
url = 'http://openleis.com/legal_entities.csv'


# data.gov details committed to variables
username=os.getenv('dGovUsername')
password=os.getenv('dGovPassword')


req = urllib2.Request(url)
try:
    handle = urllib2.urlopen(req)
except IOError as e:
        #here we want to fail
    pass
else:
    #if we don't fail then the page isn't protected
    print("This page is not protected by Authentication")
    sys.exit(1)

if not hasattr(e, 'code') or e.code != 401:
    # we got an error - but not a 401 error
    print("This page isn't protected by authentication.")
    print("But we failed for some other reason")
    sys.exit(1)

authline = e.headers['www-authenticate']
# this gerts the www-authenticate line from the headers
# which has the authentication scheme and realm in it

authobj = re.compile(
        r'''(?:\s*www-authenticate\s*:)?\s*(\w*)\s+realm=['"]([^'"]+)['"]''',re.IGNORECASE)
    # this regular expression is used to extract scheme and realm
matchobj = authobj.match(authline)


if not matchobj:
    # if the authline isn't matched by the regular expression
    # then something is wrong
    print('The authentication header is badly formed.')
    print(authline)
    sys.exit(1)

scheme = matchobj.group(1)
realm = matchobj.group(2)
# here we've extracted the scheme
# and the realm from the header
if scheme.lower() != 'basic':
    print('This example only works with BASIC authentication.')
    sys.exit(1)

base64string = base64.encodestring(
                '%s:%s' % (username, password))[:-1]
authheader =  "Basic %s" % base64string
req.add_header("Authorization", authheader)
try:
    handle = urllib2.urlopen(req)
except IOError as e:
    # here we shouldn't fail if the username/password is right
    print("It looks like the username or password is wrong.")
    sys.exit(1)
thepage = handle.read()

# urlData = urllib.request.get(url).content
# rawData = pd.read_csv(io.StringIO(urlData.decode('utf-8')))
# print(rawData)



#csv file extension
# path = '/legal_entities.csv'
# data = pd.read_csv(url)
# response = getThatShit.urlopen(url , path)
    # html = response.read()
# try:
#     data = pd.read_csv(url)
#     print("pandas csv succss")
# except:
#     print("error accessing csv")

# for row in cr:
#     print(row)


