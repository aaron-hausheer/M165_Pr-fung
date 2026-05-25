from pymongo import MongoClient


class MongoDatabase:
    def __init__(self, uri: str = "mongodb://localhost:27017", db_name: str = "booksdb"):
        # MongoClient baut die Verbindung zur MongoDB auf.
        # Die URI zeigt auf die MongoDB aus docker-compose.yml.
        self.client = MongoClient(uri)

        # In MongoDB wird eine Datenbank erst sichtbar erstellt,
        # sobald mindestens ein Dokument in eine Collection eingefügt wird.
        self.database = self.client[db_name]

    def get_collection(self, name: str):
        # Gibt eine Collection zurück, z.B. "books".
        # Auch die Collection wird erst sichtbar erstellt, wenn Daten eingefügt werden.
        return self.database[name]

    def close(self) -> None:
        # Verbindung sauber schliessen. Das gehört zu den Prüfungs-Lernzielen.
        self.client.close()
