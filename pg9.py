import pickle
from os import path
from os import remove
from datetime import date, datetime, timedelta
import dltl

today = date.today()
now = datetime.now()
empty_list = dltl.DLTL()


def pickle_into_file(contents, file_name):
    with open(f'{file_name}.pkl', "wb") as f:
        pickle.dump(contents, f)


def unpickle_file(file_name):
    with open(f'{file_name}.pkl', "rb") as f:
        return pickle.load(f)


config = unpickle_file("config")
what_i_want_to_have_in_config = {"last_refresh": date(2024, 8, 20),
          "ordering_key": {"once": 1, "daily": 2}, "american dates": False}
# specific dates should go in the front I guess

due = unpickle_file("due")
overdue = unpickle_file("overdue")
finished_today = unpickle_file("finished_today")
asleep = unpickle_file("asleep")
groups = {"due": due, "overdue": overdue, "finished_today": finished_today}
statuses = {"due": due, "overdue": overdue, "asleep": asleep, "finished": finished_today}

ordinary = {"once", "daily", "weekly", "monthly", "seasonally", "yearly"}
week = {"monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"}
seasons = {"winter", "spring", "summer", "fall"}
counting = unpickle_file("counting")
dates = unpickle_file("dates")

in_memory = {}
changed = {}
last_displayed = None
ld_origin = None     # Stores what the source of the ld list was


def _pull_file(frequency):
    """Not meant for the end user. Pulls the desired file into memory (if it exists), or returns an empty DLTL."""
    if frequency in in_memory:
        temp = in_memory[frequency]
    else:
        if path.exists(f'{frequency}.pkl'):
            temp = unpickle_file(f'{frequency}.pkl')
        else:
            temp = dltl.DLTL()
        in_memory[frequency] = temp
    return temp


def _delete_file(frequency):
    """Not meant for the end user. Permanently deletes the specified file and all the tasks in it."""
    # Remove the file and prevent it from being constructed again
    if path.exists(f'{frequency}.pkl'):
        remove(f'{frequency}.pkl')
    changed.pop(frequency, None)

    # Remove all tasks of the given frequency from elsewhere
    for group in groups.values():
        group.delete_member(frequency)
    asleep.detach_all_frequency(frequency)


def _push_file(frequency, contents):  # might rewrite later to automatically take contents from in_memory,
    """Not meant for the end user. Pushes the current state of the given task list into the corresponding file."""
    if contents == empty_list:  # Protects from saving an empty task list
        _delete_file(frequency)
    else:
        pickle_into_file(contents, frequency)
    changed.pop(frequency, None)


def _update_dltl(target_name, contents):
    in_memory[target_name] = contents
    changed[target_name] = True


def _add_node_to_dltl(node, target_dltl):       # Might refactor to include more in the future, we'll see by the uses
    target_dltl.append_node(node)
    _update_dltl(node.frequency, target_dltl)


def _add_node_to_group(node, group_name):
    groups[group_name].append_node(node, config["ordering_key"])
    changed[group_name] = True


def _make_into_sleeper(node, until):
    """Ascribes the node an until (= wake-up date), then adds it to the 'asleep' DLTL."""
    node.until = until
    asleep.add_sleeper(node)
    changed["asleep"] = True


def _convert_to_date(days):
    """Not meant for the end user. Converts the given number of days into a date in the future. Only accepts
    positive integers, returns None otherwise (to be handled accordingly)."""
    if days.isdigit() and (days := int(days)) > 0:
        return today + timedelta(days)
    return None


def _set_until_date():
    """Not meant for the end user. Handles the user ascribing a wake-up date to an asleep task."""
    print("Putting task to sleep. Please input the date you would like the task to awaken on.")
    print("If you would like to give the number of days instead, type 'days'.")

    if (until := input(f'Type the date in the format YYYY-MM-DD')) == "days":
        if (until := _convert_to_date(input(f'Please type in the number of days, without spaces:'))) is None:
            print("Error: Did not receive a positive integer. Please try again from the beginning.")
            until = _set_until_date()

    else:
        try:
            until = date(int(until[0:4]), int(until[5:7]), int(until[8:10]))
        except:
            print("Error: Did not receive a date in the specified format. Please try again from the beginning.")
            until = _set_until_date()
    return until


