import zeep
import requests
import urllib3
import xmltodict
from urllib3 import exceptions
from zeep import client
from zeep.transports import Transport
from zeep.settings import Settings
from requests import Session
from requests.auth import HTTPBasicAuth
from lxml import etree as ET
from zeep import helpers
import json



listoftpn = []

with open("credpath","r") as f:
	mylist = f.read().splitlines() 
	USERNAME=mylist[0]
	PASSWORD=mylist[1]
	ccmip=mylist[2]
	f.close()



DEBUG = False

WSDL_FILE = 'WSDLPATHAXLAPI.wsdl'

#URL for requests
url = f'https://{ccmip}:8443/axl/'

#Don't miss this HEADER Action otherwise we will get errors
headers = {
  'SOAPAction': 'CUCM:DB ver=12.5 listRoutePlan'
	   }
#headers = {'content-type': 'text/xml'}

payload = "<soapenv:Envelope xmlns:soapenv=\"http://schemas.xmlsoap.org/soap/envelope/\" xmlns:ns=\"http://www.cisco.com/AXL/API/12.5\">\r\n   <soapenv:Header/>\r\n   <soapenv:Body>\r\n      <ns:listRoutePlan sequence=\"?\">\r\n         <searchCriteria>\r\n           \r\n            <dnOrPattern>8155545%</dnOrPattern>\r\n            \r\n         </searchCriteria>\r\n         <returnedTags>\r\n            <dnOrPattern></dnOrPattern>\r\n           <description></description>\r\n            <!--Optional:-->\r\n            <usage></usage>\r\n            <!--Optional:-->\r\n            <routePartitionName uuid=\"?\"></routePartitionName>\r\n\r\n            \r\n         </returnedTags>\r\n         \r\n      </ns:listRoutePlan>\r\n   </soapenv:Body>\r\n</soapenv:Envelope>"

myresp = requests.request("POST",url,
		auth=HTTPBasicAuth( USERNAME,PASSWORD ),data = payload,
		verify = False
		)
#You can ignore this if you don't want to test output received
print(myresp)
input_dict = xmltodict.parse(myresp.text)
output_dict = json.loads(json.dumps(input_dict))
#You can ignore this if you don't want to test output received
print(output_dict)
freetpn = []
listofdesc = []
tpndump = output_dict['soapenv:Envelope']['soapenv:Body']['ns:listRoutePlanResponse']['return']['routePlan']
#You can ignore this if you don't want to test output receivedtdsdump = output_dict['soapenv:Envelope']['soapenv:Body']['ns:listRoutePlanResponse']['return']
print(tpndump)
#You can ignore this if you don't want to test output received
print(tdsdump)
for mytpn in tpndump:
	usrlines = mytpn['dnOrPattern']
	usrdesc = mytpn['description']
	listoftpn.append(usrlines)
	listofdesc.append(usrdesc)
print(listoftpn)

print(listofdesc)