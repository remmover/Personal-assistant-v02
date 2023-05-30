from functions import command_handler, close, hello, load_contacts, load_notes


def main():
    while True:
        user_input = input(
            '\nТи у головному меню. Очікую команду від тебе:\n>>> ')
        command = command_handler(user_input)
        print(command())
        if command == close:
            raise SystemExit


if __name__ == '__main__':
    print(hello())
    load_contacts()
    load_notes()
    main()
