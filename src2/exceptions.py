class ValidationError(Exception):
    """Wird ausgelöst, wenn Eingabedaten ungültig sind."""


class BookNotFoundError(Exception):
    """Wird ausgelöst, wenn ein Buch nicht gefunden wurde."""
