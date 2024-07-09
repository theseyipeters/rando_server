from pymongo import MongoClient
from urllib.parse import quote_plus

username = "theseyipeters"
password = "sagethedev"
cluster_url = "randocluster.mh8gfs3.mongodb.net"
dbname = "randoDB"

encoded_username = quote_plus(username)
encoded_password = quote_plus(password)

# print(encoded_username, encoded_password)
# mongo_uri = f'mongodb+srv://{username}:{password}@{cluster_url}/{dbname}?retryWrites=true&w=majority/'


mongo_uri = 'mongodb+srv://randocluster.mh8gfs3.mongodb.net/?retryWrites=true&w=majority&appName=randoCluster'

print(mongo_uri)

try:
    client = MongoClient(mongo_uri)
    db = client[dbname]
    db.command("ping")
    print("Connection to MongoDB successful")
except Exception as e:
    print(f"Connection failed: {e}")
