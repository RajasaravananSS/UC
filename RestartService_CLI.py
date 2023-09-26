import paramiko,socket
import time


j = 1
with open('CMLISTPATH',"r") as inp:
	ccmip = inp.read().split('\n')
	

	for ipadd in ccmip:

		fnamebfreboot = 'cucm' + str(j)
		print(fnamebfreboot)
		try:
			username = "yourusername"
			password = "yourplatformpassword"
            #you can retrieve these from a different file or environment variable refer to my other scripts

			ssh_client = paramiko.SSHClient()
			ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
			ssh_client.connect(hostname=ipadd,username=username,password=password)

			print ("Successful connection", ipadd)

			remote_connection = ssh_client.invoke_shell()

			remote_connection.send('utils service restart Cisco Tomcat\n') # type: ignore
			time.sleep(90)
			print(remote_connection.recv(20000))
			
			remote_connection.send("exit\n") # type: ignore

		except( socket.error, paramiko.AuthenticationException):
			status = 'fail' 
			failedip = open('FAILEDCMLISTPATH', 'a')
			failedip.write(ipadd + '\n') 

		time.sleep(1)


		paramiko.SSHClient.close