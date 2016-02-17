# pyvmomi_scripts
Scripts based on pyvmomi + CloudStack related things

get_orphanvms.py - scripts gets list of VMs from Vmware and CloudStack databases. After that tries to find VMs which have 'Expanging' status in CloudStack and in same time still persist in VMware

get_vmware_vms_GHCP_id.py - search all VMs directly in VMware which are related to specific account ID from CloudStack. Usage:

./get_vmware_vms_GHCP_id.py PRODUCT_ID 
