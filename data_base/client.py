from pymongo import MongoClient

# base de datos local
db_client = MongoClient()

# dase de datos remota
"""
db_client = MongoClient(
            "mongodb+srv://pepe:pete@cluster0.un37mmp.mongodb.net/?retryWrites=true&w=majority").test"""

