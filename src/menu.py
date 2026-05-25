from dao.product_dao import MongoProductDao
from exceptions import AppError
from models import Product
from validation import parse_float, parse_int, require_text


class ProductMenu:
    def __init__(self, dao: MongoProductDao) -> None:
        self.dao = dao

    def run(self) -> None:
        while True:
            self._print_menu()
            choice = input("Auswahl: ").strip()

            try:
                if choice == "1":
                    self.create_product()
                elif choice == "2":
                    self.show_products(self.dao.find_all())
                elif choice == "3":
                    self.search_products()
                elif choice == "4":
                    self.update_product()
                elif choice == "5":
                    self.delete_product()
                elif choice == "0":
                    print("Programm beendet.")
                    return
                else:
                    print("Ungueltige Auswahl.")
            except AppError as exc:
                print(f"Fehler: {exc}")

    def _print_menu(self) -> None:
        print()
        print("=== Produktverwaltung ===")
        print("1 Produkt erfassen")
        print("2 Alle Produkte anzeigen")
        print("3 Produkte suchen / filtern")
        print("4 Produkt aktualisieren")
        print("5 Produkt loeschen")
        print("0 Beenden")

    def create_product(self) -> None:
        name = require_text(input("Name: "), "Name")
        category = require_text(input("Kategorie: "), "Kategorie")
        price = parse_float(input("Preis: "), "Preis", minimum=0)
        stock = parse_int(input("Lagerbestand: "), "Lagerbestand", minimum=0)

        product_id = self.dao.create(Product(name, category, price, stock))
        print(f"Produkt erstellt mit ID: {product_id}")

    def search_products(self) -> None:
        category = input("Kategorie enthaelt (leer = egal): ").strip() or None
        search_text = input("Name enthaelt (leer = egal): ").strip() or None
        min_price_text = input("Mindestpreis (leer = egal): ").strip()
        min_price = parse_float(min_price_text, "Mindestpreis", minimum=0) if min_price_text else None

        products = self.dao.find_by_filter(
            category=category,
            min_price=min_price,
            search_text=search_text,
        )
        self.show_products(products)

    def update_product(self) -> None:
        product_id = require_text(input("ID des Produkts: "), "ID")
        current = self.dao.find_by_id(product_id)
        print("Leer lassen, wenn der Wert unveraendert bleiben soll.")

        fields = {}
        name = input(f"Name [{current['name']}]: ").strip()
        category = input(f"Kategorie [{current['category']}]: ").strip()
        price = input(f"Preis [{current['price']}]: ").strip()
        stock = input(f"Lagerbestand [{current['stock']}]: ").strip()

        if name:
            fields["name"] = name
        if category:
            fields["category"] = category
        if price:
            fields["price"] = parse_float(price, "Preis", minimum=0)
        if stock:
            fields["stock"] = parse_int(stock, "Lagerbestand", minimum=0)

        changed = self.dao.update(product_id, fields)
        if changed:
            print("Produkt aktualisiert.")
        else:
            print("Produkt war bereits auf diesem Stand.")

    def delete_product(self) -> None:
        product_id = require_text(input("ID des Produkts: "), "ID")
        confirm = input("Wirklich loeschen? (j/N): ").strip().lower()
        if confirm != "j":
            print("Loeschen abgebrochen.")
            return

        self.dao.delete(product_id)
        print("Produkt geloescht.")

    def show_products(self, products: list[dict]) -> None:
        if not products:
            print("Keine Produkte gefunden.")
            return

        print()
        print(f"{'ID':24}  {'Name':20}  {'Kategorie':15}  {'Preis':>8}  {'Lager':>5}")
        print("-" * 82)
        for product in products:
            print(
                f"{product['id']:24}  "
                f"{product['name'][:20]:20}  "
                f"{product['category'][:15]:15}  "
                f"{product['price']:8.2f}  "
                f"{product['stock']:5}"
            )

