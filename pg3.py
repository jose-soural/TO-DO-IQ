from signal import signal
import json
from os import path
from os import remove
from datetime import date, timedelta
import heapq
today = date.today()
due = []
overdue = []
sleepers = []
finished_today = []
pulled = None
Pulled_list = []
displayed = None
displayed_list = []


def exit_without_saving():
def exit():
    """ Properly saves all data, closes and exits the program. """
    #TO-DO



def __create_file(frequency):
    with open(f'{frequency}.txt', "w", encoding="utf-8") as f:
        json.dump([], f)


def __delete_file(frequency):
    if path.exists(f'{frequency}.txt'):
        remove(f'{frequency}.txt')


def __pull_file(frequency):
    if path.exists(f'{frequency}.txt'):
        with open(f'{frequency}.txt', encoding="utf-8") as f:
            temp = json.load(f)
    else:
        __create_file(frequency)
        temp = []
    return temp


def __push_changes(frequency, contents):
    with open(f'{frequency}.txt', "w", encoding="utf-8") as f:
        json.dump(contents, f)


def __display_list(task_list):
    i = 1
    while i < (len(task_list) + 1):
        print(f'{i})', task_list[i-1]["name"], sep="   ")
        i += 1


def create_task(name, frequency="once", description="", status="unfinished"):
    new_task = {"name": name, "frequency": frequency, "description": description, "status": status}
    temp_list = __pull_file(frequency)
    temp_list.append(new_task)
    with open(f'{frequency}.txt', "w", encoding="utf-8") as f:
        json.dump(temp_list, f)
#    if status == "unfinished" and __viability(frequency):
#        add it to the list
    print(f'Task "{name}" successfully created!')


def delete_task(task_index):
    task = displayed_list[task_index - 1]
    freq = task["frequency"]
    temp = __pull_file(freq)
    temp.remove(task)
    __push_changes(freq, temp)

    displayed_list.pop(task_index - 1)
    __display_list(displayed_list)


def __to_date(days):
    delta = timedelta(days)
    return today + delta


def sleep_task(task_index, duration=0, until_date=today):
    duration = int(duration)
    if until_date <= today:
        if duration <= 0:
            print('Error: Please provide at least one valid attribute between "duration" or "until_date".')
            return
        else:
            until_date = __to_date(duration)
    task = displayed_list[task_index - 1]
    freq = task["frequency"]
    temp = __pull_file(freq)
    temp_task = temp[temp.index(task)]
    temp_task["status"] = "asleep"
    temp_task["until"] = until_date
    __push_changes(freq, temp)


# displayed_list.pop(task_index - 1)
# __display_list(displayed_list)
