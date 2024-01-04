from pymongo.server_api import ServerApi
from pymongo.mongo_client import MongoClient

uri = ""

client = MongoClient(uri, server_api = ServerApi("1"))
db = client["HHGInfo"]
collection = db["pings"]


cursor = collection.find()

for document in cursor:
    print(document)

client.close()
