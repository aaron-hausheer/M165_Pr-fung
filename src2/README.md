# M165 Probeprüfung: Python Konsolenprogramm mit MongoDB

Einfache Referenzlösung für die Prüfungs-Lernziele:

- Verbindung zu MongoDB öffnen und schliessen
- CRUD: Create, Read, Update, Delete
- Datensätze mit MongoDB-Abfragen filtern
- DAO mit abstrakter Klasse verwenden
- Eingaben validieren und Exceptions behandeln

## Start

1. MongoDB starten:

```bash
docker compose up -d
```

2. Abhängigkeiten installieren:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
```

3. Programm starten:

```bash
.venv/bin/python main.py
```

## MongoDB

Das Programm verwendet:

- Datenbank: `booksdb`
- Collection: `books`

MongoDB erstellt Datenbanken und Collections erst sichtbar, wenn das erste Dokument gespeichert wurde.

## Dateien

- `main.py`: Konsolenmenü und Programmlogik
- `database.py`: MongoDB-Verbindung öffnen und schliessen
- `dao.py`: abstraktes DAO und konkrete MongoDB-CRUD-Methoden
- `validators.py`: Eingaben prüfen
- `exceptions.py`: eigene Exceptions
- `docker-compose.yml`: MongoDB als Docker-Container