def _viable_frequency(frequency):
    """Not meant for the end user. Checks whether the user typed in a valid frequency. If so,
    formats it to the programme's needs."""
    frequency = frequency.casefold()
    if frequency in ordinary or frequency in week or frequency in seasons:
        return frequency

    # It isn't in the above, so it would have to be a date. If it isn't, the following raises a ValueError.
    if len(frequency) != 5:
        raise ValueError("The frequency is too short/long.")
    if american_dates:
        frequency = date(2020, int(frequency[0:2]), int(frequency[3:5]))    # 2020 is a placeholder (leap year)
    else:
        frequency = date(2020, int(frequency[3:5]), int(frequency[0:2]))
    return frequency


def _viable_status(status):
    """Not meant for the end user. Checks whether the user typed in a valid status. If so,
        formats it to the programme's needs."""
    status = status.casefold()
    if status in statuses:
        return status
    return None


def save_changes():
    """Saves all changes and progress made to all tasks as well as programme configurations."""
    for name, status_list in statuses.values():
        if changed.pop(name, None) is not None:
            _push_file(name, status_list)
    if changed.pop("config", None) is not None:
        _push_file("config", config)

    for frequency in list(changed.keys()):      # The list is there since we are changed the dict while iterating
        _push_file(frequency, in_memory[frequency])

def exit_without_saving():
    """Properly exits the programme WITHOUT saving the changes made to the tasks and programme configurations."""


def exit_programme():
    """Properly saves all changes made and exits the programme."""
    save_changes()
    exit_without_saving()

def _catch_close_command():
    """Not meant for the end user. Catches the programme being closed in an improper way and automatically
    triggers proper close sequence."""

def _create_task_input_viability(frequency, status):

    # Checks the viability of the frequency
    try:
        frequency = _viable_frequency(frequency)
    except ValueError as ve:
        print(f'Error: The inputted frequency is invalid -- reason: {ve}. Task was NOT created.')
        return None, None

    # Checks the viability of the status
    status = _viable_status(status)
    if status is None:
        print("Error: The inputted status is invalid. Task was NOT created.")
        return None, None

    return frequency, status


def create_task(name, frequency="once", task_description="", status="due"):
    # Checks whether the user inputs are of the valid form
    frequency, status = _create_task_input_viability(frequency, status)
    if frequency is None:
        return None

    # Checks other validity concerns
    if frequency == "once" and status == "finished":
        print("Error: Cannot create a 'once' task that is already 'finished'. Task was NOT created.")
        return None
    temp = _pull_file(frequency)
    if name in temp.glossary:
        print(f'Error: Task with name {name} and frequency {frequency} already exists. Task was NOT created.')
        return None

    # Adds the task to the appropriate DLTLGroup
    until = None
    status_copy = dltl.TaskNode(name, frequency, task_description, status)
    if status == "asleep":
        until = _set_until_date()
        _make_into_sleeper(status_copy, until)
    else:
        _add_node_to_group(status_copy, status)

    # Adds the task to the frequency DLTL
    _add_node_to_dltl(dltl.TaskNode(name, frequency, task_description, status, until), temp)
    print(f'Task "{name}" was successfully created!')
    return True     # Just to signal successful completion

def _fetch_position_from_ld(position: int):
    """Not meant for the end user. Fetches a task node by its position in the last_displayed list."""
    if position < 1 or position > len(last_displayed):
        print("Error: Invalid position.")
        return None
    return last_displayed[position-1]

def _fetch_name_from_ld(name):
    """Not meant for the end user. Fetches a task node (that was in the last_displayed list) by its name."""

    # There are only 2 options
    if ld_origin in statuses:
        temp = statuses[ld_origin]
    else:
        temp = _pull_file(ld_origin)
    return temp.fetch_node(name)

def _fetch_from_ld(task):
    """Not meant for the end user. Fetches a task node that was in the last_displayed list."""
    if task.isdigit():
        return _fetch_position_from_ld(int(task))
    return _fetch_name_from_ld(task)


def _fetch_both_copies(task):
    task = _fetch_from_ld(task)
    if task is None:
        return None, None
    if ld_origin in statuses:
        status_copy = task
        frequency_copy = _pull_file(task.frequency).fetch_node(task.name)
    else:
        status_copy = statuses[task.status].glossary.get(task.name)  # Note that this could return None for "finished"
        frequency_copy = task
    return status_copy, frequency_copy


def delete_task(task):
    """Deletes a task and removes it from all lists."""
    status_copy, frequency_copy = _fetch_both_copies(task)
    if frequency_copy is None:      # The status copy may not exist if status == "finished"
        return None

    freq = _pull_file(frequency_copy.frequency)
    freq.detach_node(frequency_copy)
    _update_dltl(frequency_copy.frequency, freq)

    if status_copy is not None:
        temp = statuses[status_copy.status]
        temp.detach_node(status_copy)
        changed[status_copy.status] = True


