from bson import ObjectId
from bson.errors import InvalidId
from pymongo.collection import Collection

from dao.abstract_dao import AbstractProductDao
from exceptions import DatabaseError, NotFoundError, ValidationError
from models import Product
from validation import validate_product, validate_update_fields


class MongoProductDao(AbstractProductDao):
    def __init__(self, database) -> None:
        self.collection: Collection = database["products"]
        self.collection.create_index("name")
        self.collection.create_index("category")

    def create(self, product: Product) -> str:
        try:
            valid_product = validate_product(product)
            result = self.collection.insert_one(valid_product.to_document())
            return str(result.inserted_id)
        except ValidationError:
            raise
        except Exception as exc:
            raise DatabaseError("Produkt konnte nicht erstellt werden.") from exc

    def find_all(self) -> list[dict]:
        try:
            documents = self.collection.find().sort("name", 1)
            return [Product.from_document(document) for document in documents]
        except Exception as exc:
            raise DatabaseError("Produkte konnten nicht gelesen werden.") from exc

    def find_by_id(self, product_id: str) -> dict:
        try:
            document = self.collection.find_one({"_id": self._object_id(product_id)})
            if document is None:
                raise NotFoundError("Produkt nicht gefunden.")
            return Product.from_document(document)
        except (ValidationError, NotFoundError):
            raise
        except Exception as exc:
            raise DatabaseError("Produkt konnte nicht gelesen werden.") from exc

    def find_by_filter(
        self,
        category: str | None = None,
        min_price: float | None = None,
        search_text: str | None = None,
    ) -> list[dict]:
        query = {}

        if category:
            query["category"] = {"$regex": category, "$options": "i"}
        if min_price is not None:
            query["price"] = {"$gte": min_price}
        if search_text:
            query["name"] = {"$regex": search_text, "$options": "i"}

        try:
            documents = self.collection.find(query).sort("name", 1)
            return [Product.from_document(document) for document in documents]
        except Exception as exc:
            raise DatabaseError("Filter-Abfrage fehlgeschlagen.") from exc

    def update(self, product_id: str, fields: dict) -> bool:
        try:
            cleaned_fields = validate_update_fields(fields)
            result = self.collection.update_one(
                {"_id": self._object_id(product_id)},
                {"$set": cleaned_fields},
            )
            if result.matched_count == 0:
                raise NotFoundError("Produkt nicht gefunden.")
            return result.modified_count > 0
        except (ValidationError, NotFoundError):
            raise
        except Exception as exc:
            raise DatabaseError("Produkt konnte nicht aktualisiert werden.") from exc

    def delete(self, product_id: str) -> bool:
        try:
            result = self.collection.delete_one({"_id": self._object_id(product_id)})
            if result.deleted_count == 0:
                raise NotFoundError("Produkt nicht gefunden.")
            return True
        except (ValidationError, NotFoundError):
            raise
        except Exception as exc:
            raise DatabaseError("Produkt konnte nicht geloescht werden.") from exc

    def _object_id(self, value: str) -> ObjectId:
        try:
            return ObjectId(value)
        except InvalidId as exc:
            raise ValidationError("Ungueltige MongoDB-ID.") from exc

