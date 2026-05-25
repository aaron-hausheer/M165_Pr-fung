from dao import MongoBookDao
from database import MongoDatabase
from exceptions import BookNotFoundError, ValidationError
from validators import validate_not_empty, validate_pages, validate_year


def read_book_from_input() -> dict:
    # Alle Eingaben für ein Buch werden hier gesammelt und validiert.
    # Wenn etwas ungültig ist, wird eine ValidationError-Exception ausgelöst.
    title = validate_not_empty(input("Titel: "), "Titel")
    author = validate_not_empty(input("Autor: "), "Autor")
    year = validate_year(input("Jahr: "))
    pages = validate_pages(input("Seitenzahl: "))

    # Dieses Dictionary ist das Dokument, das später in MongoDB gespeichert wird.
    return {
        "title": title,
        "author": author,
        "year": year,
        "pages": pages,
    }


def print_book(book: dict) -> None:
    # MongoDB-Dokumente sind Dictionaries.
    # Die _id wurde von MongoDB automatisch erzeugt.
    print(
        f"ID: {book['_id']} | "
        f"{book['title']} von {book['author']} | "
        f"{book['year']} | {book['pages']} Seiten"
    )


def print_books(books: list[dict]) -> None:
    # Wenn die Liste leer ist, wurde bei der Suche nichts gefunden.
    if len(books) == 0:
        print("Keine Bücher gefunden.")
        return

    for book in books:
        print_book(book)


def create_book(dao: MongoBookDao) -> None:
    # CREATE: Eingaben lesen, validieren und über das DAO speichern.
    book = read_book_from_input()
    book_id = dao.create(book)
    print(f"Buch wurde gespeichert. ID: {book_id}")


def show_all_books(dao: MongoBookDao) -> None:
    # READ: Alle Bücher aus der Datenbank holen.
    books = dao.find_all()
    print_books(books)


def search_book_by_id(dao: MongoBookDao) -> None:
    # READ: Ein bestimmtes Buch suchen.
    book_id = validate_not_empty(input("ID: "), "ID")
    book = dao.find_by_id(book_id)
    print_book(book)


def search_books_by_author(dao: MongoBookDao) -> None:
    # FILTER: Bücher nach Autor suchen. Teiltext reicht, z.B. "martin".
    author = validate_not_empty(input("Autor suchen: "), "Autor")
    books = dao.find_by_author(author)
    print_books(books)


def update_book(dao: MongoBookDao) -> None:
    # UPDATE: ID bestimmen und danach alle Buchdaten neu erfassen.
    book_id = validate_not_empty(input("ID des Buchs: "), "ID")
    print("Neue Werte eingeben:")
    book = read_book_from_input()
    dao.update(book_id, book)
    print("Buch wurde aktualisiert.")


def delete_book(dao: MongoBookDao) -> None:
    # DELETE: Buch anhand der ID löschen.
    book_id = validate_not_empty(input("ID des Buchs: "), "ID")
    dao.delete(book_id)
    print("Buch wurde gelöscht.")


def print_menu() -> None:
    print()
    print("===== Bücherverwaltung =====")
    print("1. Buch erstellen")
    print("2. Alle Bücher anzeigen")
    print("3. Buch nach ID suchen")
    print("4. Bücher nach Autor filtern")
    print("5. Buch aktualisieren")
    print("6. Buch löschen")
    print("0. Programm beenden")


def main() -> None:
    # Verbindung zur Datenbank erstellen.
    db = MongoDatabase()

    # Collection "books" aus der Datenbank "booksdb" holen.
    # Die Datenzugriffe laufen ab hier über das DAO.
    dao = MongoBookDao(db.get_collection("books"))

    try:
        # Hauptschleife: Das Menü wird so lange angezeigt, bis der Benutzer 0 wählt.
        while True:
            print_menu()
            choice = input("Auswahl: ").strip()

            try:
                # Je nach Auswahl wird eine passende Funktion aufgerufen.
                if choice == "1":
                    create_book(dao)
                elif choice == "2":
                    show_all_books(dao)
                elif choice == "3":
                    search_book_by_id(dao)
                elif choice == "4":
                    search_books_by_author(dao)
                elif choice == "5":
                    update_book(dao)
                elif choice == "6":
                    delete_book(dao)
                elif choice == "0":
                    print("Programm beendet.")
                    break
                else:
                    print("Ungültige Auswahl.")
            except (ValidationError, BookNotFoundError) as error:
                # Erwartete Fehler werden abgefangen, damit das Programm weiterläuft.
                # Beispiele: leere Eingabe, falsches Jahr, unbekannte ID.
                print(f"Fehler: {error}")
    finally:
        # finally wird immer ausgeführt, auch wenn ein Fehler passiert.
        # So wird die MongoDB-Verbindung zuverlässig geschlossen.
        db.close()


if __name__ == "__main__":
    main()
