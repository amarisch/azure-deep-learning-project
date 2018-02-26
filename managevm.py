

VM_REFERENCE = {
    'linux': {
        'publisher': 'Canonical',
        'offer': 'UbuntuServer',
        'sku': '16.04.0-LTS',
        'version': 'latest'
    },
    'windows': {
        'publisher': 'MicrosoftWindowsServerEssentials',
        'offer': 'WindowsServerEssentials',
        'sku': 'WindowsServerEssentials',
        'version': 'latest'
    }
}


def create_linux_vm(network_client, compute_client, group_name, vm_name='myvm', username='user', pw='user', location='westus'):

	# create a NIC
	nic = create_nic(network_client)

	# Create Linux VM
	print('\nCreating Linux Virtual Machine')
	vm_parameters = create_vm_parameters(nic.id, VM_REFERENCE['linux'], vm_name, username, pw, location)
	async_vm_creation = compute_client.virtual_machines.create_or_update(
		group_name, vm_name, vm_parameters)
	async_vm_creation.wait()

def deallocate_vm(compute_client, group_name, vm_name):
	# Deallocating the VM
	print('\nDeallocating the VM')
	async_vm_deallocate = compute_client.virtual_machines.deallocate(group_name, vm_name)
	async_vm_deallocate.wait()

def start_vm(compute_client, group_name, vm_name):
	# Start the VM
	print('\nStart VM')
	async_vm_start = compute_client.virtual_machines.start(group_name, vm_name)
	async_vm_start.wait()

def restart_vm(compute_client, group_name, vm_name):
	# Start the VM
	print('\nRestart VM')
	async_vm_restart = compute_client.virtual_machines.restart(group_name, vm_name)
	async_vm_restart.wait()	

def stop_vm(compute_client, group_name, vm_name):
	# Stop the VM
	print('\nStop VM')
	async_vm_stop = compute_client.virtual_machines.power_off(group_name, vm_name)
	async_vm_stop.wait()

def delete_vm(compute_client, group_name, vm_name):
	# Delete VM
	print('\nDelete VM')
	async_vm_delete = compute_client.virtual_machines.delete(group_name, vm_name)
	async_vm_delete.wait()

def list_vm_in_subscription(compute_client):
	# List VMs in subscription
	print('\nList VMs in subscription')
	for vm in compute_client.virtual_machines.list_all():
		print("\tVM: {}".format(vm.name))

def list_vm_in_resource_group(compute_client, group_name):
	print('\nList VMs in resource group')
	for vm in compute_client.virtual_machines.list(group_name):
		print("\tVM: {}".format(vm.name))		

def create_nic(network_client, group_name, vnet_name='myvnet', subnet_name='mysubnet', \
				nic_name='mynic', ip_config_name='myipconfig', location='westus'):
    """Create a Network Interface for a VM.
    """
    # Create VNet
    print('\nCreate Vnet')
    async_vnet_creation = network_client.virtual_networks.create_or_update(
        group_name,
        vnet_name,
        {
            'location': location,
            'address_space': {
                'address_prefixes': ['10.0.0.0/16']
            }
        }
    )
    async_vnet_creation.wait()

    # Create Subnet
    print('\nCreate Subnet')
    async_subnet_creation = network_client.subnets.create_or_update(
        group_name,
        vnet_name,
        subnet_name,
        {'address_prefix': '10.0.0.0/24'}
    )
    subnet_info = async_subnet_creation.result()

    # Create NIC
    print('\nCreate NIC')
    async_nic_creation = network_client.network_interfaces.create_or_update(
        group_name,
        nic_name,
        {
            'location': location,
            'ip_configurations': [{
                'name': ip_config_name,
                'subnet': {
                    'id': subnet_info.id
                }
            }]
        }
    )
    return async_nic_creation.result()

def create_vm_parameters(nic_id, vm_reference, vm_name, username, pw, location):
	"""Create the VM parameters structure.
	"""
	return {
	'location': location,
	'os_profile': {
		'computer_name': vm_name,
		'admin_username': username,
		'admin_password': pw
	},
	'hardware_profile': {
		'vm_size': 'Standard_DS1_v2'
	},
	'storage_profile': {
		'image_reference': {
			'publisher': vm_reference['publisher'],
			'offer': vm_reference['offer'],
			'sku': vm_reference['sku'],
			'version': vm_reference['version']
	    },
	},
	'network_profile': {
		'network_interfaces': [{
			'id': nic_id,
		}]
	},
	}