#!/usr/bin/env python

from pyVim import connect
from pyVmomi import vim
from tools import pchelper

import MySQLdb
import atexit

vm_properties = ['name', 'runtime.powerState']

#connection to VMware vCenter server
service_instance = connect.SmartConnect (host='XX.XX.XX.XX', user="XXXXXXX", pwd='XXXXXX',port=443)

atexit.register (connect.Disconnect, service_instance)

view = pchelper.get_container_view(service_instance, obj_type=[vim.VirtualMachine])

vm_data=pchelper.collect_properties(service_instance, view_ref = view, obj_type = vim.VirtualMachine, path_set = vm_properties, include_mors=True)
list_vmware=[]
list_vmware=[(vm["name"], vm["runtime.powerState"]) for vm in vm_data]

#connection to CloudStack database
db=MySQLdb.connect(host='ZZ.ZZ.ZZ.ZZ',user='ZZZZZ',passwd='ZZZZZZZZZ',db='cloud')

cur=db.cursor()
cur.execute ('select instance_name, state from vm_instance;')
list_cs=cur.fetchall()

for csvm_name, csvm_state in list_cs:
	for vmware_name, vmware_state in list_vmware:
		if (csvm_state == 'Expunging') and (csvm_name == vmware_name):
			print vmware_name, vmware_state
