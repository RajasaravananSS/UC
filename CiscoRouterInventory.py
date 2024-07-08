import netmiko
from netmiko import ConnectHandler
from netmiko import ConnectionException
import time
with open('path/filename.txt',"r") as cred:
	usrcred = cred.read().split('\n')
	userid = usrcred[0]
	passc = usrcred[1]
"""or you can have IP,username and password in one line and split it like this
with open('path/filename.txt',"r") as cred:
		for mycred in cred:
			print(mycred)
			usrcred = mycred.split(',')
			host = usrcred[0]
			user = usrcred[1]
      gwip = usrcred[2]
you can also skip the fetching IP part if you use the above method"""
#verify if it fetching the correct credentials you can remove this print statement later
#print(userid)
#print(passc)

#open the text file to read the list of IP Address
with open('path/filename.txt',"r") as inp:
	gwip = inp.read().split('\n')
	

	
#cfg_file  = '/path/filename.txt'
	

for ipadd in gwip:
	print(ipadd)
	try:

		#verify if it fetching the correct credentials you can remove this print statement later
		#print(ipadd)
		#The below inout can be changed for multiple vendor products by modifying device type refer to Netmiko notes
		cisco_ios = {
		'device_type': 'cisco_ios',
		'host': ipadd,
		'username': userid,
		'password': passc,
		}
		# Creates the connection to the device.
		net_connect = ConnectHandler(**cisco_ios)
		net_connect.banner_timeout=60
		time.sleep(15)
		hostname = net_connect.send_command("show conf | i hostname")
		print(hostname)
		hostname = hostname.split()
		hostname = hostname[1]
		
		rmodel = net_connect.send_command("sh inv | inc PID:")
		rmodel = rmodel.split()
		rmodel = rmodel[1]
		if ('8200' in str(rmodel)):
			rios = net_connect.send_command("sh ver | inc Cisco IOS XE Software, Version")
			rios = rios.split(',')
			rios = rios[1]
		else:
			rios = net_connect.send_command("sh ver | inc System image file")
			rios = rios.split()
			rios = rios[4]

		rser = net_connect.send_command("sh ver | in Processor board ID")
		rser = rser.split()
		rser = rser[3]
		aspacestr = net_connect.send_command("dir | inc bytes total")
		aspacestr = aspacestr.split(' ')
		#hostname = str(hostname).split('(')
		aspacestr = aspacestr[3].strip('(')
		aspace = (int(aspacestr)/1024)/1024
		
		
		# print the gathered data.
		with open('C:Path/filename.txt',"a") as inp:
			fstr =  str(hostname + "\t" + rios + "\t" + rmodel + "\t" + rser + "\t" + aspacestr)
			inp.write(str(fstr))
			inp.write("\t")
			inp.write(str(aspace))
			inp.write("\n")
	
	except  ConnectionException as err:
		print(err)
		with open('C:Path/filename.txt',"a") as inp:
			inp.write(str(ipadd))
			inp.write("\n")

	
	
	
