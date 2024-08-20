import json
from os import path
from os import remove
from sys import exit
from datetime import date #, timedelta

today = date.today()
due = {[{},{}]}
overdue = {[{},{}]}
sleepers = [{},{}]
sleepers_heap = []
finished_today = []
in_memory = {}
changed = {}
pulled = None
pulled_list = [{},{}]
displayed = None
last_displayed = [{}, {}]


def __create_file(frequency):       #might not be necessary in the end lol
    with open(f'{frequency}.txt', "w", encoding="utf-8") as f:
        json.dump([0,{},{}], f)


def __delete_file(frequency):
    if path.exists(f'{frequency}.txt'):
        remove(f'{frequency}.txt')
    #need to remove it from the changed list as well
    #need to remove all tasks of this frequency from all lists


def __pull_file(frequency):
    global pulled_list, pulled
    if path.exists(f'{frequency}.txt'):
        with open(f'{frequency}.txt', encoding="utf-8") as f:
            temp = json.load(f)
    else:
        temp = [0,{},{}]
    in_memory[f'{frequency}'] = temp
    pulled_list = temp
    pulled = frequency
    return temp


def __push_changes(frequency, contents):
    with open(f'{frequency}.txt', "w", encoding="utf-8") as f:
        json.dump(contents, f)      #do I want to remove them from the changed list?


def save_changes():
    for frequency in changed:
        __push_changes(frequency, in_memory[frequency])     #here I want to empty the changed list


def exit_without_saving():

# TO-DO
    # actually close the program -- (via encasing it in a function/loop and breaking it upon this request?)
    # just look up how to do it


def exit_app():
    """ Properly saves all data, closes and exits the program. """
    save_changes()
    exit_without_saving()

