import argparse
import time
import subprocess
import sys
import re
import os


vm_list = ['vm11', 'vm12', 'vm21', 'vm22', 'vm23', 'vm24', 'vm31', 'vm32', 'vm41', 'vm42', 'vm51', 'vm52', 'vm61', 'vm62', 'vm63', 'vm64']
pt_list = [2201, 2202, 2203, 2204, 2205, 2206, 2207, 2208, 2209, 2210, 2211, 2212, 2214, 2215, 2216, 2217]
vmdict = dict(zip(vm_list,pt_list))
FNULL = open(os.devnull, 'w')

def startvm(vmlist, timeout):
	for vm in vmlist:
		subprocess.call("sudo -u user{} VBoxManage startvm {} --type headless".format(int(vm[2]),vm),shell=True, stderr=subprocess.STDOUT, stdout=FNULL)
		print("\033[1;32m[+]\033[0;37m Starting \033[1;32m{}\033[0m\033[0;37m on \033[1;32muser{}\033[0m".format(vm,int(vm[2])))
		if vmlist != []:
			time.sleep(timeout)

def stopvm(vmlist):
	for vm in vmlist:
		subprocess.call("sudo -u user{} VBoxManage contolvm {} acpipowerbutton".format(int(vm[2]),vm),shell=True, stderr=subprocess.STDOUT, stdout=FNULL)
		print("\033[1;31m[~]\033[0;37m Stopping VM \033[1;37m{}\033[0m\033[0;37m on \033[1;37muser{}\033[0m".format(vm,int(vm[2])))
		if vmlist != []:
			time.sleep(0.25)

def getstats(vmlist):
	for vm in vmlist:
		output = subprocess.check_output("nmap -p {} localhost --host-timeout=1".format(vmdict[vm]), shell=True, stderr=subprocess.STDOUT)
		data = re.findall(r'{}\/tcp\s+(\w+)'.format(vmdict[vm]),output)
		if "0 hosts up" in output:
			print("\033[1;31m[-]\033[0m\033[1;31m {}\033[0;37m Offline\033[0m".format(vm))
		else:
			if data[0] == "open":
				print("\033[1;32m[+]\033[0m\033[1;32m {}\033[0;37m Active, SSH on port \033[1;32m{}\033[0m".format(vm, vmdict[vm]))
			if data[0] == "closed":
				print("\033[1;31m[-]\033[0m\033[1;31m {}\033[0;37m Active, SSH port closed\033[0m".format(vm))
			

def showgui(vmlist):
	for vm in vmlist:
		print("\033[1;33m[~]\033[1;37m Trying to get GUI for VM \033[1;33m{}\033[0m".format(vm))
		subprocess.call("sudo -u user{} VBoxManage startvm {} --type separate".format(int(vm[2]),vm),shell=True, stderr=subprocess.STDOUT, stdout=FNULL)
		if vmlist != []:
			time.sleep(2)

def main():
	usage = '''
	Example:
	
	Start Virtual Machine[s]
		python vmanager.py -v [all | vm11 | vm11 vm12 vm21]

	Stop Virtual Machine[s]
		python vmanager.py -x [all | vm11 | vm11 vm12 vm21]

	Get Stats
		python vmanager.py -stat [all | vm11 | vm11 vm12 vm21]

	Show Virtual Machine in GUI Mode
		python vmanager.py -show [all | vm11 | vm11 vm12 vm21]
	'''

	parser = argparse.ArgumentParser(description="Virtual Box Script", epilog=usage, formatter_class=argparse.RawDescriptionHelpFormatter)
	parser.add_argument("-v", help="VM[s] to be Started, OPTIONS [all, virtual machine names separated by space]", type=str, nargs="*", action="store")
	parser.add_argument("-x", help="VM[s] to be Stopped, OPTIONS [all, virtual machine names separated by space]", type=str, nargs="*", action="store")
	parser.add_argument("-stat", help="Get status of VM[s], OPTIONS [all, virtual machine names separated by space]", type=str, nargs="*", action="store")
	parser.add_argument("-show", help="Show GUI for VM[s], OPTIONS [all, virtual machine names separated by space]", type=str, nargs="*", action="store")
	parser.add_argument("--timeout", help="Timeout", type=float, default=30)
	args = parser.parse_args()

	vms = args.v
	vmx = args.x
	timeout = args.timeout
	statcheck = args.stat
	showvms = args.show

	if statcheck:
		if statcheck[0] == "all":
			getstats(vm_list)
		else:
			getstats(statcheck)
	if vms:
		if vms[0] == "all":
			startvm(vm_list, timeout)
		else:
			startvm(vms, timeout)
	if vmx:
		if vmx[0] == "all":
			stopvm(vm_list)
		else:
			stopvm(vmx)
	if showvms:
		if showvms[0] == "all":
			showgui(vm_list)
		else:
			showgui(showvms)
		

main()
