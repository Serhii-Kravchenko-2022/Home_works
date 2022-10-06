contacts_dict = {}


def input_error(func):
    """
    function decorator - check input error

    :param func: function
    :return: function perform or error message
    """
    def wrapper(*args):
        try:
            return func(*args)
        except KeyError:
            return "Missing name in phone book"
        except TypeError:
            return "Wrong command. Try again!"
        except IndexError:
            return "Input name and phone"
        except ValueError as e:
            return e.args[0]
        except Exception as e:
            return e.args
    return wrapper


# handler functions:
def welcome():
    """
    Return 'How can I help you?'

    :return: str
    """
    return 'How can I help you?'


@input_error
def add_contact(user_contact):
    """
    Add name: phone_number to dictionary

    :param user_contact: str
    :return: str
    """
    if len(user_contact.split()) != 2:
        return "Must be two element's name and number after command! Try again"
    if not user_contact.split()[1].isnumeric():
        return 'Number must contain only numbers'
    name = user_contact.split()[0]
    phone_number = user_contact.split()[1]
    if name in contacts_dict:
        return f'Contact {name} already exists'
    contacts_dict[name] = phone_number
    return f'Contact {name} add to Phone book'


@input_error
def change_contact(user_contact):
    """
    Change phone_number for name in dictionary

    :param user_contact: str
    :return: str
    """
    if len(user_contact.split()) != 2:
        return "Must be two element's name and number after command! Try again"
    if not user_contact.split()[1].isnumeric():
        return 'Number must contain only numbers'
    name = user_contact.split()[0]
    phone_number = user_contact.split()[1]
    if name not in contacts_dict:
        return f'Contact {name} not in phone book'
    contacts_dict[name] = phone_number
    return f'Contact {name} phone number changed'


@input_error
def view_phone(user_contact):
    """
    Get phone number for name from dictionary

    :param user_contact: str
    :return: str
    """
    return f'{user_contact} phone number : {contacts_dict[user_contact]}' if user_contact in contacts_dict \
        else f'Missing name {user_contact} in phone book'


@input_error
def show_all():
    """
    Show all contacts from dictionary

    :return: str
    """
    return str(contacts_dict).replace('{', '').replace('}', '').replace(',', '\n').replace(' ', '').replace("'", ''). \
        replace(':', ': ') if contacts_dict else 'No contacts in phone book'


@input_error
def good_bay():
    """
    Return 'Good bye!'

    :return: str
    """
    return "Good bye!"


@input_error
def get_wrong_command():
    """
    Return message if get command does not exist
    """
    return 'Input wrong command, Try again'


command_dict = {'hello': welcome,
                'add': add_contact,
                'change': change_contact,
                'phone': view_phone,
                'show all': show_all,
                'good bye': good_bay,
                'close': good_bay,
                'exit': good_bay
                }


def get_command(command):
    """
    Return handler function from command dictionary, if command does not exist - return function
    get_wrong_command

    :command: str
    :return: str
    """
    return command_dict.get(command, get_wrong_command)


def command_check(user_input):
    """
    Check string for command from command dictionary and separate command

    :user_input: str
    :return: function get_command with command and user data
    """
    for command in command_dict:
        if command in ['show all', 'good bye']:
            if user_input.split()[:2] == command.split():
                user_command = command
                return get_command(user_command)()
        elif command in ['close', 'exit', 'hello']:
            if command == user_input:
                user_command = command
                return get_command(user_command)()
        else:
            if command == user_input.split()[0]:
                user_command = command
                user_contact = user_input.replace(user_command, '').strip()
                return get_command(user_command)(user_contact)
    return get_command(user_input)()


# main process
def main():
    """
    Main process

    :return: None
    """

    # print welcome instruction
    print("Hello user! It's CLI Bot. "
          "You must input 'command<space>name<space>number'\n"
          "Command list: ")
    for command in command_dict:
        print(command)
    while True:
        user_input = input('Enter your command: ').lower().strip()
        # check command in user input
        answer = command_check(user_input)
        # print result from handler functions
        print(answer)
        if answer == "Good bye!":
            break


if __name__ == '__main__':
    main()


