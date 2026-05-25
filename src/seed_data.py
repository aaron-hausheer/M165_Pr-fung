from dao.product_dao import MongoProductDao
from db import MongoConnection
from models import Product


PRODUCTS = [
    Product("Tastatur", "Zubehoer", 49.90, 12),
    Product("Maus", "Zubehoer", 24.50, 30),
    Product("Monitor", "Hardware", 219.00, 7),
    Product("USB-C Kabel", "Kabel", 12.90, 50),
]


def main() -> None:
    with MongoConnection() as database:
        dao = MongoProductDao(database)
        for product in PRODUCTS:
            product_id = dao.create(product)
            print(f"Eingefuegt: {product.name} ({product_id})")


if __name__ == "__main__":
    main()

