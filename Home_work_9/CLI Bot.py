contacts_dict = {}


def input_error(func):
    """
    function decorator - check input error

    :param func: function
    :return: function perform or error message
    """
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
        except IndexError:
            return 'Type command <space> name <space> phone number again'
        return result
    return wrapper

# handler functions:
def welcome():
    """
    Return 'How can I help you?'

    :return: str
    """
    return 'How can I help you?'


@input_error
def add_contact(name, phone_number):
    """
    Add name: phone_number to dictionary

    :param name: str
    :param phone_number: str
    :return: str
    """
    if name in contacts_dict:
        return f'Contact {name} already exists'
    contacts_dict[name] = phone_number
    return f'Contact {name} add to Phone book'


@input_error
def change_contact(name, phone_number):
    """
    Change phone_number for name in dictionary

    :param name: str
    :param phone_number: str
    :return: str
    """
    if name not in contacts_dict:
        return f'Contact {name} not in phone book'
    contacts_dict[name] = phone_number
    return f'Contact {name} phone number changed'


def view_phone(user_contact):
    """
    Get phone number for name from dictionary

    :param user_contact: str
    :return: str
    """
    return f'{user_contact} phone number : {contacts_dict[user_contact]}' if user_contact in contacts_dict \
        else f'Missing name {user_contact} in phone book'


def show_all():
    """
    Show all contacts from dictionary

    :return: str
    """
    return str(contacts_dict).replace('{', '').replace('}', '').replace(',', '\n').replace(' ', '').replace("'", ''). \
        replace(':', ': ') if contacts_dict else 'No contacts in phone book'


def good_bay():
    """
    Return 'Good bye!'

    :return: str
    """
    return "Good bye!"


# main process
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
    print("Hello user! It's CLI Bot. "
          "You must input 'command<space>name<space>number'\n"
          "Command list: ")
    for command in command_dict:
        print(command)
    while True:
        user_command = ''
        user_contact = ''
        user_input = input('Enter your command: ').lower()
        # check command in user input
        for command in command_dict:
            if command in ['show all', 'good bye']:
                if user_input.split()[:2] == command.split():
                    user_command = command
            else:
                if command == user_input.split()[0]:
                    user_command = command
                    user_contact = user_input.replace(user_command, '').strip()
        if not user_command:
            print('Input wrong command, Try again')
        # print result from handler functions
        if user_command in ['add', 'change', 'phone']:
            print(command_dict[user_command](user_contact))
        if user_command in ['hello', 'show all']:
            print(command_dict[user_command]())
        if user_command in ['good bye', 'close', 'exit']:
            print(command_dict[user_command]())
            break


if __name__ == '__main__':
    main()
