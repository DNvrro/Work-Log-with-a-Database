#!/usr/bin/env python3

from collections import OrderedDict
import datetime
import os
import sys

from peewee import *

db = SqliteDatabase('diary.db')


class Entry(Model):
    employee_name = CharField(max_length=100)
    task_name = TextField()
    task_time = TextField()
    completion_date = DateField(formats=["%m/%d/%Y"])
    notes = TextField()
    timestamp = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = db


def initialize():
    """Create the database and table if they don't exist"""
    db.connect()
    db.create_tables([Entry], safe=True)


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def menu_loop():
    """Show the menu"""
    choice = None

    while not choice:
        clear()
        print('Welcome to Work Log DB')
        for key, value in menu.items():
            print('{}) {}'.format(key, value.__doc__))
        choice = input('\nWhat would you like to do?\n> ').lower().strip()

        if choice in menu:
            clear()
            menu[choice]()
        else:
            print("That is not a valid choice. Please try again")
            menu_loop()

def quit_program():
    """Quit the application"""
    print("Thank you for using Work Log DB. Goodbye.")
    exit()

def add_entry():
    """Add an entry"""
    entry = ''

    while True:
        employee_name = input('Enter your name:\n ').strip()
        task_name = input('The name of your task:\n ').strip()
        task_time = time_format(input('Time '
                             'spent on the task '
                                      '(Rounded in minutes):\n ')).strip()
        completion_date = date_format(input(''))

        notes = input('Additional notes (optional):\n ').strip()


        break



    if input('Save entry? [Y/n]').lower() != 'n':
        Entry.create(employee_name=employee_name, task_name=task_name,
                     task_time=task_time, notes=notes)
        print("Saved!")
        menu_loop()
    else:
        print('Your entry was not saved.')
        menu_loop()


def view_entries(column=None, query=None):
    """View previous entries"""

    entries = Entry.select().order_by(Entry.timestamp.desc())
    entries = entries.where(column.contains(query))

    cnt = 1
    for entry in entries:
        timestamp = entry.timestamp.strftime('%B %d, %Y %I:%M%p')
        clear()
        print(timestamp)
        print('=' * len(timestamp))
        print('Result {} of {}'.format(cnt, len(entries)))
        print('Employee: {}'.format(entry.employee_name))
        print('Task: {}'.format(entry.task_name))
        print('Task Time (Minutes): {}'.format(entry.task_time))
        print('Notes: {}'.format(entry.notes))
        print('=' * len(timestamp))
        print('n) next entry')
        print('d) delete entry')
        print('e) edit entry')
        print('q) return to main menu')
        cnt += 1

        next_action = input('\n> ').lower().strip()
        if next_action == 'q':
            menu_loop()
            break
        elif next_action == 'd':
            delete_entry(entry)
            print('Entry deleted!')
        elif next_action == 'e':
            edit_entry(entry, column, query)
            print("Your entry has been updated!")

    menu_loop()





def search_entries():
    """Search for an entry"""

    search_options = {'a': search_employee, 'b': search_date,
                      'c': search_time, 'd': search_term}

    search_choice = input('What would you like to search by?'
                          '\na) Employee Name'
                          '\nb) Entry Date'
                          '\nc) Task Duration'
                          '\nd) Search term'
                          '\n> ')
    try:
        choice = search_options[search_choice]
        clear()

    except KeyError:
        input("That is not a valid choice. Please try again \n")
        search_entries()
        clear()
    else:
        choice()
        clear()
    # view_entries(input('Search query: '))


def search_employee():
    employees = [employee.employee_name for employee in
                 Entry.select().order_by(Entry.timestamp.desc())]

    cnt = 1
    print('\n' + '=' * 60)
    for name in employees:
        print(str(cnt) + '. ' + name)
        cnt += 1

    choice = None
    while not choice:
        choice = input('\nPlease enter the name of the employee you wish'
                       ' to view entries from.\n>')
        if choice in employees:
            view_entries(Entry.employee_name, choice)
        else:
            choice = None



