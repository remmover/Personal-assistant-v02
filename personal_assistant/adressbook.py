from abc import ABC, abstractmethod
from collections import UserDict
from datetime import datetime
import pickle
import re


class Abstract(ABC):

    @abstractmethod
    def value(self, data):
        pass


class Field(Abstract):
    def __init__(self, value) -> None:
        self._value = value

    @property
    def value(self):
        return self._value
    
    @value.setter
    def value(self, new_value) -> None:
        self._value = new_value


class Name(Field):
    def __init__(self, value) -> None:
        self.value = value
    
    @Field.value.setter
    def value(self, value: str) -> None:
        if not value:
            raise ValueError("Ім'я не може бути порожнім!")
        if not value.isalpha():
            raise ValueError("Ім'я повинно бути рядком, жодних чисел!")
        if value in ADRESS_BOOK:
            raise ValueError("Контакт з таким ім'ям вже існує!")
        self._value = value


class Phone(Field):
    def __init__(self, value):
        self.value = value

    @Field.value.setter
    def value(self, value):
        if bool(re.match(r'^\+380\d{9}$', value)):
            self._value = [value]
        else:
            raise ValueError('Номер телефону повинен бути у форматі +380123456789.')


class Email(Field):
    def __init__(self, value) -> None:
        self.value = value

    @Field.value.setter
    def value(self, value):
        if bool(re.match(r'[a-zA-Z][a-zA-Z0-9._]+@\w+\.[a-z]{2,}', value)):
            self._value = value
        else:
            raise ValueError('Електронна пошта може складатись з латинських символів, цифр та символів . та _')


class Birthday(Field):
    def __init__(self, value) -> None:
        self.value = value

    @Field.value.setter
    def value(self, value):
        try:
            datetime.strptime(value, "%d-%m-%Y")
            self._value = datetime.strptime(value, "%d-%m-%Y").date()
        except ValueError:
            raise ValueError("Дата неправильна. Повинно бути в форматі дд-мм-рррр.")
    

class Adress(Field):
    pass


class Record:
    def __init__(self, name: Name, phone: Phone, email: Email = None, birthday: Birthday = None, address: Adress = None) -> None:
        self.name = name
        self.phone = phone
        self.birthday = birthday
        self.email = email
        self.address = address

    def add_birthday(self, bd):
        if not self.birthday:
            self.birthday = Birthday(bd)
            return f'\nДля контакту {self.name.value} додано день народження {bd}.\n'
        return f'\nКонтакт {self.name.value} вже має день народження. Можливо ти хотів його змінити?\n'

    def add_email(self, email):
        if not self.email:
            self.email = Email(email)
            return f'\nДля контакту {self.name.value} додано e-mail {email}.\n'
        return f'\nКонтакт {self.name.value} вже має e-mail. Можливо ти хотів його змінити?\n'

    def add_phone(self, phone):
        if phone in self.phone.value:
            return f'\nКонтакт {self.name.value} вже має такий номер телефону.\n'
        self.phone.value.append(phone)
        return f'\nНомер телефону {phone} додано до контакту {self.name.value}.\n'
    
    def add_address(self, address):
        if not self.address:
            self.address = Adress(address)
            return f'\nДля контакту {self.name.value} додано адресу {address}.\n'
        return f'\nКонтакт {self.name.value} вже має адресу. Можливо ти хотів її змінити?\n'
    
    def change_address(self, address):
        if self.address:
            self.address =  Adress(address)
            return f'\nДля контакта {self.name.value} змінено адресу на {address}.\n'
        return f'\nЩоб змінити адресу, для початку не завадило б її додати :)\n'

    def change_birthday(self, bd):
        if self.birthday:
            self.birthday = Birthday(bd)
            return f'\nДля контакта {self.name.value} змінено день народження на {bd}.\n'
        return f'\nЩоб змінити день народження, для початку не завадило б його додати :)\n'
    
    def change_email(self, email):
        if self.email:
            self.email = Email(email)
            return f'\nДля контакта {self.name.value} змінено e-mail на {email}.\n'
        return f'\nЩоб змінити імейл, для початку не завадило б його додати :)\n'
    
    def change_phone(self, old_phone, new_phone):
        if old_phone in self.phone.value:
            self.phone.value.remove(old_phone)
            self.phone.value.append(new_phone)
            return f'\nУ контакта {self.name.value} телефон {old_phone} змінено на {new_phone}.\n'
        else:
            return f'\nТи впевнений, що саме цей номер {old_phone}? Я його не знайшов.\n'

    def delete_address(self):
        if self.address:
            self.address = None
            return f'\nУ контакта {self.name.value} видалено адресу.\n'
        return f'\nЯ впорався. У контакта {self.name.value} не було данних для видалення.\n'

    def delete_birthday(self):
        if self.birthday:
            self.birthday = None
            return f'\nЯ видалив день народження контакта {self.name.value}.\n'
        return f'\nЯ впорався. У контакта {self.name.value} не було данних для видалення.\n'

    def delete_email(self):
        if self.email:
            self.email = None
            return f'\nЯ видалив імейл контакта {self.name.value}.\n'
        return f'\nЯ впорався. У контакта {self.name.value} не було данних для видалення.\n'
        
    def delete_phone(self, phone):
        if phone in self.phone.value:
            self.phone.value.remove(phone)
            return f'\nЯ видалив {phone} у контакта {self.name.value}.\n'
        else:
            return f'\nТи впевнений, що саме цей номер {phone}? Я його не знайшов.\n'


    # def days_to_birthday(self, birthday):
    #     birthday = str(birthday)
    #     current_date = datetime.now().date()
    #     normal_date = datetime.strptime(birthday, '%d.%m.%Y').replace(
    #         year=current_date.year).date()
    #     days = (normal_date - current_date).days
    #     if days < 0:
    #         normal_date = datetime.strptime(birthday, '%d.%m.%Y').replace(
    #             year=current_date.year + 1).date()
    #         days = (normal_date - current_date).days
    #     self.records.append(f'days to BD = {days} ;')


    def __repr__(self):
        attrs = []
        attrs.append(f"{self.records}")
        return f"{', '.join(attrs)}"


class AddressBook(UserDict):
    def add_record(self, record: Record):
        name = record.name.value
        self.data[name] = record
        return f'Контакт {name} додано до записної книги.'
    
    def del_record(self, record: Record):
        name = record.name.value
        del ADRESS_BOOK[name]
        return f'Контакт {name} видалено з записної книги.'
    
    def save_to_bin(self, path="addressbook.bin"):
        with open(path, "wb") as f:
            pickle.dump(self.data, f)

    @staticmethod
    def load_from_bin(path="addressbook.bin"):
        try:
            with open(path, "rb") as f:
                return pickle.load(f)
        except FileNotFoundError:
            return ADRESS_BOOK
        except EOFError:
            return ADRESS_BOOK
        

ADRESS_BOOK = AddressBook()