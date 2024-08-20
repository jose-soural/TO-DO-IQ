import json
from os import path
from os import remove
from datetime import date, datetime, timedelta

today = date.today()
config = {}

due = {"entries": {},"glossary": {}}
overdue = {"entries": {},"glossary": {}}
asleep = {"entries": {}, "glossary": {}}
finished_today = {"entries": {},"glossary": {}}
ordinary = {"once", "daily", "weekly", "monthly", "seasonally", "yearly"}
specific = {}
special = {due, overdue, asleep, finished_today}

ordering = {"once": 1, "daily": 2}      # specific dates should go in the front I guess
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
            temp = {"length": 0, "entries": {}, "glossary": {}}
        in_memory[f'{frequency}'] = temp
    return temp


def __delete_file(frequency):
    if path.exists(f'{frequency}.txt'):
        remove(f'{frequency}.txt')
    for collection in special:
        if f'{frequency}' in collection["entries"]:
            for task in collection["entries"][f'{frequency}'].values():
                del collection["glossary"][task["name"]]
            del collection["entries"][f'{frequency}']
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


def __add_to_special(task, collection):
    if (freq := task["frequency"]) not in collection["entries"]:
        collection["entries"][freq] = {"length": 0, "entries": {}, "glossary": {}}
    temp = collection["entries"][freq]
    temp["length"] += 1
    temp["entries"][temp["length"]] = task
    temp["glossary"][task["name"]] = temp["entries"][temp["length"]]



def __viability(frequency):
    if frequency in ordinary:
        return True
    return TO_DO


def __to_date(days):
    delta = timedelta(days)
    return today + delta


def create_task(name, frequency="once", description="", status="unfinished"):
    if status == "finished" and frequency == "once":
        print(f'Error: Cannot add a "once" task that is already finished. Task "{name}" was NOT created.')
        return
    new_task = {"name": name, "frequency": frequency, "description": description, "status": status}
    if status == "unfinished":
        if __viability(frequency):
            __add_to_special(new_task, due)
    elif status == "asleep":
        print("Putting task to sleep. Please input the date you would like the task to awaken on.")
        print("If you would like to give the number of days instead, type 'days'.")
        if (until := input(f'Type the date in the format {today}')) == "days":
            # converter code
        new_task["until"] = until
        __add_to_special(new_task, asleep)

    temp = __pull_file(frequency)
    temp["length"] += 1
    temp["entries"][temp["length"]] = new_task
    temp["glossary"][name] = temp["entries"][temp["length"]]
    in_memory[frequency] = temp
    changed[frequency] = True

    print(f'Task "{name}" was successfully created!')   # perhaps add to finished today if finished?
    return
