# Pruefung Spickzettel

## MongoDB Verbindung

```python
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")
db = client["meine_datenbank"]
collection = db["meine_collection"]

client.close()
```

## Create

```python
data = {"name": "Test", "age": 20}
result = collection.insert_one(data)
print(result.inserted_id)
```

## Read

```python
alle = list(collection.find())
ein_datensatz = collection.find_one({"name": "Test"})
```

## Update

```python
collection.update_one(
    {"name": "Test"},
    {"$set": {"age": 21}},
)
```

## Delete

```python
collection.delete_one({"name": "Test"})
```

## Wichtige Filter

```python
# Gleichheit
collection.find({"city": "Zuerich"})

# Groesser / kleiner
collection.find({"age": {"$gte": 18}})
collection.find({"age": {"$gte": 18, "$lte": 65}})

# Textsuche mit Regex, nicht case-sensitive
collection.find({"name": {"$regex": "ann", "$options": "i"}})

# OR
collection.find({
    "$or": [
        {"first_name": {"$regex": "ann", "$options": "i"}},
        {"last_name": {"$regex": "ann", "$options": "i"}},
    ]
})

# Sortieren
collection.find().sort("age", 1)   # aufsteigend
collection.find().sort("age", -1)  # absteigend

# Zaehlen
collection.count_documents({"active": True})
```

## ObjectId verwenden

```python
from bson import ObjectId

id_text = "6651f2e7d0c4b6f42b5d1234"

if ObjectId.is_valid(id_text):
    document = collection.find_one({"_id": ObjectId(id_text)})
```

## Validierung

```python
if not name or len(name.strip()) < 2:
    raise ValueError("Name muss mindestens 2 Zeichen haben.")

if age < 0 or age > 120:
    raise ValueError("Alter ist ungueltig.")

if "@" not in email:
    raise ValueError("E-Mail ist ungueltig.")
```

## Exception Handling

```python
try:
    # MongoDB / Validierung / Menue-Logik
    pass
except ValueError as error:
    print(f"Validierungsfehler: {error}")
except Exception as error:
    print(f"Unerwarteter Fehler: {error}")
finally:
    client.close()
```

