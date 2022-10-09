from collections import UserDict


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record


class Record:
    def __init__(self, name, phone=None):
        self.name = Name(name)
        if phone:
            self.phones = [Phone(phone)]
        else:
            self.phones = []

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def delete_phone(self, phone):
        phone_obj = Phone(phone)
        if phone_obj in self.phones:
            self.phones.remove(phone_obj)

    def change_phone(self, old_phone_number, new_phone_number):
        phone_obj = Phone(old_phone_number)
        if phone_obj in self.phones:
            self.phones[self.phones.index(phone_obj)] = Phone(new_phone_number)


class Field:
    def __init__(self, value):
        self.value = value


class Name(Field):
    ...


class Phone(Field):
    ...


contacts_dict = AddressBook()


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
        data = contacts_dict.data[name]
        data.add_phone(phone_number)
    else:
        data = Record(name, phone_number)
        contacts_dict.add_record(data)
    return f'Contact {name} add to Phone book'


@input_error
def change_contact(user_contact):
    """
    Change phone_number for name in dictionary

    :param user_contact: str
    :return: str
    """
    if len(user_contact.split()) != 3:
        return "Must be 3 element's name, old number and new number after command! Try again"
    if not user_contact.split()[1].isnumeric() and user_contact.split()[2].isnumeric():
        return 'Number must contain only numbers'
    name = user_contact.split()[0]
    old_phone_number = user_contact.split()[1]
    new_phone_number = user_contact.split()[2]
    if name not in contacts_dict:
        return f'Contact {name} not in phone book'
    data = contacts_dict.data[name]
    data.change_phone(old_phone_number, new_phone_number)
    return f'Contact {name} phone number {old_phone_number} changed on {new_phone_number}'


@input_error
def view_phone(user_contact):
    """
    Get phone number for name from dictionary

    :param user_contact: str
    :return: str
    """
    data = contacts_dict.data[user_contact]
    return f'{user_contact} phone numbers : ' + ', '.join([phone.value for phone in data.phones]) \
        if user_contact in contacts_dict else f'Missing name {user_contact} in phone book'


@input_error
def show_all():
    """
    Show all contacts from dictionary

    :return: str
    """
    all_data = ''
    for name, data in contacts_dict.items():
        all_data += name + ' ' + ', '.join([phone.value for phone in data.phones]) + '\n'
    return all_data if all_data else 'No contacts in phone book'


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


