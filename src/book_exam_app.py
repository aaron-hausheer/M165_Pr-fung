from configparser import ConfigParser

from bson import ObjectId
from bson.errors import InvalidId
from pymongo import MongoClient
from pymongo.errors import OperationFailure, PyMongoError


class BookValidationError(Exception):
    pass


class BookNotFoundError(Exception):
    pass


class BookDatabaseError(Exception):
    pass


class BookMongoApp:
    def __init__(self, config_file: str = "config.ini") -> None:
        config = ConfigParser()
        config.read(config_file)

        uri = config["mongodb"]["uri"]
        database_name = config["mongodb"]["database"]
        collection_name = config["mongodb"]["collection"]
        username = config["mongodb"].get("username", "").strip()
        password = config["mongodb"].get("password", "").strip()
        auth_source = config["mongodb"].get("auth_source", "admin").strip()

        client_options = {"serverSelectionTimeoutMS": 3000}
        if username and password:
            client_options["username"] = username
            client_options["password"] = password
            client_options["authSource"] = auth_source or "admin"

        self.client = MongoClient(uri, **client_options)
        self.database = self.client[database_name]
        self.collection = self.database[collection_name]
        self._check_connection()

    def close(self) -> None:
        self.client.close()

    def create_book(self, title: str, author: str, price: float) -> str:
        book = self._validate_book(title, author, price)
        try:
            result = self.collection.insert_one(book)
            return str(result.inserted_id)
        except PyMongoError as exc:
            raise self._database_error(exc) from exc

    def count_books(self) -> int:
        try:
            return self.collection.count_documents({})
        except PyMongoError as exc:
            raise self._database_error(exc) from exc

    def update_price(self, book_id: str, new_price: float) -> bool:
        if new_price < 0:
            raise BookValidationError("Preis darf nicht negativ sein.")

        try:
            result = self.collection.update_one(
                {"_id": self._object_id(book_id)},
                {"$set": {"price": new_price}},
            )
        except PyMongoError as exc:
            raise self._database_error(exc) from exc

        if result.matched_count == 0:
            raise BookNotFoundError("Buch nicht gefunden.")
        return result.modified_count > 0

    def find_books_between_prices(self, min_price: float, max_price: float) -> list[dict]:
        query = {"price": {"$gte": min_price, "$lte": max_price}}
        try:
            return list(self.collection.find(query).sort("price", 1))
        except PyMongoError as exc:
            raise self._database_error(exc) from exc

    def get_all_titles(self) -> list[str]:
        try:
            books = self.collection.find({}, {"title": 1, "_id": 0}).sort("title", 1)
            return [book["title"] for book in books]
        except PyMongoError as exc:
            raise self._database_error(exc) from exc

    def delete_book(self, book_id: str) -> bool:
        try:
            result = self.collection.delete_one({"_id": self._object_id(book_id)})
        except PyMongoError as exc:
            raise self._database_error(exc) from exc

        if result.deleted_count == 0:
            raise BookNotFoundError("Buch nicht gefunden.")
        return True

    def drop_books_collection(self) -> None:
        try:
            self.collection.drop()
        except PyMongoError as exc:
            raise self._database_error(exc) from exc

    def list_books(self) -> list[dict]:
        try:
            return list(self.collection.find().sort("title", 1))
        except PyMongoError as exc:
            raise self._database_error(exc) from exc

    def _validate_book(self, title: str, author: str, price: float) -> dict:
        title = title.strip()
        author = author.strip()

        if not title:
            raise BookValidationError("Titel darf nicht leer sein.")
        if not author:
            raise BookValidationError("Autor darf nicht leer sein.")
        if price < 0:
            raise BookValidationError("Preis darf nicht negativ sein.")

        return {"title": title, "author": author, "price": price}

    def _object_id(self, value: str) -> ObjectId:
        try:
            return ObjectId(value)
        except InvalidId as exc:
            raise BookValidationError("Ungueltige MongoDB-ID.") from exc

    def _check_connection(self) -> None:
        try:
            self.client.admin.command("ping")
        except PyMongoError as exc:
            raise self._database_error(exc) from exc

    def _database_error(self, exc: PyMongoError) -> BookDatabaseError:
        if isinstance(exc, OperationFailure) and exc.code == 13:
            return BookDatabaseError(
                "MongoDB verlangt Authentifizierung. Trage username/password in config.ini ein."
            )
        return BookDatabaseError(f"MongoDB-Fehler: {exc}")


def read_price(label: str) -> float:
    try:
        return float(input(label))
    except ValueError as exc:
        raise BookValidationError("Preis muss eine Zahl sein.") from exc


def print_books(books: list[dict]) -> None:
    if not books:
        print("Keine Buecher gefunden.")
        return

    print(f"{'ID':24}  {'Titel':25}  {'Autor':20}  {'Preis':>8}")
    print("-" * 84)
    for book in books:
        print(
            f"{str(book['_id']):24}  "
            f"{book['title'][:25]:25}  "
            f"{book['author'][:20]:20}  "
            f"{book['price']:8.2f}"
        )


def print_menu() -> None:
    print()
    print("=== Book App ===")
    print("1 Buch erfassen")
    print("2 Alle Buecher anzeigen")
    print("3 Anzahl Buecher anzeigen")
    print("4 Preis eines Buches aendern")
    print("5 Buecher zwischen zwei Preisen anzeigen")
    print("6 Nur Buchtitel anzeigen")
    print("7 Buch loeschen")
    print("8 Collection books loeschen")
    print("0 Beenden")


def run() -> None:
    try:
        app = BookMongoApp()
    except BookDatabaseError as exc:
        print(f"Fehler: {exc}")
        return

    try:
        while True:
            print_menu()
            choice = input("Auswahl: ").strip()

            try:
                if choice == "1":
                    title = input("Titel: ")
                    author = input("Autor: ")
                    price = read_price("Preis: ")
                    book_id = app.create_book(title, author, price)
                    print(f"Buch erstellt mit ID: {book_id}")
                elif choice == "2":
                    print_books(app.list_books())
                elif choice == "3":
                    print(f"Anzahl Buecher: {app.count_books()}")
                elif choice == "4":
                    book_id = input("ID: ").strip()
                    price = read_price("Neuer Preis: ")
                    changed = app.update_price(book_id, price)
                    print("Preis aktualisiert." if changed else "Preis war bereits gleich.")
                elif choice == "5":
                    min_price = read_price("Minimaler Preis: ")
                    max_price = read_price("Maximaler Preis: ")
                    print_books(app.find_books_between_prices(min_price, max_price))
                elif choice == "6":
                    for title in app.get_all_titles():
                        print(title)
                elif choice == "7":
                    book_id = input("ID: ").strip()
                    app.delete_book(book_id)
                    print("Buch geloescht.")
                elif choice == "8":
                    confirm = input("Collection wirklich loeschen? (j/N): ").strip().lower()
                    if confirm == "j":
                        app.drop_books_collection()
                        print("Collection geloescht.")
                    else:
                        print("Abgebrochen.")
                elif choice == "0":
                    print("Programm beendet.")
                    return
                else:
                    print("Ungueltige Auswahl.")
            except (BookValidationError, BookNotFoundError, BookDatabaseError) as exc:
                print(f"Fehler: {exc}")
    finally:
        app.close()


if __name__ == "__main__":
    run()
