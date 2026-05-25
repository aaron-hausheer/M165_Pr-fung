from bson import ObjectId
from pymongo import ASCENDING, DESCENDING

from dao.abstract_dao import AbstractDAO
from exceptions import NotFoundError, ValidationError
from models.person import Person


class PersonDAO(AbstractDAO):
    def __init__(self, database):
        self.collection = database["persons"]
        self.collection.create_index("email", unique=True)

    def create(self, person):
        result = self.collection.insert_one(person.to_dict())
        return str(result.inserted_id)

    def find_all(self):
        return list(self.collection.find().sort("last_name", ASCENDING))

    def find_by_id(self, person_id):
        document = self.collection.find_one({"_id": self._object_id(person_id)})
        if document is None:
            raise NotFoundError("Person wurde nicht gefunden.")
        return document

    def update(self, person_id, data):
        update_data = self._clean_update_data(data)

        if not update_data:
            raise ValidationError("Keine gueltigen Update-Daten erhalten.")

        old_document = self.find_by_id(person_id)
        merged_document = {
            **old_document,
            **update_data,
        }

        Person.from_dict(merged_document)

        result = self.collection.update_one(
            {"_id": self._object_id(person_id)},
            {"$set": update_data},
        )

        if result.matched_count == 0:
            raise NotFoundError("Person wurde nicht gefunden.")

        return result.modified_count

    def delete(self, person_id):
        result = self.collection.delete_one({"_id": self._object_id(person_id)})
        if result.deleted_count == 0:
            raise NotFoundError("Person wurde nicht gefunden.")
        return result.deleted_count

    def find_by_city(self, city):
        return list(self.collection.find({"city": {"$regex": city, "$options": "i"}}))

    def find_by_min_age(self, min_age):
        return list(self.collection.find({"age": {"$gte": min_age}}).sort("age", ASCENDING))

    def find_by_age_range(self, min_age, max_age):
        return list(
            self.collection.find({"age": {"$gte": min_age, "$lte": max_age}}).sort(
                "age", ASCENDING
            )
        )

    def find_by_name(self, search_text):
        query = {
            "$or": [
                {"first_name": {"$regex": search_text, "$options": "i"}},
                {"last_name": {"$regex": search_text, "$options": "i"}},
            ]
        }
        return list(self.collection.find(query).sort("last_name", ASCENDING))

    def find_active(self):
        return list(self.collection.find({"active": True}).sort("last_name", ASCENDING))

    def find_sorted_by_age_desc(self):
        return list(self.collection.find().sort("age", DESCENDING))

    def count_by_city(self, city):
        return self.collection.count_documents({"city": {"$regex": city, "$options": "i"}})

    def deactivate(self, person_id):
        return self.update(person_id, {"active": False})

    def _object_id(self, value):
        if not ObjectId.is_valid(value):
            raise ValidationError("Ungueltige MongoDB-ID.")
        return ObjectId(value)

    def _clean_update_data(self, data):
        allowed_fields = {"first_name", "last_name", "age", "email", "city", "active"}
        return {
            key: value
            for key, value in data.items()
            if key in allowed_fields and value is not None and value != ""
        }

