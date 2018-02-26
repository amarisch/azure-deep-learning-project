from utils import *

def create_resource_group(client, groupname):
	print('Create Resource Group')
	resource_group_params = {'location':'westus'}
	print_item(client.resource_groups.create_or_update(groupname, resource_group_params))

# TODO
def update_resource_group(client, groupname):
	print('Update Resource Group')
	resource_group_params = {'location':'westus'}
	print_item(client.resource_groups.create_or_update(groupname, resource_group_params))

def delete_resource_group(client, groupdname):
    print('Delete Resource Group')
    delete_async_operation = client.resource_groups.delete(groupdname)
    delete_async_operation.wait()
    print("\nDeleted: {}".format(groupdname))

def print_group_resource(client, groupname):
	for item in client.resource_groups.list_resources(groupname):
		print_item(item)