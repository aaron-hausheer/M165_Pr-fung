import os

from exceptions import DatabaseError


class MongoConnection:
    def __init__(self) -> None:
        self.uri = os.getenv("MONGO_URI", "mongodb://localhost:27017")
        self.database_name = os.getenv("MONGO_DB", "pruefung_db")
        self.client = None
        self.database = None

    def connect(self):
        try:
            from pymongo import MongoClient

            self.client = MongoClient(self.uri, serverSelectionTimeoutMS=3000)
            self.client.admin.command("ping")
            self.database = self.client[self.database_name]
            return self.database
        except Exception as exc:
            raise DatabaseError(
                "MongoDB-Verbindung fehlgeschlagen. Laeuft MongoDB und stimmt MONGO_URI?"
            ) from exc

    def close(self) -> None:
        if self.client is not None:
            self.client.close()

    def __enter__(self):
        return self.connect()

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self.close()

