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




with open("CREDPATH","r") as f:
	mylist = f.read().splitlines() 
	USERNAME=mylist[0]
	PASSWORD=mylist[1]
	ccmip=mylist[2]
	f.close()


DEBUG = False



WSDL_FILE = 'WSDLPATH'



url = f'https://{ccmip}:8443/axl/'
headers = {
  'SOAPAction': 'CUCM:DB ver=12.5 listLine'
	   }
#headers = {'content-type': 'text/xml'}
duuid = []
#Open the txt file and read the DN
with open("DNLISTPATH","r") as m:
	listeuline = m.read().splitlines()
	for myline in listeuline:
		try:
			print(myline)
			payload = "<soapenv:Envelope xmlns:soapenv=\"http://schemas.xmlsoap.org/soap/envelope/\" xmlns:ns=\"http://www.cisco.com/AXL/API/12.5\">\r\n   <soapenv:Header/>\r\n   <soapenv:Body>\r\n      <ns:listLine sequence=\"?\">\r\n         <searchCriteria>\r\n           \r\n            <pattern>{userline}</pattern>\r\n            \r\n         </searchCriteria>\r\n         <returnedTags>\r\n            <pattern></pattern>\r\n            <!--Optional:-->\r\n            <description></description>\r\n            <!--Optional:-->\r\n            <usage></usage>\r\n            <!--Optional:-->\r\n            <routePartitionName uuid=\"?\"></routePartitionName>\r\n\r\n            \r\n         </returnedTags>\r\n         \r\n      </ns:listLine>\r\n   </soapenv:Body>\r\n</soapenv:Envelope>"

			myresp = requests.request("POST",url,
					auth=HTTPBasicAuth( USERNAME,PASSWORD ),data = payload.format(userline=myline),
					verify = False
					)
			
			print(myresp)
			deviceCSS = 'NA_ZEROCALL_CSS'
			input_dict = xmltodict.parse(myresp.text)
			output_dict = json.loads(json.dumps(input_dict))
			
			
			linedump = output_dict['soapenv:Envelope']['soapenv:Body']['ns:listLineResponse']['return']['line']
			print(linedump)
			lenld = len(linedump)
			if (lenld == 5):
				myuuid = output_dict['soapenv:Envelope']['soapenv:Body']['ns:listLineResponse']['return']['line']['@uuid']
				print(myuuid)
			else:
				
				for myline in linedump:
					usrlines = myline['pattern']
					myuuid = myline['@uuid']
					duuid.append(myuuid)
					print(usrlines)
					print(myuuid)
		

			for euuid in duuid:

				try:
				#with client.settings(raw_response=True):
					userdn = myline
					result = (service.updateLine( uuid = euuid,shareLineAppearanceCssName = deviceCSS ))

					#print(result)
						
				except:
					print("Entering Exception2")
					with open("FAILEDDNPATH","a") as fm:
						fm.write(myline)
						fm.write('\n')
		except:
			print("Entering Exception1")
			with open("FAILEDDNPATH","a") as fm:
				fm.write(myline)
				fm.write('\n')
			

