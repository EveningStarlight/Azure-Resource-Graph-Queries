# Import specific methods and models from other libraries
from azure.mgmt.resource import SubscriptionClient
from azure.identity import AzureCliCredential

import os, uuid
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

def main():
    print("Starting Script")
    print()
    StorageAccount.getContainers(StorageAccount.list[0], True)

class StorageAccount:
    list = ['stndmfdidpb01sa']

    def getContainers(storageAccount, verbose=False):
        try:
            print("Begin itterating over: " + storageAccount)
            print()

            account_url = "https://" + storageAccount + ".blob.core.windows.net"
            credential = AzureCliCredential()

            # Create the BlobServiceClient object
            blob_service_client = BlobServiceClient(account_url, credential=credential)

            containerList = blob_service_client.list_containers()

            for container in containerList:
                containerObj= Container(account_url, container.name, credential)
                if verbose:
                    print(containerObj)

            print('Run Successful')

        except Exception as ex:
            print('Exception:')
            print(ex)

class Container:
    def __init__(self, account_url, name, credential):
        container_client = ContainerClient(account_url, name, credential)
        properties = container_client.get_container_properties()
        blobs = container_client.list_blobs()
        totalSize = sum(blob['size'] for blob in blobs)

        self.name = properties.name
        self.ucid = properties.metadata["ucid"]
        self.size = totalSize

    def __str__(self):
        string = "Container Name: " + self.name + "\n"
        string = string + "UCID: " + self.ucid + "\n"
        string = string + "Total Size: " + str(self.size) + "\n"

        return string
    

if __name__ == "__main__":
    main()