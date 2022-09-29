CONTACTS = {}
user_instruction = 'Instruction'


def input_error(func):
    def wrapper(user_contact):
        if len(user_contact.split()) != 2:
            return "Must be two element's name and number after command! Try again"
        if not user_contact.split()[1].isnumeric():
            return 'Number must contain only numbers'
        name = user_contact.split()[0]
        phone_number = user_contact.split()[1]
        try:
            result = func(name, phone_number)
        except KeyError:  # KeyError, ValueError, IndexError
            return 'Missing name in phone book'
        except ValueError:
            return 'too many values to unpack'
        except IndexError:
            return 'Type command <space> name <space> phone number again'
        return result
    return wrapper


def welcome():
    return 'How can I help you?'


@input_error
def add_contact(name, phone_number):
    if name in CONTACTS:
        return f'Contact {name} already exists'
    CONTACTS[name] = phone_number
    return f'Contact {name} add to Phone book'


@input_error
def change_contact(name, phone_number):
    if name not in CONTACTS:
        return f'Contact {name} not in phone book'
    CONTACTS[name] = phone_number
    return f'Contact {name} phone number changed'


def view_phone(user_contact):
    return f'Phone number {user_contact}: {CONTACTS[user_contact]}' if user_contact in CONTACTS \
        else f'Missing name {user_contact} in phone book'


def show_all():
    return str(CONTACTS).replace('{', '').replace('}', '').replace(',', '\n').replace(' ', '').replace("'", ''). \
        replace(':', ': ') if CONTACTS else 'No contacts in phone book'


def good_bay():
    return "Good bye!"


def main():
    """
    Main process
    :return: None
    """
    command_dict = {'hello': welcome,
                    'add': add_contact,
                    'change': change_contact,
                    'phone': view_phone,
                    'show all': show_all,
                    'good bye': good_bay,
                    'close': good_bay,
                    'exit': good_bay
                    }
    # print welcome instruction
    print(user_instruction)
    while True:
        user_command = ''
        user_contact = ''
        user_input = input('Enter your command: ').lower()
        for command in command_dict:
            if command in user_input:
                user_command = command
                user_contact = user_input.replace(user_command, '').strip()
        if not user_command:
            print('Input wrong command, Try again')
        if user_command in ['add', 'change', 'phone']:
            print(command_dict[user_command](user_contact))
        if user_command in ['hello', 'show all']:
            print(command_dict[user_command]())
        if user_command in ['good bye', 'close', 'exit']:
            print(command_dict[user_command]())
            break


if __name__ == '__main__':
    main()
