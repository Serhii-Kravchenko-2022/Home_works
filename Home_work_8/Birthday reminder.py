from calendar import monthcalendar
from collections import defaultdict
from datetime import timedelta
from datetime import datetime as dt
from random import choice, randint


NAMES = """Liam Noah Oliver William Elijah James Benjamin Lucas Mason Ethan Alexander Henry Jacob Michael Daniel Logan 
            Jackson Sebastian Jack Aiden Owen Samuel Matthew Joseph Levi Olivia Emma Ava Sophia Isabella Charlotte 
            Amelia Mia Harper Evelyn Abigail Emily Ella Elizabeth Luna Sofia Avery Aria Scarlett Penelope Chloe 
            Victoria Madison Eleanor Grace
        """


def create_birthday_list_dict(names: list, colleague_quantity: int):
    """
    Create random list of quantity dictionaries {"Name": date}
    :param names: str
    :param colleague_quantity: int
    :return: list of dictionaries {'name'(:str): data(datatime)}
    """
    result_list_dict = []
    for i in range(colleague_quantity):
        # create random date from 01.01.2005 to 01.01.2022
        # date = dt(year=randint(2005, 2022), month=randint(1, 12), day=randint(1, 28))
        date = dt(year=2022, month=9, day=randint(24, 30))
        # choice random name from names
        name = choice(names)
        result_list_dict.append({'name': name, "birthday": date})
    # print('result_list_dict', result_list_dict)
    return result_list_dict


def get_first_week_day(date: dt):
    """
    Gets the first day of the current week

    :return: datatime
    """
    delta_week_day = 0
    # Get week list pet month
    month_list = monthcalendar(date.year, date.month)
    for week_list in month_list:
        # if date in day's week list - get day's delta to first week day
        if date.day in week_list:
            delta_week_day = week_list.index(date.day)
    result_date = date - timedelta(days=delta_week_day)
    return result_date


def get_birthdays_per_week(users: list, date: dt):
    """
    Print user's names with birthdays one week ahead of the current week

    :param date: datetime current day
    :param users: list of users dictionaries
    :return: print list of dictionaries {day: list names}
    """
    # create dictionary of day's name
    days_names = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday', 4: 'Friday', 5: 'Saturday', 6: 'Sunday'}
    result_list_lists = []
    # determine the billing period
    first_period_day = get_first_week_day(date) - timedelta(days=2)
    last_period_day = get_first_week_day(date) + timedelta(days=5)
    first_week_day = get_first_week_day(date)
    # create list lists with
    for user in users:
        result_list = []
        if last_period_day > user['birthday'] >= first_week_day:
            # result_dict[days_names[user['birthday'].weekday()]] = user['name']
            result_list.append(days_names[user['birthday'].weekday()])
            result_list.append(user['name'])
            result_list_lists.append(result_list)
        if first_week_day > user['birthday'] >= first_period_day:
            result_list.append('Monday')
            result_list.append(user['name'])
            result_list_lists.append(result_list)
    if not result_list_lists:
        print('We have no Birthday on this week')
        exit()
    # create dictionary with user's name per week day
    users_per_week = defaultdict(list)
    for week_dey, names in result_list_lists:
        users_per_week[week_dey].append(names)
    sorted(users_per_week.items())
    # print result user's list
    for index, day_name in days_names.items():
        if index < 5:
            print(day_name, end=': ')
            print(str(users_per_week[day_name])[1:-1].replace("'", ''))


def main():
    """
    Main process
    :return: None
    """
    # calc next week day from day now
    needle_day = dt.now() + timedelta(days=7)
    # create users list with quantity dictionaries with keys 'name', 'birthday'
    names_list = NAMES.split()
    users_list = create_birthday_list_dict(names_list, 50)
    # print list colleague's birthday per day, if it on weekend - print them on Monday
    get_birthdays_per_week(users_list, needle_day)


if __name__ == '__main__':
    main()