def search_date():
    dates =[date.timestamp for date in Entry.select()
        .order_by(Entry.timestamp.desc())]
    new_dates = []
    for date in dates:
        d = datetime.datetime.strptime(str(date),'%Y-%m-%d %H:%M:%S.%f')
        new_date = d.strftime('%B %d, %Y %I:%M%p')
        new_dates.append(new_date)

    cnt =  1
    print('\n' + '=' * 60)
    for date in new_dates:
        print(str(cnt) + '. ' + str(date))
        cnt += 1

    choice = None
    while not choice:
        choice = input("Enter the number coresponding to the date you "
                          "would like to search \nor enter 'q' to return to "
                          "the search menu:\n>").lower().strip()
        if choice == 'q':
            search_entries()
        else:
            try:
                choice = int(choice)
            except ValueError:
                choice = input('Please enter a valid number: \n>')
    view_entries(Entry.timestamp, dates[choice - 1])







def search_time():
    times = [time.task_time for time in Entry.select()
        .order_by(Entry.timestamp.desc())]

    choice = input("What duration of time would you like to search? \n>")
    if choice in times:
        view_entries(Entry.task_time, choice)
    else:
        print('There are no entries with that duration of time.'
              'Please try another time\n')
        search_time()

def search_term():
    search = input('What term would you like to search for? \n>').strip()
    choice = input('Would you like to search [t]ask or '
                   ' [n]otes? \n>').lower()

    checked = True
    while checked:
        try:
            choice == 't' or 'n'
            checked = False
        except ValueError:
            choice = input('Please enter [t]ask or [n]otes '
                           'to pick from where to search: ')

    entries1 = [task.task_name for task in Entry.select()
        .where(Entry.task_name.contains(search))]

    entries2 = [notes.notes for notes in Entry.select().
        where(Entry.notes.contains(search))]


    if choice == 't':
        if len(entries1) >= 1:
            view_entries(Entry.task_name, search)

    elif choice == 'n':
        if len(entries2) >= 1:
            view_entries(Entry.notes, search)

    else:
        print('There is no such term in the database.')
        search_entries()



def delete_entry(entry):
    """Delete an entry"""
    if input('Are you sure? [Y/N] ').lower() == 'y':
        entry.delete_instance()

def edit_entry(entry, column, query):

    choice = input('What part of the entry would you like to edit?'
                          '\na) Task'
                          '\nb) Task Time'
                          '\nc) Date'
                          '\nd) Notes'
                          '\n> ').lower().strip()

    if choice == 'a':
        new_task = input("Please enter a new task name: ")
        new_new = entry.update(task_name=new_task).\
            where(column.contains(query)).execute()
    elif choice == 'b':
        new_time = time_format(input("Please enter a new time duration: "))
        new_new = entry.update(task_time=new_time).\
            where(column.contains(query)).execute()
    elif choice == 'c':
        new_date =




    elif choice != 'a' or 'b' or 'c':
        print('Please choose from the menu (a/b/c).')
        edit_entry()




def date_format(date):
    """Checks that the user has entered
        a date in the specified format
    """

    formatted = True
    task_date = date
    while formatted:
        try:
            datetime.datetime.strptime(task_date, "%m/%d/%Y")
            formatted = False
            clear()
        except ValueError:
            clear()
            task_date = input(
                "Sorry. That is not a valid date. Please enter a date "
                "in the MM/DD/YYYY format: \n>")


def time_format(time):
    """Verifies that the user has entered the time spent in a rounded
    minutes format
    """
    task_time = time
    formatted = True
    while formatted:
        try:
            int(task_time)
            formatted = False
            clear()
        except ValueError:
            clear()
            task_time = input("Please submit the time in rounded minutes: \n>")
    return task_time


menu = OrderedDict([
    ('a', add_entry),
    ('s', search_entries),
    ('q', quit_program)

])

if __name__ == '__main__':
    initialize()
    menu_loop()
