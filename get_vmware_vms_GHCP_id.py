#!/usr/bin/env python

from pyVim import connect
from pyVmomi import vim
from tools import pchelper

import atexit
import sys
import MySQLdb

account_id= sys.argv[1]

vm_properties = ['name', 'runtime.powerState']

#connection to VMware vCenter server
service_instance = connect.SmartConnect (host='XX.XX.XX.XX', user="XXXXXXXX", pwd='XXXXXXXX',port=443)

atexit.register (connect.Disconnect, service_instance)

view = pchelper.get_container_view(service_instance, obj_type=[vim.VirtualMachine])

vm_data=pchelper.collect_properties(service_instance, view_ref = view, obj_type = vim.VirtualMachine, path_set = vm_properties, include_mors=True)
list_vmware=[]
list_vmware=[(vm["name"], vm["runtime.powerState"]) for vm in vm_data]

#connection to CloudStack database
db=MySQLdb.connect(host='ZZ.ZZ.ZZ.ZZ',user='ZZZZZZ',passwd='ZZZZZZZ',db='cloud')
cur=db.cursor()
cur.execute("select id from account where account_name like %s", ("%"+account_id))
query_result = cur.fetchone()
cs_account_id = str(query_result[0])

for vmware_name, vmware_state in list_vmware:
	if 'i-'+cs_account_id in vmware_name:
		print vmware_name, vmware_state
