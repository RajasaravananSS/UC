from zeep import Client
import requests
from requests.auth import HTTPBasicAuth
from zeep import Client, Settings, Plugin, xsd
from zeep.transports import Transport
from zeep.exceptions import Fault
import sys
import urllib3



DEBUG = False

	
WSDL_FILE = 'WSDLPATH'

	
session = requests.Session()


session.verify = False
urllib3.disable_warnings( urllib3.exceptions.InsecureRequestWarning )



with open("CREDPATH","r") as f:
	mylist = f.read().splitlines() 
	USERNAME=mylist[0]
	PASSWORD=mylist[1]
	ccmip=mylist[2]
	f.close()

# Add Basic Auth credentials
session.auth = HTTPBasicAuth( USERNAME,PASSWORD )

#print (session.auth)

# Create a Zeep transport and set a reasonable timeout value
transport = Transport( session = session, timeout = 10 )

# strict=False is not always necessary, but it allows zeep to parse imperfect XML
settings = Settings( strict = False, xml_huge_tree = True )

# Create the Zeep client with the specified settings
client = Client( WSDL_FILE, settings = settings, transport = transport )

service = client.create_service( '{http://www.cisco.com/AXLAPIService/}AXLAPIBinding',f'https://{ccmip}:8443/axl/' )


deviceCSS = 'NEW_CSS'

	


#Open the txt file and read the MAC Address
with open("MACADDRESSLISTPATH","r") as m:
	listmac = m.read().splitlines()
	for mymac in listmac:
		
		try:
		
			udevname = mymac
			result = (service.updatePhone( name = udevname,callingSearchSpaceName = deviceCSS ))
			#print(result)
				
		except:
			print("Entering Exception")
			with open("FAILEDMACADDRESSLISTPATH","a") as fm:
				fm.write(mymac)
				fm.write('\n')


	