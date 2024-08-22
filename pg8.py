import json
from os import path
from os import remove
from datetime import date, datetime, timedelta
import dltl

today = date.today()
now = datetime.now()
config = {}

due = dltl.DLTL
overdue = dltl.DLTL
asleep = dltl.DLTL
finished_today = {"frequencies": {}, "glossary": {}}

ordinary = {"once", "daily", "weekly", "monthly", "seasonally", "yearly"}
week = {"monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"}
specific = {}
special = {due, overdue, asleep, finished_today}

ordering = {"once": 1, "daily": 2}      # specific dates should go in the front I guess
in_memory = {}
changed = {}
last_displayed = {"source": due, "frequency": all}


def _pull_file(frequency):
    if f'{frequency}' in in_memory:
        temp = in_memory[f'{frequency}']
    else:
        if path.exists(f'{frequency}.txt'):
            with open(f'{frequency}.txt', encoding="utf-8") as f:
                temp = json.load(f)
        else:
            temp = dltl.DLTL
    return temp


def _delete_file(frequency):
    if path.exists(f'{frequency}.txt'):
        remove(f'{frequency}.txt')
    for collection in special:
        task_list = collection["frequencies"].pop([f'{frequency}'], None)
        if task_list:
            current = task_list.head
            for _ in range(task_list.size):
                del collection["glossary"][current.name]
                current = current.next

    changed.pop(f'{frequency}', None)


def _push_file(frequency, contents):  # might rewrite later to automatically take contents from in_memory,
    # we'll see

    with open(f'{frequency}.txt', "w", encoding="utf-8") as f:
        json.dump(contents, f)
    changed.pop(f'{frequency}', None)


def save_changes():
    if changed.pop("special", False):
        _push_file("special", special)
    if changed.pop("config", False):
        _push_file("config", config)
    for frequency in list(changed.keys()):
        _push_file(frequency, in_memory[frequency])


# here I ought to add the two EXIT functions.

def _add_to_special(task, collection):
    if (freq := task["frequency"]) not in collection["frequencies"]:
        collection["frequencies"][freq] = dltl.DLTL
    collection["frequencies"][freq].append_task(task)


def _viability(frequency):
    if frequency in ordinary:
        return True
    elif frequency in week:
        if frequency == now.strftime('%A'):
            return True
    elif frequency in specific:
        if frequency == today:
            return True
            # like many other things where I am working with "dates" but actually strings, this won't work properly
    return False


def _to_date(days):
    delta = timedelta(days)
    return today + delta


def create_task(name, frequency="once", description="", status="unfinished"):
    frequency = frequency.casefold()
    if status == "finished" and frequency == "once":
        print(f'Error: Cannot add a "once" task that is already finished. Task "{name}" was NOT created.')
        return
    new_task = {"name": name, "frequency": frequency, "description": description, "status": status}
    if status == "unfinished":
        if _viability(frequency):
            _add_to_special(new_task, due)
    elif status == "asleep":
        print("Putting task to sleep. Please input the date you would like the task to awaken on.")
        print("If you would like to give the number of days instead, type 'days'.")
        if (until := input(f'Type the date in the format {today}')) == "days":
            until = _to_date(until)
        new_task["until"] = until
        _add_to_special(new_task, asleep)

    temp = _pull_file(frequency)
    temp.append_task(new_task)
    in_memory[frequency] = temp
    changed[frequency] = True

    print(f'Task "{name}" was successfully created!')   # perhaps add to finished today if finished?
    return

def _target_task_in_special(user_input):
    ld = last_displayed

def _target_task(user_input):
    ld = last_displayed
    if ld["source"] in special:
        if ld["frequency"] == "all":
            task = _target_task_in_special(user_input)
        else:
            temp = ld["source"]["frequencies"].get(["frequency"])
    else:
        temp = _pull_file(ld["source"])

    if user_input.isdigit():
        task = temp.fetch_node_at_position(user_input, ).task
    else:
        task = temp.fetch_task(user_input)
    return task
