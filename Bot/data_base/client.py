from pymongo import MongoClient

# base de datos local
#db_client = MongoClient()

# dase de datos remota
db_client = MongoClient(
            "mongodb+srv://victorinoedr:Elbesto@cluster0.mgupgk9.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0").test

