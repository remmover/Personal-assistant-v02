from datetime import datetime
from notebook import NOTE_BOOK, Text, Keyword, RecordNote
from adressbook import ADRESS_BOOK, Record, Name, Phone
from weather_and_bank import exchange_rates, show_weather
from sorter import main as sort_main
from dec import input_error


def hello():
    with open('personal_assistant/hello.txt', 'rb') as fh:
        text = fh.read().decode('utf-8')
    return text

def help():
    with open('personal_assistant/help.txt', 'rb') as fh:
        text = fh.read().decode('utf-8')
    return text

def sorter():
    sort_main()

def close():
    return 'До нових зустрічей!'

def load_contacts():
    contacts = ADRESS_BOOK.load_from_bin()
    if contacts:
        for key, value in contacts.items():
            ADRESS_BOOK.data[key] = value

def load_notes():
    notes = NOTE_BOOK.load_from_notebin()
    if notes:
        for key, value in notes.data.items():
            NOTE_BOOK.data[key] = value

def add_note():
    tag = Keyword(input('Введи теги через кому або залиш поле порожнім:\n>>> '))
    text = Text(input('Введи текст нотатки:\n>>> '))
    record = RecordNote(text=text, keyword=tag)
    return NOTE_BOOK.add_record(record)

def del_note():
    param = input('Введи тег для видалення нотатки:\n>>> ')
    return NOTE_BOOK.delete_note(param)

def search_note():
    param = input('Введи слово для пошуку у нотатнику:\n>>> ')
    return NOTE_BOOK.search(param)

def print_header_note():
    note_record, note_tag, note_text = 'Номер запису', 'Тег нотатки', 'Текст нотатки'
    print('-'*69)
    print('|{:^15}|{:^20}|{:^30}|'.format(note_record, note_tag, note_text))
    print('-'*69)

# def print_notes(note_record, note_tag, note_text):
    # print('|{:^15}|{:^20}|{:^30}|'.format(note_record, note_tag, note_text))

def show_notes():
    # print_header_note()
    data = NOTE_BOOK.show_all_notes()
    # note_data = data.split('\n')
    # print_notes(note_data[0], note_data[2], note_data[1])
    return data

def edit_note(notebook: NOTE_BOOK, note_name: str, new_text: str) -> str:
    for key, record in notebook.data.items():
        if note_name == key:
            record.edit_note(Text(new_text))
            return f"Текст нотатки '{note_name}' змінено на '{new_text}'"
    return f"Нотатку з ім'ям '{note_name}' не знайдено"

def edit_keyword(notebook: NOTE_BOOK, note_name: str, old_keyword: str, new_keyword: str) -> str:
    for key, record in notebook.data.items():
        if note_name == key:
            record.edit_keyword(Keyword(old_keyword), Keyword(new_keyword))
            return f"Тег нотатки '{note_name}' з '{old_keyword }' змінено на '{new_keyword}'"
    return f"Нотатку з ім'ям '{note_name}' не знайдено"

def note_book():
    while True:
        user_input = input('\nВітаю в меню нотатника!\n\
Я вмію додавати(команда add) нотатки за тегами;\n\
видаляти(команда del) та редугавати нотатки(команда edit);\n\
здіснювати пошук за тегами(команда search);\n\
а також можу показати усі збережені записи(команда show).\n\
\n\
Щоб перейти до головного меню обери команду menu.\n\
>>> ').lower() 
        match user_input:
            case 'add':
                print(add_note())        
            case 'del':
                print(del_note())            
            case 'edit':
                user_input = input('Що саме ти хочеш змінити? (тег чи текст нотатки)>>>')
                match user_input:
                    case 'тег':
                        name = input('name>>')
                        old_tag = input('old tag>>')
                        new_tag = input('new tag>>')
                        print(edit_keyword(NOTE_BOOK, name, old_tag, new_tag))
                    case 'текст':
                        name = input('name>>')
                        new_text = input('new_text>>')
                        print(edit_note(NOTE_BOOK, name, new_text))
            case 'search':
                print(search_note())
            case 'show':
                print(show_notes())
            case 'menu':
                NOTE_BOOK.save_to_notebin()
                main()
            case _:
                print('Вибач, але в нотатнику поки що немає такої команди.')

@input_error
def add_contact():
    name = Name(input('Введи ім\'я користувача>>> ').capitalize())
    phone = Phone(input('Введи номер телефону користувача починаючи с +38>>> '))
    rec = Record(name=name, phone=phone)
    return ADRESS_BOOK.add_record(rec)

def print_header_contact():
    name, phone, email, adres, bd = "Ім'я", 'Телефон', 'E-mail', 'Адреса', 'День народження'
    print('-'*146)
    print('|{:^20}|{:^35}|{:^25}|{:^45}|{:15}|'.format(name, phone, email, adres, bd))
    print('-'*146)

def print_contacts(name, phone, email, adres, bd):
    print('|{:^20}|{:^35}|{:^25}|{:^45}|{:^15}|'.format(name, phone, email, adres, bd))

def search_contact():
    search_input = input("Введи ім'я або телефон для пошуку\n>>> ").capitalize()
    for record in ADRESS_BOOK.values():
        if search_input in record.name.value or search_input in record.phone.value:
            name = record.name.value
            phones = ' '.join(record.phone.value)
            email = record.email.value if record.email else ''
            adres = record.address.value if record.address else ''
            bd = (record.birthday.value).strftime('"%d-%m-%Y"') if record.birthday else ''

            print_header_contact()
            print_contacts(name, phones, email, adres, bd)

