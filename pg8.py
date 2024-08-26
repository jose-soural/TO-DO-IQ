import json
from os import path
from os import remove
from datetime import date, datetime, timedelta
import dltl

today = date.today()
now = datetime.now()
empty_list = dltl.DLTL()

config = {"last_refresh": date(2024, 8, 20),
          "ordering_key": {"once": 1, "daily": 2}}
# specific dates should go in the front I guess

due = {"frequencies": {}, "glossary": {}, "ordering": []}
overdue = {"frequencies": {}, "glossary": {}, "ordering": []}
finished_today = {"frequencies": {}, "glossary": {}, "ordering": []}
asleep = dltl.SleeperDLTL()

ordinary = {"once", "daily", "weekly", "monthly", "seasonally", "yearly"}
week = {"monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"}
seasons = {"winter", "spring", "summer", "fall"}

counting = {}
dates = {}
special = {"due": due, "overdue": overdue, "finished_today": finished_today}

in_memory = {}
changed = {}
last_displayed = None


def _pull_file(frequency):
    """Not meant for the end user. Pulls the desired file into memory (if it exists), or returns an empty DLTL."""
    if frequency in in_memory:
        temp = in_memory[frequency]
    else:
        if path.exists(f'{frequency}.txt'):
            with open(f'{frequency}.txt', encoding="utf-8") as f:
                temp = json.load(f)
        else:
            temp = dltl.DLTL()
        in_memory[frequency] = temp
    return temp


def _delete_file(frequency):
    """Not meant for the end user. Permanently deletes the specified file and all the tasks in it."""
    if path.exists(f'{frequency}.txt'):
        remove(f'{frequency}.txt')
    for collection in special:
        task_list = collection["frequencies"].pop(frequency, None)
        if task_list is not None:
            current = task_list.head
            for _ in range(task_list.size):
                del collection["glossary"][current.name]
                #Deletes the node itself
                next = current.next
                del current
                current = next
                current = current.next
    
    current = sleepers.head
    while current is not None:
        next = current.next
        if current.task["frequency"] == frequency:
            del asleep["glossary"][current.task["name"]]        # Actually, I can do this through dltl methods!
            _remove_node(current)
    sleepers
    task_list = collection["frequencies"].pop(frequency, None)

    changed.pop(frequency, None)


def _push_file(frequency, contents):  # might rewrite later to automatically take contents from in_memory,
    """Not meant for the end user. Pushes the current state of the given task list into the corresponding file."""
    # we'll see
    if contents == empty_list:     # Protects from saving an empty task list
        _delete_file(frequency)
    else:
        with open(f'{frequency}.txt', "w", encoding="utf-8") as f:
            json.dump(contents, f)
    changed.pop(frequency, None)


def save_changes():
    """Saves all changes and progress made to all tasks and configurations."""
    if changed.pop("special", None) is None:
        _push_file("special", special)
    if changed.pop("config", None) is None:
        _push_file("config", config)
    for frequency in list(changed.keys()):
        _push_file(frequency, in_memory[frequency])


# here I ought to add the two EXIT functions.


def _add_to_special(task, collection):
    """Not meant for the end user. Adds a task (and the corresponding DLTL, maintaining order) to the collection."""
    if (freq := task["frequency"]) not in collection["frequencies"]:
        collection["frequencies"][freq] = dltl.DLTL()

        collection["ordering"].append(freq)
        i = 0
        while ordering_key[collection["ordering"][i]] < ordering_key[freq]:     # the search could be optimized, but the insert below negates any reason to
            i += 1
        collection["ordering"].insert(i, freq)
        collection["ordering"].pop()

    collection["frequencies"][freq].append_task(task)
    collection["glossary"][task["name"]] = task


def _remove_from_special(task, collection):     # This could cause a meltdown
    """Not meant for the end user. Removes a task (and the corresponding DLTL) from the collection."""
    collection["glossary"].pop(task["name"], None)
    freq = task["frequency"]
    temp = collection["frequencies"][freq]
    temp.detach_node_by_name(task["name"])
    if temp.size == 0:
        del collection["frequencies"][freq]
        collection["ordering"].remove(freq)


def _viability(frequency):
    """Not meant for the end user. Checks whether the task in question should be made due."""
    if frequency in ordinary:
        return True
    elif frequency in week:
        if frequency == now.strftime('%A'):
            return True
    elif frequency in dates:
        if frequency == today:
            return True
            # like many other things where I am working with "dates" but actually strings, this won't work properly
    return False


