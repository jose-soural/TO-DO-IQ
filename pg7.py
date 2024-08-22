import json
from os import path
from os import remove
from datetime import date, datetime, timedelta
import dltl

today = date.today()
now = datetime.now()
config = {}

due = {"frequencies": {}, "glossary": {}, "ordering": []}
overdue = {"frequencies": {}, "glossary": {}, "ordering": []}
asleep = {"frequencies": {}, "glossary": {}, "ordering": []}
finished_today = {"frequencies": {}, "glossary": {}, "ordering": []}

ordinary = {"once", "daily", "weekly", "monthly", "seasonally", "yearly"}
week = {"monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"}
specific = {}
special = {due, overdue, asleep, finished_today}
ordering_key = {"once": 1, "daily": 2}      # specific dates should go in the front I guess

in_memory = {}
changed = {}
last_displayed = {}


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

        collection["ordering"].append(freq)
        i = 0
        while ordering_key[collection["ordering"][i]] < ordering_key[freq]:     # the search could be optimized, but the insert below negates any reason to
            i += 1
        collection["ordering"].insert(i, freq)
        collection["ordering"].pop()

    collection["frequencies"][freq].append_task(task)
    collection["glossary"][task["name"]] = task


def _remove_from_special(task, collection):
    del collection["glossary"][task["name"]]
    temp = collection["frequencies"][task["frequency"]]
    temp.remove_task(task["name"])
    if temp.size == 0:
        del collection["frequencies"][task["frequency"]]
        collection["ordering"].remove(task["frequency"])


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


def create_task(name, frequency="once", description="", status="unfinished"):       # Maybe special treatment for "once" tasks?
    frequency = frequency.casefold()
    if status == "finished" and frequency == "once":
        print(f'Error: Cannot add a "once" task that is already finished. Task "{name}" was NOT created.')
        return
    temp = _pull_file(frequency)
    if name in temp.glossary:
        print(f'Error: Task with name {name} and frequency {frequency} already exists. Task was NOT created.')
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

    temp.append_task(new_task)
    in_memory[frequency] = temp
    changed[frequency] = True

    print(f'Task "{name}" was successfully created!')   # perhaps add to finished today if finished?
    return


def _target_task_in_special(digit_input):
    i = 0
    while digit_input > (temp := last_displayed["frequencies"][last_displayed["ordering"][i]]).size:
        digit_input = digit_input - temp.size
        i += 1
    return temp.fetch_node_at_position(digit_input).task


def _target_task(user_input):
    if user_input.isdigit():
        if last_displayed in special:
            return _target_task_in_special(user_input)
        else:
            return last_displayed.fetch_node_at_position(user_input).task
    else:
        return last_displayed["glossary"][user_input]


def delete_task(task):
    task = _target_task(task)
    frequency = task["frequency"]

    temp = _pull_file(frequency)
    temp.remove_task(task["name"])
    in_memory[frequency] = temp
    changed[frequency] = True

    for collection in special:
        if task["name"] in collection["glossary"]:
            _remove_from_special(task, collection)


def change_frequency(task, new_frequency):      # Add the case, where he changes it to once (and it's finished)
    task = _target_task(task)
    old_frequency = task["frequency"]
    task["frequency"] = new_frequency

    temp = _pull_file(old_frequency)
    temp.remove_task(task["name"])
    in_memory[old_frequency] = temp
    changed[old_frequency] = True

    temp = _pull_file(new_frequency)
    temp.append_task(task["name"])
    in_memory[new_frequency] = temp
    changed[new_frequency] = True

    for collection in special:
        if task["name"] in collection["glossary"]:
            _remove_from_special(task, collection)
            _add_to_special(task, collection)


def change_description(task, new_description):
    task = _target_task(task)
    frequency = task["frequency"]

    temp = _pull_file(frequency)
    temp.fetch_task(task["name"])["description"] = new_description
    in_memory[frequency] = temp
    changed[frequency] = True

    for collection in special:
        if task["name"] in collection["glossary"]:
            collection["glossary"][task["name"]]["description"] = new_description


def set_asleep(task):
    task = _target_task(task)
    frequency = task["frequency"]

    print("Putting task to sleep. Please input the date you would like the task to awaken on.")
    print("If you would like to give the number of days instead, type 'days'.")
    if (until := input(f'Type the date in the format {today}')) == "days":
        until = _to_date(until)

    temp = _pull_file(frequency)
    task = temp.fetch_task(task["name"])
    task["status"] = "asleep"
    task["until"] = until
    in_memory[frequency] = temp
    changed[frequency] = True

    for collection in special:
        if task["name"] in collection["glossary"]:
            _remove_from_special(task, collection)
    _add_to_special(task, asleep)
