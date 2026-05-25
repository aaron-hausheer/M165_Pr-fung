from pymongo import MongoClient


class MongoDatabase:
    def __init__(self, uri="mongodb://localhost:27017", database_name="pruefung_db"):
        self.uri = uri
        self.database_name = database_name
        self.client = None
        self.database = None

    def connect(self):
        self.client = MongoClient(self.uri, serverSelectionTimeoutMS=3000)
        self.client.admin.command("ping")
        self.database = self.client[self.database_name]
        return self.database

    def close(self):
        if self.client is not None:
            self.client.close()
            self.client = None
            self.database = None

