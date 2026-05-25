from exceptions import ValidationError


def validate_not_empty(value: str, field_name: str) -> str:
    # strip() entfernt Leerzeichen am Anfang und Ende.
    # So gilt "   " ebenfalls als leer.
    value = value.strip()
    if value == "":
        raise ValidationError(f"{field_name} darf nicht leer sein.")
    return value


def validate_year(value: str) -> int:
    try:
        # input() liefert immer Text. Für das Jahr brauchen wir eine Zahl.
        year = int(value)
    except ValueError as exc:
        raise ValidationError("Jahr muss eine Zahl sein.") from exc

    # Einfache fachliche Prüfung, damit kein unrealistisches Jahr gespeichert wird.
    if year < 0 or year > 2100:
        raise ValidationError("Jahr muss zwischen 0 und 2100 liegen.")

    return year


def validate_pages(value: str) -> int:
    try:
        # Auch die Seitenzahl kommt aus input() zuerst als Text.
        pages = int(value)
    except ValueError as exc:
        raise ValidationError("Seitenzahl muss eine Zahl sein.") from exc

    # Ein Buch mit 0 oder negativer Seitenzahl ist ungültig.
    if pages <= 0:
        raise ValidationError("Seitenzahl muss grösser als 0 sein.")

    return pages
