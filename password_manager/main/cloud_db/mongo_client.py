from pymongo import MongoClient
from pymongo.server_api import ServerApi
from pymongo.errors import ConnectionFailure, OperationFailure
import os


class MongoDBClient:
    def __init__(self):
        self.host = os.getenv('MONGO_HOST', 'localhost')
        self.port = int(os.getenv('MONGO_PORT', '27017'))
        self.database = os.getenv('MONGO_DATABASE')
        self.username = os.getenv('MONGO_USER')
        self.password = os.getenv('MONGO_PASSWORD')
        self.is_local = os.getenv('IS_LOCAL', 'False').lower() == 'true'
        self.client = None
        self.db = None

    def __str__(self):
        return f"MongoDBClient(host={self.host}, port={self.port}, database={self.database}, username={self.username}, password={self.password})"

    def connect(self):
        try:
            if not self.client:
                if self.is_local:
                    self.client = MongoClient(
                        host=self.host,
                        port=self.port,
                        serverSelectionTimeoutMS=5000,
                        maxPoolSize=10  # Adjust the pool size based on your application needs
                    )
                else:
                    uri = "mongodb+srv://{}:{}@passwords.obc9lkx.mongodb.net/?retryWrites=true&w=majority".format(
                        self.username, self.password
                    )
                    self.client = MongoClient(uri, server_api=ServerApi('1'))
            self.db = self.client[self.database]
            print("Connected to MongoDB")
            try:
                self.client.admin.command('ping')
                print("Pinged your deployment. You successfully connected to MongoDB!")
            except Exception as e:
                print(e)

        except ConnectionFailure as e:
            print(f"Failed to connect to MongoDB: {e}")
            raise

    def disconnect(self):
        if self.client:
            print("Returned connection to MongoDB connection pool")

    def insert_document(self, collection, document):
        try:
            result = self.db[collection].insert_one(document)
            print(f"Document inserted with ID: {result.inserted_id}")

        except OperationFailure as e:
            print(f"Failed to insert document: {e}")
            raise

    def find_documents(self, collection, query=None):
        try:
            cursor = self.db[collection].find(query) if query else self.db[collection].find()
            documents = [doc for doc in cursor]
            return documents

        except OperationFailure as e:
            print(f"Failed to find documents: {e}")
            raise

    def set_record_deleted(self, collection, query, update_document):
        try:
            update_query = {"$set": update_document}
            self.db[collection].update_one(query, update_query, upsert=True)
            print(f"Document deleted with ID: {self.db[collection].find_one(query).get('_id')}")
        except OperationFailure as e:
            print(f"Failed to delete document: {e}")
            raise
