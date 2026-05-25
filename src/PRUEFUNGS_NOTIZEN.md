# Pruefungs-Notizen

Diese Vorlage verwendet `Product` als Beispiel-Entitaet. Wenn in der Pruefung eine andere Entitaet verlangt wird, zum Beispiel `Kunde`, `Buch`, `Film` oder `Mitarbeiter`, musst du vor allem diese Stellen anpassen:

1. `models.py`
   - Dataclass-Felder aendern
   - `to_document()` und `from_document()` anpassen

2. `validation.py`
   - Pflichtfelder pruefen
   - Zahlenbereiche pruefen
   - eigene Validierungsregeln ergaenzen

3. `dao/product_dao.py`
   - Collection-Name aendern: `database["products"]`
   - Filter in `find_by_filter()` anpassen
   - Indexe anpassen

4. `menu.py`
   - Eingabefelder im Menue anpassen
   - Tabellen-Ausgabe anpassen

## Typische MongoDB-Befehle in Python

```python
collection.insert_one(document)
collection.find()
collection.find_one({"_id": ObjectId(id)})
collection.find({"category": {"$regex": "buch", "$options": "i"}})
collection.find({"price": {"$gte": 10}})
collection.update_one({"_id": ObjectId(id)}, {"$set": {"name": "Neu"}})
collection.delete_one({"_id": ObjectId(id)})
```

## Typischer Ablauf

```python
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")
db = client["pruefung_db"]
collection = db["products"]

collection.insert_one({"name": "Maus", "price": 19.90})

for document in collection.find():
    print(document)

client.close()
```

## Fehlerbehandlung

```python
try:
    value = int(input("Zahl: "))
except ValueError:
    print("Bitte eine ganze Zahl eingeben.")
```

## ObjectId

MongoDB speichert IDs als `ObjectId`. Benutzereingaben sind Strings und muessen umgewandelt werden:

```python
from bson import ObjectId
from bson.errors import InvalidId

try:
    object_id = ObjectId(user_input)
except InvalidId:
    print("Ungueltige ID")
```

