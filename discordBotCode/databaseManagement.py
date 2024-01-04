from pymongo.server_api import ServerApi
from pymongo.mongo_client import MongoClient

class Ping():
    name =  None
    count = 1



# Connects to the Mongo database
def getCollection(uri, name):
    client = MongoClient(uri, server_api = ServerApi("1"))
    db = client["HHGInfo"]
    collection = db[name]

    return collection

# Inserts document into Mongo Database appropriately
def create_document(collection, ping):
    new_ping = {
        "name": ping.name,
        "count":ping.count
    }
    return collection.insert_one(new_ping)

def update_document(collection, ping):
    filter_criteria = {"name":ping.name}
    update_data = {"$set":{"count":ping.count+1}}
    collection.update_one(filter_criteria, update_data) 

def checkForUser(collection, name):
    filter_criteria = {"name":name}
    document = collection.find_one(filter_criteria)

    if document:
        return(document["count"])
    else:
        return 0

def insertOrUpdateUserCollection(collection, name):

    query = checkForUser(collection, name)
    if(query > 0):
        ping = Ping()
        ping.name = name
        ping.count = query
        update_document(collection,ping)
    else:
        ping = Ping()
        ping.name = name
        create_document(collection,ping)

def print_collection(collection):
    
    cursor = collection.find()
    rows = []
    for document in cursor:
        print(document)
        rows.append(document)

    return rows

# def main():
#     # set database to access
#     database = r"C:\Users\bkowa\Documents\Python Code\OhioBot\discordBotCode\csgamerpings.db"
#     conn = create_connection(database)
        


# if __name__ == '__main__':
#     main()
