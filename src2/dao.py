from abc import ABC, abstractmethod

from bson import ObjectId
from bson.errors import InvalidId
from pymongo.collection import Collection

from exceptions import BookNotFoundError


class BookDao(ABC):
    # Abstrakte Klasse: Sie definiert nur, welche Methoden ein DAO haben muss.
    # Die konkrete Datenbank-Logik steht weiter unten in MongoBookDao.
    @abstractmethod
    def create(self, book: dict) -> str:
        pass

    @abstractmethod
    def find_all(self) -> list[dict]:
        pass

    @abstractmethod
    def find_by_id(self, book_id: str) -> dict:
        pass

    @abstractmethod
    def find_by_author(self, author: str) -> list[dict]:
        pass

    @abstractmethod
    def update(self, book_id: str, book: dict) -> None:
        pass

    @abstractmethod
    def delete(self, book_id: str) -> None:
        pass


class MongoBookDao(BookDao):
    def __init__(self, collection: Collection):
        # Das DAO arbeitet nur mit der Collection.
        # main.py muss dadurch keine MongoDB-Befehle kennen.
        self.collection = collection

    def create(self, book: dict) -> str:
        # CREATE: Neues Dokument in MongoDB speichern.
        result = self.collection.insert_one(book)

        # MongoDB erzeugt automatisch eine eindeutige _id.
        # Für die Konsole geben wir sie als String zurück.
        return str(result.inserted_id)

    def find_all(self) -> list[dict]:
        # READ: Alle Bücher lesen und nach Titel aufsteigend sortieren.
        return list(self.collection.find().sort("title", 1))

    def find_by_id(self, book_id: str) -> dict:
        # READ: Ein einzelnes Buch über seine MongoDB-ID suchen.
        book = self.collection.find_one({"_id": self._to_object_id(book_id)})
        if book is None:
            raise BookNotFoundError("Buch wurde nicht gefunden.")
        return book

    def find_by_author(self, author: str) -> list[dict]:
        # FILTER: $regex sucht nach einem Teiltext.
        # $options "i" bedeutet: Gross-/Kleinschreibung ignorieren.
        query = {"author": {"$regex": author, "$options": "i"}}
        return list(self.collection.find(query).sort("title", 1))

    def update(self, book_id: str, book: dict) -> None:
        # UPDATE: Mit $set werden die angegebenen Felder ersetzt/aktualisiert.
        result = self.collection.update_one(
            {"_id": self._to_object_id(book_id)},
            {"$set": book},
        )

        # matched_count == 0 bedeutet: Es gab kein Dokument mit dieser ID.
        if result.matched_count == 0:
            raise BookNotFoundError("Buch wurde nicht gefunden.")

    def delete(self, book_id: str) -> None:
        # DELETE: Dokument anhand der ID löschen.
        result = self.collection.delete_one({"_id": self._to_object_id(book_id)})
        if result.deleted_count == 0:
            raise BookNotFoundError("Buch wurde nicht gefunden.")

    def _to_object_id(self, book_id: str) -> ObjectId:
        # MongoDB speichert _id als ObjectId, nicht als normalen String.
        # Darum muss die Eingabe aus der Konsole zuerst umgewandelt werden.
        try:
            return ObjectId(book_id)
        except InvalidId as exc:
            raise BookNotFoundError("Ungültige ID.") from exc
