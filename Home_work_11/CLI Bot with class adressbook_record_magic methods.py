from collections import UserDict
from datetime import datetime
from re import findall


class DictIterator:
    def __init__(self, collection, number):
        self._collection = collection
        self._index = 0
        self._number = number

    def __next__(self):
        # create a dictionary from number amount of dictionary data for one iteration
        if self._index >= len(self._collection):
            raise StopIteration
        # iterate over the keys of the dictionary and create a list of keys
        key_list = list(self._collection.keys())
        # create empty dictionary
        result = {}
        # loop over part of list indexes in count number
        for i in range(self._index, self._index + self._number):
            # checking for data and matching list index
            if i < len(self._collection) and self._collection[key_list[i]]:
                result[key_list[i]] = self._collection[key_list[i]]
        # increment the index by number for the next iteration
        self._index += self._number
        return result

    def __iter__(self):
        return self


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def iterator(self, number):
        # return generator for number of data
        return DictIterator(self.data, number)


class Record:
    def __init__(self, name, phone=None, birthday=None):
        self.name = Name(name)
        if birthday:
            self.birth = Birthday(birthday)
        else:
            self.birth = Birthday('01.01.1970')
        if phone:
            self.phones = [Phone(phone)]
        else:
            self.phones = []

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def delete_phone(self, phone):
        for index, phone_obj in enumerate(self.phones):
            if phone_obj.value == phone:
                self.phones.remove(phone_obj)

    def change_phone(self, old_phone, new_phone):
        for index, phone in enumerate(self.phones):
            if phone.value == old_phone:
                self.phones[index] = Phone(new_phone)

    def days_to_birthday(self):
        #  calculating the number of days until a birthday
        if self.birth.value != '01.01.1970':
            data_str = self.birth.value.replace('.', ' ').replace(',', '.')
            current_datetime = datetime.now()
            birthday = datetime.strptime(data_str, '%d %m %Y')
            birthday = datetime(year=current_datetime.year, month=birthday.month, day=birthday.day)
            if birthday < current_datetime:
                birthday = datetime(year=birthday.year + 1, month=birthday.month, day=birthday.day)
            day_to_birthday = birthday - current_datetime
            return day_to_birthday.days
        return 'No birthday data'


class Field:
    def __init__(self, value):
        self.value = value


class Name(Field):
    ...


class Phone(Field):
    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_value):
        #  check phone value for numbers
        if new_value.isnumeric():
            self.__value = new_value
        else:
            print('Phone number must be numeric')
            raise TypeError


class Birthday(Field):
    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_value):
        # check birthday value for datatime rules
        if findall(r'(\d){2}[.,](\d){2}[.,](\d){4}', new_value):
            # if int(new_value.split('.')[0]) < 31 and int(new_value.split('.')[1]) <= 12:
            self.__value = new_value
        else:
            print('Birthday data must be dd.mm.yyyy')
            raise TypeError


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
    if len(user_contact.split()) >= 3:
        name = user_contact.split()[0]
        phone_number = user_contact.split()[1]
        birthday = user_contact.split()[2]
    elif len(user_contact.split()) == 2:
        name = user_contact.split()[0]
        phone_number = user_contact.split()[1]
        birthday = None
    else:
        return "Must be minimum two element's: 'name' and 'number' after command! Try again"
    if name in contacts_dict:
        data = contacts_dict.data[name]
        data.add_phone(phone_number)
    else:
        data = Record(name=name, phone=phone_number, birthday=birthday)
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
    return f'{user_contact} phone number(s) : ' + ', '.join([phone.value for phone in data.phones]) \
        if user_contact in contacts_dict else f'Missing name {user_contact} in phone book'


@input_error
def show_all():
    """
    Show all contacts from dictionary

    :return: str
    """
    all_data = ''
    quantity_data = 2  # quantity of data per iteration
    view_iteration = contacts_dict.iterator(quantity_data)  # Numbers of data on one page
    for one_page in view_iteration:
        all_data += '___________________\n'  # start on page
        for name, data in one_page.items():
            birth_data = data.birth.value if data.birth.value != '01.01.1970' else 'No data'
            all_data += name + ' ' + 'Phone(s): ' + ', '.join([phone.value for phone in data.phones]) + \
                ' Birthday: ' + birth_data + '\n'
        all_data += '___________________\n'  # end of page
    return all_data if all_data else 'No contacts in phone book'


@input_error
def get_day_to_birthday(user_contact):
    """
    Calculate days to birthday

    :param user_contact: str
    :return: str
    """
    name = user_contact.split()[0]
    if name not in contacts_dict:
        return f'Contact {name} not in phone book'
    data = contacts_dict.data[name]
    return f'{data.days_to_birthday()} days before birthday'


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
                'exit': good_bay,
                'birthday': get_day_to_birthday
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
    print("Hello user! \nIt's CLI Bot. \nFor add contact "
          "you must input \n'command<space>name<space>phone_number<space>birthday as dd.mm.yyyy'")

    while True:
        print("\nCommand list: ")
        for command in command_dict:
            print(f'"{command}" / ', end='')
        user_input = input('\nEnter your command: ').lower().strip()
        # check command in user input
        answer = command_check(user_input)
        # print result from handler functions
        print(answer)
        if answer == "Good bye!":
            break


if __name__ == '__main__':
    main()
