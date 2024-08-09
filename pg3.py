import json
from os import path
from os import remove
from datetime import date
date_today = date.today()
due = []
overdue = []
sleepers = [None]
finished_today = []
current_file = None


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


def __push_file(frequency, contents):
    with open(f'{frequency}.txt', "w", encoding="utf-8") as f:
        json.dump(contents, f)


def create_task(name, frequency="once", description="", status="unfinished"):
    new_task = {"name": name, "description": description, "status": status}
    temp_list = __pull_file(frequency)
    temp_list.append(new_task)
    with open(f'{frequency}.txt', "w", encoding="utf-8") as f:
        json.dump(temp_list, f)
#    if status == "unfinished" and __viability(frequency):
#        add it to the list
    print(f'Task "{name}" successfully created!')


def __display_tasks(frequency, status="all"):
    temp = __pull_file(frequency)
    if status == "all":
        output = temp
    else:
        output = [item for item in temp if item["status"] == status]
    return output
