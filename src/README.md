# MongoDB Python Konsolen-App

Vorlage zur Vorbereitung auf die praktische Pruefung vom 1. Juni 2026.

Wichtig: In der Pruefung ist der Einsatz von KI nicht erlaubt. Nutze diese App vorher zum Ueben und als eigenes Codebeispiel nur so, wie es die erlaubten Hilfsmittel deiner Pruefung zulassen.

## Inhalt

- MongoDB-Verbindung mit Python aufbauen und schliessen
- CRUD-Operationen fuer Produkte
- Filter-Abfragen in Python
- DAO-Pattern mit abstrakter Klasse
- Validierungen und eigene Exceptions
- Konsolenmenue mit Fehlerbehandlung

## Installation

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

MongoDB muss lokal laufen, zum Beispiel auf:

```text
mongodb://localhost:27017
```

Mit Docker kannst du die vorbereitete Datenbank starten:

```bash
docker compose up -d
```

Diese App ist bereits fuer den Docker-Container konfiguriert:

```ini
uri = mongodb://localhost:27018
username = m165
password = m165pass
auth_source = admin
```

Optional kannst du eigene Werte setzen:

```bash
export MONGO_URI="mongodb://localhost:27017"
export MONGO_DB="pruefung_db"
```

Die pruefungsnahe Buch-App `book_exam_app.py` liest ihre Verbindung aus `config.ini`.
Wenn deine lokale MongoDB Authentifizierung verlangt, trage dort Benutzername und Passwort ein:

```ini
[mongodb]
uri = mongodb://localhost:27017
database = booksdb
collection = books
username = dein_username
password = dein_passwort
auth_source = admin
```

## Start

```bash
python main.py
```

Pruefungsnahe Buch-App starten:

```bash
python book_exam_app.py
```

Einfachster Start ohne manuelles Aktivieren der `.venv`:

```bash
./start.sh
```

Oder direkt ueber den Python-Starter:

```bash
python main.py
```

## Dateien

- `main.py`: Einstiegspunkt
- `menu.py`: Konsolenlogik
- `db.py`: MongoDB-Verbindung
- `models.py`: Produktmodell
- `validation.py`: Validierungen
- `exceptions.py`: eigene Exceptions
- `dao/abstract_dao.py`: abstrakte DAO-Klasse
- `dao/product_dao.py`: konkrete MongoDB-Implementierung