def _to_date(days):
    """Not meant for the end user. Converts the given number of days into a date in the future."""
    delta = timedelta(days)
    return today + delta


def create_task(name, frequency="once", task_description="", status="unfinished"):       # Maybe special treatment for "once" tasks?
    """Creates a task and automatically adds it to the correct list."""
    frequency = frequency.casefold()
    if status == "finished" and frequency == "once":
        print(f'Error: Cannot add a "once" task that is already finished. Task "{name}" was NOT created.')
        return
    temp = _pull_file(frequency)
    if name in temp.glossary:
        print(f'Error: Task with name {name} and frequency {frequency} already exists. Task was NOT created.')
        return
    new_task = {"name": name, "frequency": frequency, "description": task_description, "status": status}
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
    """Not meant for the end user. Helper function for finding a task in a nonDLTL collection."""
    i = 0
    while digit_input > (temp := last_displayed["frequencies"][last_displayed["ordering"][i]]).size:
        digit_input = digit_input - temp.size
        i += 1
    return temp.fetch_node_at_position(digit_input).task


def _target_task(user_input):       # Add properly: Block the user from doing shit with "(un)finished" selections (sorry, this is not allowed. View the main list)
    """Not meant for the end user. Retrieves a task based on the user typing its name or position in displayed list."""
    if user_input.isdigit():
        if last_displayed in special:
            return _target_task_in_special(user_input)
        else:
            return last_displayed.fetch_node_at_position(user_input).task
    else:
        return last_displayed["glossary"][user_input] if last_displayed in special else last_displayed.glossary[user_input]


def delete_task(task):
    """Deletes a task and removes it from all lists."""
    task = _target_task(task)
    frequency = task["frequency"]

    temp = _pull_file(frequency)
    temp.detach_node_by_name(task["name"])
    in_memory[frequency] = temp
    changed[frequency] = True

    for collection in special:
        if task["name"] in collection["glossary"]:
            _remove_from_special(task, collection)


def change_frequency(task, new_frequency):      # Add the case, where he changes it to once (and it's finished)
    """Changes the frequency (trigger condition) of the specified task."""
    task = _target_task(task)
    old_frequency = task["frequency"]
    task["frequency"] = new_frequency

    temp = _pull_file(old_frequency)
    temp.detach_node_by_name(task["name"])
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
    """Changes the description of the specified task."""
    task = _target_task(task)
    frequency = task["frequency"]

    temp = _pull_file(frequency)
    temp.fetch_task(task["name"])["description"] = new_description
    in_memory[frequency] = temp
    changed[frequency] = True

    for collection in special:
        if task["name"] in collection["glossary"]:
            collection["glossary"][task["name"]].task["description"] = new_description


def description(task):
    """Returns the description of the specified task, if it has one."""
    descript = _target_task(task)["description"]
    if descript == "":
        print("Requested task has no description.")
        return
    print(descript)


def set_asleep(task):
    """Sets the task to 'sleep' making become due on a specific day. Note: this makes it ignore its normal trigger condition."""
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


def renew(task):
    """Sets a task's status to 'due' and ads it to the agenda."""
    task = _target_task(task)
    frequency = task["frequency"]

    temp = _pull_file(frequency)
    task = temp.fetch_task(task["name"])
    task["status"] = "due"
    in_memory[frequency] = temp
    changed[frequency] = True

    for collection in special:
        if task["name"] in collection["glossary"]:
            _remove_from_special(task, collection)
    _add_to_special(task, due)


def finish(task):
    """Sets a task's status to 'finished', marking its completion and taking it off the agenda."""
    task = _target_task(task)
    frequency = task["frequency"]

    temp = _pull_file(frequency)
    task = temp.fetch_task(task["name"])
    task["status"] = "finished"
    in_memory[frequency] = temp
    changed[frequency] = True

    for collection in special:
        if task["name"] in collection["glossary"]:
            _remove_from_special(task, collection)
    _add_to_special(task, finished_today)


def mark_as_overdue(task):
    """Sets a task's status to 'overdue', marking its completion as high priority."""
    task = _target_task(task)
    frequency = task["frequency"]

    temp = _pull_file(frequency)
    task = temp.fetch_task(task["name"])
    task["status"] = "overdue"
    in_memory[frequency] = temp
    changed[frequency] = True

    for collection in special:
        if task["name"] in collection["glossary"]:
            _remove_from_special(task, collection)
    _add_to_special(task, overdue)