def show_contact(record: Record):
    name = record.name.value
    phones = ' '.join(record.phone.value)
    email = record.email.value if record.email else ''
    adres = record.address.value if record.address else ''
    bd = (record.birthday.value).strftime('%d-%m-%Y') if record.birthday else ''

    print_contacts(name, phones, email, adres, bd)

def delete_contact_record():
    name = input("Введи ім'я контакту, котрого треба видалити\n>>> ").capitalize()
    for key, record in ADRESS_BOOK.items():    
        if key == name:
            return ADRESS_BOOK.del_record(record)
    return f'Контакту з іменем {name} не знайдено.'

def show_all_contacts():
    if ADRESS_BOOK.values():
        print_header_contact()
        for record in ADRESS_BOOK.values():
            show_contact(record)
    else:
        print('\nЯ поки що не знаю ніяких контактів.')

@input_error
def add_contact_info(name):
    values = ADRESS_BOOK[name]
    add_input = input('\nЩо я маю додати?\n\
    - телефон (команда phone);\n\
    - електронну пошту (команда email);\n\
    - день народження (команда bd);\n\
    - адресу (команда ad)\n\
>>> ')
    match add_input:
        case 'phone':
            user_input = input("Введи номер телефону у форматі +380123456789\n>>> ")
            return values.add_phone(user_input)
        case 'email':
            user_input = input('Введи електронну пошту\n>>> ')
            return values.add_email(user_input)
        case 'bd':
            user_input = input('Введи день народження контакту у форматі дд-мм-рррр\n>>> ')
            return values.add_birthday(user_input)
        case 'ad':
            user_input = input('Введи адресу\n>>> ')
            return values.add_address(user_input)
        case _:
            return '\nУ цьому меню така команда відсутня.\n'
    
@input_error
def del_contact_info(name):
    values = ADRESS_BOOK[name]
    del_input = input('\nЩо я маю видалити?\n\
    - телефон (команда phone);\n\
    - електронну пошту (команда email);\n\
    - день народження (команда bd);\n\
    - адресу (команда ad)\n\
>>> ')
    match del_input:
        case 'phone':
            user_input = input('Введи номер для видалення у форматі +380123456789\n>>> ')
            return values.delete_phone(user_input)
        case 'email':
            return values.delete_email()
        case 'bd':
            return values.delete_birthday()
        case 'ad':
            return values.delete_address()
        case _:
            return '\nУ цьому меню така команда відсутня.\n'

@input_error
def change_contact_info(name):
    values = ADRESS_BOOK[name]
    change_input = input('\nЩо я маю редагувати?\n\
    - телефон (команда phone);\n\
    - електронну пошту (команда email);\n\
    - день народження (команда bd);\n\
    - адресу (команда ad)\n\
>>> ')
    match change_input:
        case 'phone':
            phone_input = (input("Через кому введи старий та новий номер телефону у форматі +380633456789,+380501234567\n>>> ")).split(',')
            return values.change_phone(phone_input[0], phone_input[1])
        case 'email':
            email_input = input('Введи імейл користувача\n>>> ')
            return values.change_email(email_input)
        case 'bd':
            user_input = input('Введи день народження контакту у форматі дд-мм-рррр\n>>> ')
            return values.change_birthday(user_input)
        case 'ad':
            user_input = input('Введи адресу\n>>> ')
            return values.change_address(user_input)
        case _:
            return '\nУ цьому меню така команда відсутня.\n'

def edit_contact():
    contact_input = input("Введи ім'я контакта, дані якого хочеш змінити\n>>> ").capitalize()
    if contact_input in ADRESS_BOOK.keys():
        edit_input = input(f"\nЩо я маю робити з контактом {contact_input}?\n\
    - щось додати (команда add);\n\
    - щось редагувати (команда change);\n\
    - щось видалити (команда del)\n\
>>> ").lower()
        match edit_input:
            case 'change':
                return change_contact_info(contact_input)
            case 'add':
                return add_contact_info(contact_input)
            case 'del':
                return del_contact_info(contact_input)
            case _:
                return 'Такої команди я не знаю.'
    else:
        return f"Контакт з ім'ям {contact_input} не знайдено!"

def adress_book():
    while True:
        user_input = input('\nЩоб додати контакт введи add;\n\
видалити контакт за командою del;\n\
побачити книгу контактів за командою show;\n\
знайти інформацію по контакту за командою search;\n\
змінити інформацію існуючого контакту за командою edit.\n\
\n\
Щоб перейти до головного меню обери команду menu.\n\
>>> ').lower()
        
        match user_input:
            case 'add':
                print(add_contact())
            case 'del':
                print(delete_contact_record())
            case 'edit':
                print(edit_contact())
            case 'search':
                search_contact()
            case 'show':
                show_all_contacts()
            case 'menu':
                ADRESS_BOOK.save_to_bin()
                main()
            case _:
                print('Вибач, але в записній книзі немає такої команди.')

COMMANDS = {
    help: 'help',
    note_book: 'notes',
    sorter: 'sort',
    close: 'exit',
    adress_book: 'contacts',
    exchange_rates: 'valuta',
    show_weather: 'weather'
}

def no_command():
    return 'Вибач, але я поки що не знаю такої команди.'

def command_handler(text: str):
    for command, kword in COMMANDS.items():
        if text.startswith(kword):
            return command
    return no_command

def main():
    print(hello())
    load_contacts()
    load_notes()
    while True:
        user_input = input('\nТи у головному меню. Очікую команду від тебе:\n>>> ')
        command = command_handler(user_input)
        print(command())
        if command == close:
            raise SystemExit
            
if __name__ == '__main__':
    main()
