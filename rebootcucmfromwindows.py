import paramiko
from paramiko import ssh_exception
import time

def FormatOP(indata):
	
	myout = indata.splitlines('\r\n\r\n')
	for line in myout:
		myline = str(line)
		line1 = myline.replace("b","")
		line2 = myline.replace("\\r\\n'","").replace("\\t","")
		print(line2.strip('\n'))
		with open('C:/Users/PATH/outdata.txt',"a") as opdata:
			opdata.write(str(line2))
			opdata.write("\n")

def rebootserver():
	
	   	with open('C:PATH/login.txt',"r") as cred:
    		for mycred in cred:
    			print(mycred)
    			usrcred = mycred.split('\t')
    			host = usrcred[0]
    			user = usrcred[1]
    			#passw = usrcred[2]	
    			ssh = paramiko.SSHClient()
    			ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    			try:
    				print(host, user, passw)
    				ssh.connect(hostname=host, username=user, password=passw)
    				#shell = ssh.exec_command(command="show status",bufsize=10000,get_pty=True)
            #Used the above output from show status to test the output trim function FormatOP
    				shell = ssh.invoke_shell()
    				print('\n'+time.strftime("%m/%d/%Y %H:%M:%S"))
    				time.sleep(40)
    				shell.send("utils system restart\n")
    				time.sleep(3)
    				shell.send("y")
    				time.sleep(1)
    				shell.send("e")
    				time.sleep(1)
    				shell.send("s\n")
    				time.sleep(10)
    				print('\n'+time.strftime("%m/%d/%Y %H:%M:%S"))
    				buffer = shell.recv(10240)
    				myout = shell.recv(10240).decode('utf-8')
            myout = indata.splitlines('\r\n\r\n')
          	for line in myout:
          		myline = str(line)
          		line1 = myline.replace("b","")
          		line2 = myline.replace("\\r\\n'","").replace("\\t","")
          		print(line2.strip('\n'))
          		with open('C:/Users/PATH/outdata.txt',"a") as opdata:
          			opdata.write(str(line2))
          			opdata.write("\n")
    				
    				#Or you can use the function to trim output FormatOP(myout)
    
    			except ssh_exception as err:
    				print(err)



rebootserver()
