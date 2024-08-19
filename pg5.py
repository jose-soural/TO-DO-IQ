import json
from os import path
from os import remove
from datetime import date  # , timedelta

today = date.today()
config = {}
due = [{}, {}]
overdue = [{}, {}]
sleepers = [{}, {}]
finished_today = [{}, {}]
special = [due, overdue, sleepers, finished_today]
in_memory = {}
changed = {}
displayed = None
displayed_list = [{}, {}]


def __pull_file(frequency):
    if f'{frequency}' in in_memory:
        temp = in_memory[f'{frequency}']
    else:
        if path.exists(f'{frequency}.txt'):
            with open(f'{frequency}.txt', encoding="utf-8") as f:
                temp = json.load(f)
        else:
            temp = [0, {}, {}]
        in_memory[f'{frequency}'] = temp
    return temp


def __delete_file(frequency):
    if path.exists(f'{frequency}.txt'):
        remove(f'{frequency}.txt')
    for collection in special:
        if f'{frequency}' in collection[0]:
            for task in collection[0][f'{frequency}'].values():
                del collection[1][task["name"]]
            del collection[0][f'{frequency}']
    changed.pop(f'{frequency}', False)
    global displayed, displayed_list
    if displayed == f'{frequency}':     # is this actually necessary?
        displayed = None
        displayed_list = [{}, {}]


def __push_file(frequency, contents):        # might rewrite later to automatically take contents from in_memory,
    # we'll see

    with open(f'{frequency}.txt', "w", encoding="utf-8") as f:
        json.dump(contents, f)
    changed.pop(f'{frequency}', False)


def save_changes():
    if changed.pop("special", False):
        __push_file("special", special)
    if changed.pop("config", False):
        __push_file("config", config)
    for frequency in list(changed.keys()):
        __push_file(frequency, in_memory[frequency])

# here I ought to add the two EXIT functions.

def create_task(name, frequency="once", description="", status="unfinished"):
    new_task = {"name": name, "frequency": frequency, "description": description, "status": status}
    temp_list = __pull_file(frequency)
    temp_list.append(new_task)
    with open(f'{frequency}.txt', "w", encoding="utf-8") as f:
        json.dump(temp_list, f)
#    if status == "unfinished" and __viability(frequency):
#        add it to the list
    print(f'Task "{name}" successfully created!')
