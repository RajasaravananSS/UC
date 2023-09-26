from requests.auth import HTTPBasicAuth
import requests
import urllib3
import os


def RestartOtherServices():

	with open('CREDPATH',"r") as lgn:
		usrlgn = lgn.read().splitlines() 
		MYUSERNAME=usrlgn[0]
		MYPASSWORD=usrlgn[1]
		lgn.close()
	
	
	#k = 1
	j = 1

	WSDL_FILE = 'WSDLPATH'

	urllib3.disable_warnings( urllib3.exceptions.InsecureRequestWarning )

	session = requests.Session()
	session.auth = HTTPBasicAuth( MYUSERNAME,MYPASSWORD )

	session.verify = False
	with open('CMLIST',"r") as inp:
		ccmip = inp.read().split('\n')
	

		for ipadd in ccmip:

			fnamebfreboot = 'cucm' + str(j)
			print(fnamebfreboot)
			
			

			url = f'https://{ipadd}:8443/controlcenterservice2/services/ControlCenterServices'

			

			
			payload = "<soapenv:Envelope xmlns:soapenv=\"http://schemas.xmlsoap.org/soap/envelope/\" xmlns:soap=\"http://schemas.cisco.com/ast/soap\">\r\n    <soapenv:Header/>\r\n  <soapenv:Body>\r\n <soap:soapDoControlServices>\r\n <soap:ControlServiceRequest>\r\n	<soap:NodeName>{ipadd}</soap:NodeName>\r\n	<soap:ControlType>Restart</soap:ControlType>\r\n  <soap:ServiceList>\r\n   		<soap:item>Cisco DRF Local</soap:item>\r\n 		</soap:ServiceList>\r\n 	</soap:ControlServiceRequest>\r\n		</soap:soapDoControlServices>\r\n		</soapenv:Body>\r\n		</soapenv:Envelope>"
			headers = {
				'SOAPAction': 'soapDoControlServices',
				'Content-Type': 'text/plain'
			}
			try:

				response = requests.request("POST", url, auth=HTTPBasicAuth(MYUSERNAME,MYPASSWORD), headers=headers, data=payload, verify=False)

				with open('SUCCESSLISTTXTFILEPATH', 'a') as fnd:
					fnd.write(ipadd)
					fnd.write(response.text)
					fnd.close()

			except Fault as err:
				with open('FAILEDLISTTXTFILEPATH', 'a') as fnd:
					fnd.write(ipadd)
					fnd.write(response.text)
					fnd.close()
				continue
			j=j+1

RestartOtherServices()
			
