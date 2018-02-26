"""
Manage Azure VM for AI and Deep Learning tools
"""

import os
import json
import traceback

from azure.common.credentials import ServicePrincipalCredentials
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.compute import ComputeManagementClient

from haikunator import Haikunator

from prompt_toolkit import prompt

from utils import *
from manageresource import *
from managevm import *

"""
AZURE_TENANT_ID: your Azure Active Directory tenant id or domain
AZURE_CLIENT_ID: your Azure Active Directory Application Client ID
AZURE_CLIENT_SECRET: your Azure Active Directory Application Secret
AZURE_SUBSCRIPTION_ID: your Azure Subscription Id
"""

CLIENT_ID = 0 # application ID
TENANT_ID = 0
CLIENT_SECRET = 0
SUBSCRIPTION_ID = 0

WEST_US = 'westus'

def run():
	credentials, subscription_id = get_credentials()
	resource_client = ResourceManagementClient(credentials, subscription_id)
	compute_client = ComputeManagementClient(credentials, subscription_id)
	network_client = NetworkManagementClient(credentials, subscription_id)


def get_credentials():
	SUBSCRIPTION_ID = prompt('Enter your Subscription ID: ')
	TENANT_ID = prompt('Enter your Tenant ID: ')
	CLIENT_ID = prompt('Enter your Client/Service Principal Application ID: ')
	CLIENT_SECRET = prompt('Enter your Service Principal password: ')

	credentials = ServicePrincipalCredentials(
		client_id=CLIENT_ID,
		secret=CLIENT_SECRET,
		tenant=TENANT_ID
	)
	return credentials, SUBSCRIPTION_ID

if __name__ == '__main__':
	run()


	# answer = prompt('Give me some input: ')
	# print('You said: %s' % answer)