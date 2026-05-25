from exceptions import ValidationError
from models import Product


def require_text(value: str, field_name: str) -> str:
    value = value.strip()
    if not value:
        raise ValidationError(f"{field_name} darf nicht leer sein.")
    return value


def parse_float(value: str, field_name: str, minimum: float | None = None) -> float:
    try:
        number = float(value)
    except ValueError as exc:
        raise ValidationError(f"{field_name} muss eine Zahl sein.") from exc

    if minimum is not None and number < minimum:
        raise ValidationError(f"{field_name} muss mindestens {minimum} sein.")
    return number


def parse_int(value: str, field_name: str, minimum: int | None = None) -> int:
    try:
        number = int(value)
    except ValueError as exc:
        raise ValidationError(f"{field_name} muss eine ganze Zahl sein.") from exc

    if minimum is not None and number < minimum:
        raise ValidationError(f"{field_name} muss mindestens {minimum} sein.")
    return number


def validate_product(product: Product) -> Product:
    product.name = require_text(product.name, "Name")
    product.category = require_text(product.category, "Kategorie")

    if product.price < 0:
        raise ValidationError("Preis darf nicht negativ sein.")
    if product.stock < 0:
        raise ValidationError("Lagerbestand darf nicht negativ sein.")

    return product


def validate_update_fields(fields: dict) -> dict:
    allowed_fields = {"name", "category", "price", "stock"}
    cleaned = {}

    for key, value in fields.items():
        if key not in allowed_fields:
            raise ValidationError(f"Feld '{key}' darf nicht aktualisiert werden.")

        if key in {"name", "category"}:
            cleaned[key] = require_text(str(value), key)
        elif key == "price":
            cleaned[key] = float(value)
            if cleaned[key] < 0:
                raise ValidationError("Preis darf nicht negativ sein.")
        elif key == "stock":
            cleaned[key] = int(value)
            if cleaned[key] < 0:
                raise ValidationError("Lagerbestand darf nicht negativ sein.")

    if not cleaned:
        raise ValidationError("Es wurden keine Felder zum Aktualisieren angegeben.")

    return cleaned

