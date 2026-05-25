# Python MongoDB Konsolenprogramm Vorlage

Diese Vorlage ist fuer eine praktische Pruefung gedacht. Sie zeigt:

- MongoDB-Verbindung oeffnen und schliessen
- CRUD mit Python und MongoDB
- Filter-Abfragen
- DAO mit abstrakter Klasse
- Validierung und Exception-Handling
- Konsolenmenue

## Installation

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## MongoDB starten

Empfohlen mit Docker Compose:

```bash
docker compose up -d
```

Stoppen:

```bash
docker compose down
```

Datenbank komplett loeschen:

```bash
docker compose down -v
```

Alternative mit lokaler MongoDB:

```bash
mongod
```

## Programm starten

```bash
python main.py
```

## In der Pruefung anpassen

Die wichtigsten Stellen:

- `models/person.py`: Felder und Validierung anpassen
- `dao/person_dao.py`: Collection-Name und Filter anpassen
- `main.py`: Menuepunkte und Eingaben anpassen

Wenn z.B. statt Personen Produkte verlangt sind:

- `Person` zu `Product` umbenennen
- Felder wie `name`, `price`, `stock`, `category` verwenden
- Validierungen entsprechend anpassen
- Collection z.B. `products` nennen
