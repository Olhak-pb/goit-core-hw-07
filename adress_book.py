
from __future__ import annotations

from collections import UserDict

from datetime import datetime, date, timedelta

class Field:
    def __init__(self, value: str):
        self.value = value

    def __str__(self) -> str:
        return str(self.value)

class Name(Field):
    pass

class Phone(Field):
    """Phone must contain exact 10 digits."""

    def __init__(self, value: str):
        value = str(value)
        if not (value.isdigit() and len(value) == 10):
            raise ValueError("Phone number must contain exactly 10 digits.")
        super().__init__(value)

class Birthday(Field):
    """Birthday must be in DD.MM.YYYY format"""

    def __init__(self, value: str):
        value = str(value)
        try:
            datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Invalid date format. Please use D.MM.YYYY")
        super().__init__(value)
    def to_date(self) -> date:
        return datetime.strptime(self.value, "%d.%m.%Y").date()



class Record:
    def __init__(self, name: str):
        self.name = Name(name)
        self.phones: list[Phone] = []
        self.birthday: Birthday | None = None

    def find_phone(self, phone: str) -> Phone | None:
        for p in self.phones:
            if p.value == phone:
                return p
        return None
        
    def add_phone(self, phone: str) -> None:
        self.phones.append(Phone(phone))

    def remove_phone(self, phone: str) -> None:
        found_phone = self.find_phone(phone)
        if found_phone:
            self.phones.remove(found_phone)

    def edit_phone(self, old_phone: str, new_phone: str) -> None:
        found_phone = self.find_phone(old_phone)
        if not found_phone:
            raise ValueError("Old phone number not found.")
        self.phones[self.phones.index(found_phone)] = Phone(new_phone)

    def add_birthday(self, birthday: str) -> None:
        self.birthday = Birthday(birthday)

    def __str__(self) -> str:
        phones_str = "; ".join(p.value for p in self.phones) if self.phones else "-"
        bday_str = str(self.birthday) if self.birthday else "-"
        return f"Contact name: {self.name.value}, phones: {phones_str}, birthday: {bday_str}"


class AddressBook(UserDict):
    def add_record(self, record: Record) -> None:
        self.data[record.name.value] = record

    def find(self, name: str) -> Record | None:
        return self.data.get(name)

    def delete(self, name: str) -> None:
        self.data.pop(name, None)

    def get_upcoming_birthdays(self) -> list[dict[str, str]]:
        today = date.today()
        end_day = today + timedelta(days=7)

        result: list[dict[str, str]] = []

        for record in self.data.values():
            if record.birthday is None:
                continue

            bday = record.birthday.to_date()

            try:
                bday_this_year = bday.replace(year=today.year)
            except ValueError:
                continue

            if bday_this_year < today:
                try:
                    bday_this_year = bday.replace(year=today.year + 1)
                except ValueError:
                    continue

            if today <= bday_this_year:
                congrats = bday_this_year

                if congrats.weekday() == 5:
                    congrats +=timedelta(days=2)
                elif congrats.weekday() == 6:
                    congrats += timedelta(days=1)

                result.append(
                    {
                        "name": record.name.value,
                        "birthday": congrats.strftime("%d.%m.%Y"),
                    }
                )
        return result

    def __str__(self) -> str:
        if not self.data:
            return "No contacts saved."
        return "\n".join(str(record) for record in self.data.values())
