# Import Azure Resource Graph library
import azure.mgmt.resourcegraph as arg

# Import specific methods and models from other libraries
from azure.mgmt.resource import SubscriptionClient
from azure.identity import AzureCliCredential

# Wrap all the work in a function
def getresources( strQuery ):
    # Get your credentials from Azure CLI (development only!) and get your subscription list
    credential = AzureCliCredential()
    subsClient = SubscriptionClient(credential)
    subsRaw = []
    for sub in subsClient.subscriptions.list():
        subsRaw.append(sub.as_dict())
    subsList = []
    for sub in subsRaw:
        subsList.append(sub.get('subscription_id'))

    # Create Azure Resource Graph client and set options
    argClient = arg.ResourceGraphClient(credential)
    argQueryOptions = arg.models.QueryRequestOptions(result_format="objectArray")

    # Create query
    argQuery = arg.models.QueryRequest(subscriptions=subsList, query=strQuery, options=argQueryOptions)

    # Run query
    argResults = argClient.resources(argQuery)

    # Show Python object
    print(argResults)

# getresources("Resources | project name, type | limit 5 | order by name asc")

getresources("Resources | where type =~ 'Microsoft.Storage/storageAccounts' | where tags['ucid']=='DAaaS_Shared' | project name")