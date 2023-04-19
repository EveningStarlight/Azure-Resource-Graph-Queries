# Import specific methods and models from other libraries
from azure.identity import AzureCliCredential

import os, uuid
from datetime import datetime
from azure.storage.blob import BlobServiceClient, ContainerClient

def main():
    print("Starting Script" + '\n')
    containerDic = {}
    for storageAccount in StorageAccount.list:
        containerDic[storageAccount] = StorageAccount.getContainers(storageAccount, True)
    writeCSV(containerDic)
    print('Script Complete' + '\n')

def writeCSV(dic):
    f = open("data/" + datetime.today().strftime('%Y-%m-%d') + ".csv", "x")
    for storageAccount in dic.keys():
        f.write(storageAccount + ', , ,\n')
        for container in dic[storageAccount].values():
            f.write(container.toCSV())
    f.close()

class StorageAccount:
    list = ['stpdmfdidun01sa']
    #list = ['stndmfdidpb01sa', 'stndmfdidun01sa', 'stndmfdiipb01sa', 'stndmfdiiun01sa', 'stndmfdisto01sa', 'stpdmfdidpb01sa', 'stpdmfdidun01sa', 'stpdmfdiipb01sa', 'stpdmfdiiun01sa', 'stpdmfdisto01sa']

    def getContainers(storageAccount, verbose=False):
        try:
            print("Begin itterating over: " + storageAccount + '\n')

            account_url = "https://" + storageAccount + ".blob.core.windows.net"
            credential = AzureCliCredential()

            # Create the BlobServiceClient object
            blob_service_client = BlobServiceClient(account_url, credential=credential)

            containerList = blob_service_client.list_containers()
            containerObjs = {}

            for container in containerList:
                try:
                    containerObj = Container(account_url, container.name, credential, storageAccount)
                    containerObjs[container.name] = containerObj
                    if verbose:
                        print(containerObj)
                except Exception as ex:
                    print('Exception:' + '\n' + str(ex) + '\n')
            return containerObjs

        except Exception as ex:
            print('Exception:' + '\n' + str(ex) + '\n')

class Container:
    def __init__(self, account_url, name, credential, storageAccount):
        container_client = ContainerClient(account_url, name, credential)
        properties = container_client.get_container_properties()

        count = 0
        size = 0
        for blob in container_client.list_blobs():
            count += 1
            size += blob['size']

        self.storageAccount = storageAccount
        self.name = properties.name
        self.ucid = properties.metadata["ucid"]
        self.count = count
        self.size = size

    def toCSV(self):
        return ', ' + self.name + ', ' + self.ucid + ', ' + str(self.size) + '\n'

    def __str__(self):
        string = "Container Name: " + self.name + "\n"
        string = string + "UCID: " + self.ucid + "\n"
        string = string + "File Count: " + str(self.count) + "\n"
        string = string + "Total Size: " + str(self.size) + "\n"

        return string
        
    

if __name__ == "__main__":
    main()