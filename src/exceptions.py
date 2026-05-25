class AppError(Exception):
    """Basisklasse fuer erwartete Anwendungsfehler."""


class ValidationError(AppError):
    """Wird geworfen, wenn Eingabedaten ungueltig sind."""


class NotFoundError(AppError):
    """Wird geworfen, wenn ein Datensatz nicht gefunden wurde."""


class DatabaseError(AppError):
    """Wird geworfen, wenn ein Datenbankzugriff fehlschlaegt."""

