from pymongo.errors import DuplicateKeyError, PyMongoError

from dao.person_dao import PersonDAO
from database import MongoDatabase
from exceptions import NotFoundError, ValidationError
from models.person import Person


def read_int(label, minimum=None, maximum=None):
    while True:
        try:
            value = int(input(label))
            if minimum is not None and value < minimum:
                print(f"Wert muss mindestens {minimum} sein.")
                continue
            if maximum is not None and value > maximum:
                print(f"Wert darf maximal {maximum} sein.")
                continue
            return value
        except ValueError:
            print("Bitte eine ganze Zahl eingeben.")


def read_bool(label):
    while True:
        value = input(label + " (j/n): ").strip().lower()
        if value in ("j", "ja", "y", "yes"):
            return True
        if value in ("n", "nein", "no"):
            return False
        print("Bitte j oder n eingeben.")


def print_person(person):
    print(
        f"ID: {person['_id']} | "
        f"{person['first_name']} {person['last_name']} | "
        f"Alter: {person['age']} | "
        f"E-Mail: {person['email']} | "
        f"Ort: {person['city']} | "
        f"Aktiv: {person.get('active', True)}"
    )


def print_persons(persons):
    if not persons:
        print("Keine Datensaetze gefunden.")
        return

    for person in persons:
        print_person(person)


def create_person(dao):
    person = Person(
        first_name=input("Vorname: "),
        last_name=input("Nachname: "),
        age=read_int("Alter: ", 0, 120),
        email=input("E-Mail: "),
        city=input("Ort: "),
        active=read_bool("Aktiv"),
    )
    inserted_id = dao.create(person)
    print(f"Person erstellt mit ID: {inserted_id}")


def update_person(dao):
    person_id = input("ID der Person: ")
    print("Leere Eingabe bedeutet: Feld nicht aendern.")

    first_name = input("Neuer Vorname: ")
    last_name = input("Neuer Nachname: ")
    age_text = input("Neues Alter: ")
    email = input("Neue E-Mail: ")
    city = input("Neuer Ort: ")
    active_text = input("Aktiv? leer/j/n: ").strip().lower()

    age = int(age_text) if age_text else None
    active = None
    if active_text in ("j", "ja", "y", "yes"):
        active = True
    elif active_text in ("n", "nein", "no"):
        active = False

    modified_count = dao.update(
        person_id,
        {
            "first_name": first_name,
            "last_name": last_name,
            "age": age,
            "email": email,
            "city": city,
            "active": active,
        },
    )
    print(f"Geaenderte Datensaetze: {modified_count}")


def delete_person(dao):
    person_id = input("ID der Person: ")
    deleted_count = dao.delete(person_id)
    print(f"Geloeschte Datensaetze: {deleted_count}")


def show_filter_menu(dao):
    print("\nFilter")
    print("1 - Nach Ort suchen")
    print("2 - Mindestalter")
    print("3 - Altersbereich")
    print("4 - Nach Name suchen")
    print("5 - Nur aktive Personen")
    print("6 - Nach Alter absteigend sortieren")
    print("7 - Personen pro Ort zaehlen")

    choice = input("Auswahl: ")

    if choice == "1":
        city = input("Ort: ")
        print_persons(dao.find_by_city(city))
    elif choice == "2":
        min_age = read_int("Mindestalter: ", 0, 120)
        print_persons(dao.find_by_min_age(min_age))
    elif choice == "3":
        min_age = read_int("Von Alter: ", 0, 120)
        max_age = read_int("Bis Alter: ", min_age, 120)
        print_persons(dao.find_by_age_range(min_age, max_age))
    elif choice == "4":
        search_text = input("Suchtext: ")
        print_persons(dao.find_by_name(search_text))
    elif choice == "5":
        print_persons(dao.find_active())
    elif choice == "6":
        print_persons(dao.find_sorted_by_age_desc())
    elif choice == "7":
        city = input("Ort: ")
        print(f"Anzahl: {dao.count_by_city(city)}")
    else:
        print("Ungueltige Auswahl.")


def seed_examples(dao):
    examples = [
        Person("Anna", "Meier", 22, "anna.meier@example.com", "Zuerich", True),
        Person("Ben", "Mueller", 35, "ben.mueller@example.com", "Bern", True),
        Person("Clara", "Keller", 17, "clara.keller@example.com", "Zuerich", False),
    ]

    for person in examples:
        try:
            dao.create(person)
        except DuplicateKeyError:
            pass

    print("Beispieldaten eingefuegt.")


def show_menu():
    print("\n--- MongoDB Pruefungs-Vorlage ---")
    print("1 - Person erstellen")
    print("2 - Alle Personen anzeigen")
    print("3 - Person nach ID anzeigen")
    print("4 - Person aktualisieren")
    print("5 - Person loeschen")
    print("6 - Filter / Suche")
    print("7 - Person deaktivieren")
    print("8 - Beispieldaten einfuegen")
    print("0 - Beenden")


def main():
    database_connection = MongoDatabase()

    try:
        database = database_connection.connect()
        dao = PersonDAO(database)

        while True:
            try:
                show_menu()
                choice = input("Auswahl: ")

                if choice == "1":
                    create_person(dao)
                elif choice == "2":
                    print_persons(dao.find_all())
                elif choice == "3":
                    person_id = input("ID der Person: ")
                    print_person(dao.find_by_id(person_id))
                elif choice == "4":
                    update_person(dao)
                elif choice == "5":
                    delete_person(dao)
                elif choice == "6":
                    show_filter_menu(dao)
                elif choice == "7":
                    person_id = input("ID der Person: ")
                    dao.deactivate(person_id)
                    print("Person wurde deaktiviert.")
                elif choice == "8":
                    seed_examples(dao)
                elif choice == "0":
                    print("Programm beendet.")
                    break
                else:
                    print("Ungueltige Auswahl.")

            except DuplicateKeyError:
                print("Fehler: Diese E-Mail existiert bereits.")
            except ValidationError as error:
                print(f"Validierungsfehler: {error}")
            except NotFoundError as error:
                print(f"Nicht gefunden: {error}")
            except ValueError:
                print("Fehler: Zahl konnte nicht gelesen werden.")

    except PyMongoError as error:
        print(f"MongoDB-Fehler: {error}")
    finally:
        database_connection.close()


if __name__ == "__main__":
    main()
