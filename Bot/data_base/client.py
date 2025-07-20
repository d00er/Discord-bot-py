from pymongo import MongoClient

# base de datos local
#db_client = MongoClient()

# dase de datos remota
db_client = MongoClient(
            "mongodb+srv://victorinoedr:p3X5pzSHIr3coSPP@cluster0.ialojuw.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0").test