def change_name(task, new_name):
    """Changes the name of the specified task."""
    task = _target_task(task)
    frequency = task["frequency"]
    old_name = task["name"]

    temp = _pull_file(frequency)
    if new_name in temp.glossary:
        print(f'Error: Task with name {new_name} and frequency {frequency} already exists. Name change was aborted.')
        return -1
    node = temp.fetch_task(old_name)
    node.name = new_name
    node.task["name"] = new_name
    temp.glossary[new_name] = temp.glossary[old_name]
    del temp.glossary[old_name]
    in_memory[frequency] = temp
    changed[frequency] = True

    for collection in special:
        if old_name in collection["glossary"]:
            collection["glossary"][new_name] = collection["glossary"][old_name]
            del collection["glossary"][old_name]
            collection["glossary"][new_name].task["name"] = new_name
            collection["glossary"][new_name].name = new_name


def _display_special(collection, initial_index=1):
    """Not meant for the end user. Helper function for displaying all tasks in a nonDLTL collection."""
    if len(collection["ordering"]) == 0:
        raise ValueError("The list you have tried to display is empty!")             # Need to add proper handling of this!
    for frequency in collection["ordering"]:
        print(frequency)
        print()
        collection["frequencies"][frequency].display_tasks()
        initial_index += collection["frequencies"][frequency].size
    global last_displayed
    last_displayed = collection
    return initial_index


def _display_subspecial(collection, subspecial):
    """Not meant for the end user. Helper function for displaying all tasks from a DLTL saved in a nonDLTL collection"""
    if subspecial not in collection["frequencies"]:
        print("The list you have tried to display is empty!")
        return
    collection["frequencies"][subspecial].display_tasks()
    global last_displayed
    last_displayed = collection["frequencies"][subspecial]


def _display_finished(frequency, status):
    """Not meant for the end user. Helper function for displaying all 'finished' tasks from a DLTL."""
    temp = _pull_file(frequency)
    in_memory[frequency] = temp
    flag = temp.display_tasks_conditional(status)
    if flag == 1:   # No tasks were displayed, includes empty list case
        print("The list you have tried to display is empty!")
        return
    global last_displayed
    last_displayed = status


def display_tasks(category, status="all"):
    """Displays all the tasks of a given category and status. For valid parameters, see ___"""
    if category in special:
        _display_special(category)
    else:
        if status == "all":
            category.display_tasks()
            global last_displayed
            last_displayed = category
        elif status == "due":
            _display_subspecial(due, category)
        elif status == "overdue":
            _display_subspecial(overdue, category)
        elif status == "asleep":
            _display_subspecial(asleep, category)
        elif status == "finished_today":
            _display_subspecial(finished_today, category)
        elif status == "finished":
            _display_finished(category, "finished")
        elif status == "unfinished":
            _display_finished(category, "unfinished")


def to_do():
    """Displays all tasks on today's agenda."""

    i = 1
    first_failed = False
    try:
        i = _display_special(overdue)
    except ValueError:
        first_failed = True
    try:
        _display_special(due, i)
    except ValueError as e:
        if first_failed:
            print(f'Error: {e}')


def due():
    """Displays all due tasks except tasks that are overdue."""
    _display_special(due)


def overdue():
    """Displays all overdue tasks."""
    _display_special(overdue)


def asleep():
    """Displays all tasks which are asleep."""
    _display_special(asleep)


def finished_today():
    """Displays all tasks which were finished today."""
    _display_special(finished_today)


def display_all():
    """Displays all tasks currently logged by the program. Please note that this may be demanding on your device."""
    i = 1
    for frequency in ordinary:
        print(frequency)
        print()
        i = _pull_file(frequency).display_tasks(i)
    for frequency in week:
        print(frequency)
        print()
        i = _pull_file(frequency).display_tasks(i)
    for frequency in seasons:
        print(frequency)
        print()
        i = _pull_file(frequency).display_tasks(i)
    for frequency in counting:
        print(frequency)
        print()
        i = _pull_file(frequency).display_tasks(i)
    for frequency in dates:
        print(frequency)
        print()
        i = _pull_file(frequency).display_tasks(i)

    if i == 1:
        print("You have no tasks. Consider making some!")
    else:
        print()
        print("And that is all.")