def change_name(task, new_name):
    """Changes the name of the specified task."""
    status_copy, frequency_copy = _fetch_both_copies(task)
    if frequency_copy is None:  # The status copy may not exist if status == "finished"
        return False

    # First the frequency copy
    freq = _pull_file(frequency_copy.frequency)
    if new_name in freq.glossary:
        print(f'Error: Task with name {new_name} and frequency {frequency_copy.frequency} already exists. Name change was aborted.')
        return False
    freq.rename_node(frequency_copy, new_name)
    _update_dltl(frequency_copy.frequency, freq)

    # Then the status copy
    if status_copy is not None:
        temp = statuses[status_copy.status]
        temp.rename_node(status_copy, new_name)
        changed[status_copy.status] = True

def _change_freq_ask_user():
    if (response := input("Warning: Changing the frequency of a 'finished' task to 'once' will remove the task."
                          "Do you wish to proceed? (Y/N):")) == "Y":
        return True
    elif response == "N":
        return False
    else:
        print("Did not understand answer. Please try again.")
        return _change_freq_ask_user()


def change_frequency(task, new_frequency):
    """Changes the frequency (trigger condition) of the specified task."""
    if new_frequency == "once" and task.status == "finished":
        if _change_freq_ask_user():
            delete_task(task)
            return True
        else:
            return False

    status_copy, frequency_copy = _fetch_both_copies(task)
    if frequency_copy is None:  # The status copy may not exist if status == "finished"
        return False
    name, old_frequency = frequency_copy.name, frequency_copy.frequency

    # First the frequency copy
    freq2 = _pull_file(new_frequency)
    if name in freq2.glossary:
        print(
            f'Error: Task with name {name} and frequency {new_frequency} already exists.'
            f'Frequency change was aborted.')
        return False

    freq1 = _pull_file(old_frequency)
    freq1.detach_node(frequency_copy)
    frequency_copy.frequency = new_frequency
    freq2.append_node(frequency_copy)
    _update_dltl(old_frequency, freq1)
    _update_dltl(new_frequency, freq2)

    # Then the status copy
    if status_copy is not None:
        temp = statuses[status_copy.status]
        temp.change_frequency(status_copy, new_frequency, config["ordering_key"])
        changed[status_copy.status] = True


def change_description(task, new_description):
    """Changes the description of the specified task."""
    status_copy, frequency_copy = _fetch_both_copies(task)
    if frequency_copy is None:  # The status copy may not exist if status == "finished"
        return False

    # First the frequency copy
    freq = _pull_file(frequency_copy.frequency)
    freq.change_description(frequency_copy, new_description)
    _update_dltl(frequency_copy.frequency, freq)

    # Then the status copy
    if status_copy is not None:
        temp = statuses[status_copy.status]
        temp.change_description(status_copy, new_description)
        changed[status_copy.status] = True


def renew(task):
    """Sets a task's status to 'due' and ads it to the agenda."""
    status_copy, frequency_copy = _fetch_both_copies(task)
    if frequency_copy is None:  # The status copy may not exist if status == "finished"
        return False
    elif frequency_copy.status == "due":
        print("Error: The given task is already due. Aborting process.")
        return False

    # First the frequency copy
    freq = _pull_file(frequency_copy.frequency)
    freq.change_status(frequency_copy, "due")
    _update_dltl(frequency_copy.frequency, freq)

    # Then the status copy
    if status_copy is not None:
        temp = statuses[status_copy.status]
        temp.detach_node(status_copy)
        changed[status_copy.status] = True
    due.append_node(dltl.TaskNode(frequency_copy.name, frequency_copy.frequency,  frequency_copy.description,
                                  "due"), config["ordering_key"])
    changed["due"] = True


def mark_as_overdue(task):
    """Sets a task's status to 'overdue', marking its completion as high priority."""
    status_copy, frequency_copy = _fetch_both_copies(task)
    if frequency_copy is None:  # The status copy may not exist if status == "finished"
        return False
    elif frequency_copy.status == "overdue":
        print("Error: The given task is already overdue. Aborting process.")
        return False




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
---------------------------------



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
        raise ValueError("The list you have tried to display is empty!")  # Need to add proper handling of this!
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
    if flag == 1:  # No tasks were displayed, includes empty list case
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
