from exceptions import ValidationError


class Person:
    def __init__(self, first_name, last_name, age, email, city, active=True):
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.email = email
        self.city = city
        self.active = active
        self.validate()

    def validate(self):
        if not self.first_name or len(self.first_name.strip()) < 2:
            raise ValidationError("Vorname muss mindestens 2 Zeichen haben.")

        if not self.last_name or len(self.last_name.strip()) < 2:
            raise ValidationError("Nachname muss mindestens 2 Zeichen haben.")

        if not isinstance(self.age, int):
            raise ValidationError("Alter muss eine ganze Zahl sein.")

        if self.age < 0 or self.age > 120:
            raise ValidationError("Alter muss zwischen 0 und 120 sein.")

        if not self.email or "@" not in self.email or "." not in self.email:
            raise ValidationError("E-Mail ist ungueltig.")

        if not self.city or len(self.city.strip()) < 2:
            raise ValidationError("Ort muss mindestens 2 Zeichen haben.")

        if not isinstance(self.active, bool):
            raise ValidationError("Aktiv muss True oder False sein.")

    def to_dict(self):
        return {
            "first_name": self.first_name.strip(),
            "last_name": self.last_name.strip(),
            "age": self.age,
            "email": self.email.strip().lower(),
            "city": self.city.strip(),
            "active": self.active,
        }

    @staticmethod
    def from_dict(data):
        return Person(
            first_name=data["first_name"],
            last_name=data["last_name"],
            age=data["age"],
            email=data["email"],
            city=data["city"],
            active=data.get("active", True),
        )

