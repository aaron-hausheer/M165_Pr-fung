from dataclasses import dataclass


@dataclass
class Product:
    name: str
    category: str
    price: float
    stock: int

    def to_document(self) -> dict:
        return {
            "name": self.name,
            "category": self.category,
            "price": self.price,
            "stock": self.stock,
        }

    @staticmethod
    def from_document(document: dict) -> dict:
        return {
            "id": str(document["_id"]),
            "name": document.get("name", ""),
            "category": document.get("category", ""),
            "price": document.get("price", 0.0),
            "stock": document.get("stock", 0),
        }

