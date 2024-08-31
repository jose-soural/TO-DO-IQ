import pickle
import sys
from os import path, remove
from datetime import date, datetime, timedelta
from bisect import insort
import dltl     # Custom module
empty_dltl = dltl.DLTL()


def pickle_into_file(contents, file_name):
    with open(f'{file_name}.pkl', "wb") as f:
        pickle.dump(contents, f)


def unpickle_file(file_name, failsafe):
    if path.exists(f'{file_name}.pkl'):
        with open(f'{file_name}.pkl', "rb") as f:
            return pickle.load(f)
    return failsafe


config = unpickle_file("config", {"last_refresh": date(2024, 8, 20),
                                  "auto_refresh": False,
                                  "ordering_key": {"once": 1, "daily": 2}})
# specific dates should go in the front I guess

due = unpickle_file("due", dltl.DLTLGroup())
overdue = unpickle_file("overdue", dltl.DLTLGroup())
finished_today = unpickle_file("finished", dltl.DLTLGroup())
asleep = unpickle_file("asleep", dltl.SleeperDLTL())
groups = {"due": due, "overdue": overdue, "finished_today": finished_today}
statuses = {"due": due, "overdue": overdue, "asleep": asleep, "finished": finished_today}

ordinary = {"once", "daily", "weekly", "monthly", "seasonally", "yearly"}
week = {1: "monday", 2: "tuesday", 3: "wednesday", 4: "thursday", 5: "friday", 6: "saturday", 7: "sunday"}
months = {1: 'january', 2: 'february', 3: 'march', 4: 'april', 5: 'may', 6: 'june', 7: 'july', 8: 'august',
          9: 'september', 10: 'october', 11: 'november', 12: 'december'}
seasons = {1: "winter", 2:  "spring", 3: "summer", 4: "fall"}
# counting = unpickle_file("counting")
dates = unpickle_file("dates", {})      # An ordered list of dates we are using.

in_memory = {}
changed = {}
last_displayed = []
ld_origin = None     # Stores what the source of the ld list was


def _pull_file(frequency):
    """Not meant for the end user. Pulls the desired file into memory (if it exists), or returns an empty DLTL."""
    if frequency in in_memory:
        temp = in_memory[frequency]
    else:
        if path.exists(f'{frequency}.pkl'):
            temp = unpickle_file(f'{frequency}.pkl', None)
        else:
            temp = dltl.DLTL()
            # If we are creating a date entry, we have to add it to the list
            if isinstance(frequency, date):
                insort(dates, frequency)
                changed["dates"] = True

        in_memory[frequency] = temp
    return temp


def _delete_file(frequency):
    """Not meant for the end user. Permanently deletes the specified file and all the tasks in it."""
    # Remove the file and prevent it from being constructed again
    if path.exists(f'{frequency}.pkl'):
        remove(f'{frequency}.pkl')
    in_memory.pop(frequency, None)
    changed.pop(frequency, None)

    # If it was a date, remove it from the list of used dates
    if isinstance(frequency, date):
        dates.remove(frequency)
        changed["dates"] = True

    # Remove all tasks of the given frequency from elsewhere
    for group in groups.values():
        group.delete_member(frequency)
    asleep.detach_all_frequency(frequency)


def _push_file(frequency, contents):  # might rewrite later to automatically take contents from in_memory,
    """Not meant for the end user. Pushes the current state of the given task list into the corresponding file."""
    if contents == empty_dltl:  # Protects from saving an empty task list, but only for normal DLTLs
        _delete_file(frequency)
    else:
        pickle_into_file(contents, frequency)
    changed.pop(frequency, None)


def _update_dltl(target_name, contents):
    """Not meant for the end user. Updates the in memory copy of the DLTL and logs that it has been altered
    (= marks that it should be saved onto a file later)."""
    in_memory[target_name] = contents
    changed[target_name] = True


def _convert_to_date(days):
    """Not meant for the end user. Converts the given number of days into a date in the future. Only accepts
    positive integers, returns None otherwise (to be handled accordingly)."""
    if days.isdigit() and (days := int(days)) > 0:
        return date.today() + timedelta(days)
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
        except (ValueError, TypeError, IndexError):
            print("Error: Did not receive a date in the specified format. Please try again from the beginning.")
            until = _set_until_date()
    return until


def save_changes(namespace):        # The namespace is only to prevent "expected 0 arguments received 1 error"
    """Saves all changes and progress made to all tasks as well as programme configurations."""
    for name, status_list in statuses.items():
        if changed.pop(name, None) is not None:
            _push_file(name, status_list)
    if changed.pop("config", None) is not None:
        _push_file("config", config)
    if changed.pop("dates", None) is not None:
        _push_file("dates", dates)

    for frequency in list(changed.keys()):      # The list is there since we are changed the dict while iterating
        _push_file(frequency, in_memory[frequency])


def exit_without_saving(namespace):
    """Properly exits the programme WITHOUT saving the changes made to the tasks and programme configurations."""
    sys.exit(42)


def exit_programme(namespace):
    """Properly saves all changes made and exits the programme."""
    save_changes(namespace)
    exit_without_saving(namespace)


def catch_close_command():
    """Not meant for the end user. Catches the programme being closed in an improper way and prompts them, asking them
    to initiate proper exit procedure."""
    print("Caught attempt to exit application.")
    print("Warning: The used method is not the proper way to close TO-DO-IQ. Unsaved data WILL be lost."
          "Do you wish to save data before exiting? (Y/N)")
    while True:
        if (response := input().casefold()) == "y":
            save_changes("y")
            print("Data saved. Until next time!")
            sys.exit(0)
        elif response == "n":
            print("The changes from this session have been discarded. Until next time!")
            sys.exit(0)
        else:
            print("Did not understand answer. Please try again.")
            continue


def list_valid_frequencies(namespace):
    """Displays a list of all valid task frequencies (= trigger conditions)."""
    print("Any date in the format 'MM-DD' (M = month, D = day). -- The task will trigger once every year on that date.")
    print()
    print("We also support the following 'once every ____' frequencies:")
    for freq in seasons.values():
        print(f"'{freq}'", end=", ")
    for freq in months.values():
        print(f"'{freq}'", end=", ")
    for freq in week.values():
        print(f"'{freq}'", end=", ")
    print()
    print("Last but not least, the following are also supported:")
    for freq in ordinary:
        print(f"'{freq}'", end=", ")


def _validify_frequency(frequency):
    """Not meant for the end user. Checks whether the user input a frequency supported by the program. If so, formats
    it to the program's needs. More specific frequency restrictions are handled by the caller function itself."""
    frequency = frequency.casefold()
    if (frequency in ordinary or frequency in week.values() or frequency in months.values()
            or frequency in seasons.values() or frequency == "all"):
        return frequency

    # It isn't in the above, so it would have to be a date. If it isn't, then it's not valid
    if len(frequency) != 5:
        print("Error: The inputted frequency could not be matched to a frequency supported by the program, and was"
              "too long/short to be a date. Aborting process.")
        return None
    try:
        frequency = date(2020, int(frequency[0:2]), int(frequency[3:5]))    # 2020 is a placeholder (leap year)
    except (TypeError, ValueError) as e:
        print(f'Error: The inputted frequency could not be matched to a frequency supported by the program, and '
              f'could not be confirmed as a date -- reason: {e}. Aborting process.')
        return None
    return frequency


def create_task(name, frequency="once", task_description="", status="due"):
    """Creates a task with the given name, frequency (= trigger condition), description and status & adds it
    to appropriate lists."""
    # Checks whether the user inputted a valid frequency. The others were handled by argparse already
    frequency = _validify_frequency(frequency)
    if frequency is None:
        return None
    elif frequency == "all":
        print("Error: Cannot create a task with frequency 'all'.")
        return None

    # Checks other validity concerns
    if frequency == "once" and status == "finished":
        print("Error: Cannot create a 'once' task that is already 'finished'. Task was NOT created.")
        return None
    temp = _pull_file(frequency)
    if name in temp.glossary:
        print(f'Error: Task with name {name} and frequency {frequency} already exists. Task was NOT created.')
        return None
    if name in statuses[status].glossary:
        print(f'Error: Task with name {name} and status {status} already exists. Task was NOT created.')
        return None

    # Adds the task to the appropriate DLTLGroup
    until = None
    status_copy = dltl.TaskNode(name, frequency, task_description, status)
    if status == "asleep":
        # Ascribes the node an until (= wake-up date), then adds it to the 'asleep' DLTL
        until = status_copy.until = _set_until_date()
        asleep.add_sleeper(status_copy)
        changed["asleep"] = True
    else:
        statuses[status].append_node(status_copy, config["ordering_key"])
        changed[status] = True

    # Adds the task to the frequency DLTL
    temp.append_node(dltl.TaskNode(name, frequency, task_description, status, until))
    _update_dltl(frequency, temp)

    print(f'Task "{name}" was successfully created!')
    return True     # Just to signal successful completion


def create_task_argparse(namespace):
    """Not meant for the end user. Handles the passing of the arguments received from the user by argparse onto
    the create_task() function. Purely for refactoring purposes"""
    if create_task(namespace.task_name, namespace.frequency, namespace.DESCRIPTION, namespace.status) is None:
        return None


def _fetch_position_from_ld(position: int):
    """Not meant for the end user. Fetches a task node by its position in the last_displayed list."""
    if position < 1 or position > len(last_displayed):
        print("Error: Invalid position.")
        return None
    return last_displayed[position-1]


def _fetch_name_from_ld(name):
    """Not meant for the end user. Fetches a task node (that was in the last_displayed list) by its name."""

    # There are only 3 options
    if ld_origin == "to_do":
        if name in due.glossary:
            temp = due
        else:
            temp = overdue
    elif ld_origin in statuses:
        temp = statuses[ld_origin]
    else:
        temp = _pull_file(ld_origin)
    return temp.fetch_node(name)


def _fetch_from_ld(task):
    """Not meant for the end user. Fetches a task node that was in the last_displayed list, after checking that it's
    possible."""
    if ld_origin == "unsupported":
        print("Error: The last displayed list is too broad and as such does not allow interaction with tasks. Please"
              "display a more specialized list to access specific tasks.")
        return None
    if task.isdigit():
        return _fetch_position_from_ld(int(task))
    return _fetch_name_from_ld(task)


def _fetch_both_copies(task):
    task = _fetch_from_ld(task)
    if task is None:
        return None, None
    if ld_origin == "to_do" or ld_origin in statuses:
        status_copy = task
        frequency_copy = _pull_file(task.frequency).fetch_node(task.name)
    else:
        status_copy = statuses[task.status].glossary.get(task.name)  # Note that this could return None for "finished"
        frequency_copy = task
    return status_copy, frequency_copy


def delete_task(namespace):
    """Deletes a task and removes it from all lists."""
    status_copy, frequency_copy = _fetch_both_copies(namespace.target_task)
    if frequency_copy is None:      # The status copy may not exist if status == "finished"
        return None

    freq = _pull_file(frequency_copy.frequency)
    freq.detach_node(frequency_copy)
    _update_dltl(frequency_copy.frequency, freq)

    if status_copy is not None:
        temp = statuses[status_copy.status]
        temp.detach_node(status_copy)
        changed[status_copy.status] = True


def change_name(namespace):
    """Changes the name of the specified task."""
    status_copy, frequency_copy = _fetch_both_copies(namespace.target_task)
    new_name = namespace.NEW
    if frequency_copy is None:  # The status copy may not exist if status == "finished"
        return False

    # First the frequency copy
    freq = _pull_file(frequency_copy.frequency)
    if new_name in freq.glossary:
        print(f'Error: Task with name {new_name} and frequency {frequency_copy.frequency}'
              f'already exists. Name change was aborted.')
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
                          "Do you wish to proceed? (Y/N):").casefold()) == "y":
        return True
    elif response == "n":
        return False
    else:
        print("Did not understand answer. Please try again.")
        return _change_freq_ask_user()


def change_frequency(namespace):
    """Changes the frequency (trigger condition) of the specified task."""

    # Checks whether the user inputted a valid frequency
    new_frequency = _validify_frequency(namespace.NEW)
    if new_frequency is None:
        return None
    elif new_frequency == "all":
        print("Error: Cannot create a task with frequency 'all'.")
        return None

    status_copy, frequency_copy = _fetch_both_copies(namespace.target_task)
    if frequency_copy is None:  # The status copy may not exist if status == "finished"
        return False
    name, old_frequency = frequency_copy.name, frequency_copy.frequency

    if new_frequency == old_frequency:
        print("Error: The given task already has said frequency. Process aborted.")
        return None

    if new_frequency == "once" and frequency_copy.status == "finished":
        if _change_freq_ask_user():
            delete_task(namespace.target_task)
            return True
        else:
            return False

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


def change_description(namespace):
    """Changes the description of the specified task."""
    status_copy, frequency_copy = _fetch_both_copies(namespace.target_task)
    new_description = namespace.NEW
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


def _change_status(task, new_status):
    """not for user -- umbrella function -- but not for asleep"""
    status_copy, frequency_copy = _fetch_both_copies(task)
    if frequency_copy is None:  # The status copy may not exist if status == "finished"
        return False

    name, old_status = frequency_copy.name, frequency_copy.status
    if old_status == new_status:
        print(f'Error: The given task is already {new_status}. Aborting process.')
        return False
    if name in statuses[new_status].glossary:
        print(
            f'Error: Task with name {name} and status {new_status} already exists.'
            f'Aborting process.')
        return False

    # First the frequency copy
    freq = _pull_file(frequency_copy.frequency)
    freq.change_status(frequency_copy, new_status)
    frequency_copy.until = None     # It cannot change into a sleeper, so in case it is changing from being one
    _update_dltl(frequency_copy.frequency, freq)

    # Then the status copy
    if status_copy is not None:
        temp = statuses[old_status]
        temp.detach_node(status_copy)
        changed[old_status] = True
    status_copy.until = None
    statuses[new_status].append_node(status_copy, config["ordering_key"])
    changed[new_status] = True


def set_asleep(namespace):
    """Sets the task to 'sleep' making become due on a specific day.
    Note: this makes it ignore its normal trigger condition."""
    status_copy, frequency_copy = _fetch_both_copies(namespace.target_task)
    if frequency_copy is None:  # The status copy may not exist if status == "finished"
        return False

    if frequency_copy.name in asleep.glossary:
        print(
            f'Error: Task with name {frequency_copy.name} and status "asleep" already exists.'
            f'Aborting process.')
        return False

    status_copy.until = frequency_copy.until = _set_until_date()

    # First the frequency copy
    freq = _pull_file(frequency_copy.frequency)
    freq.change_status(frequency_copy, "asleep")
    _update_dltl(frequency_copy.frequency, freq)

    # Then the status copy
    if status_copy is not None:
        temp = statuses[status_copy.status]
        temp.detach_node(status_copy)
        changed[status_copy.status] = True
    asleep.add_sleeper(status_copy)
    changed["asleep"] = True


def renew(namespace):
    """Sets a task's status to 'due' and ads it to the agenda."""
    _change_status(namespace.target_task, "due")


def mark_as_overdue(namespace):
    """Sets a task's status to 'overdue', marking its completion as high priority."""
    _change_status(namespace.target_task, "overdue")


def finish(namespace):
    """Sets a task's status to 'finished', marking its completion and taking it off the agenda. NOTE: finishing
    a 'once' task will automatically remove it."""
    node = _fetch_from_ld(namespace.target_task)
    if node is None:
        return None
    if node.frequency == "once":
        delete_task(namespace.target_task)
    else:
        _change_status(namespace.target_task, "finished")


def _prepare_description(task_description):
    if task_description == "":
        return "None"
    return task_description


def description(namespace):
    """Displays the description of the task."""
    task = _fetch_from_ld(namespace.target_task)
    if task is None:
        return None

    print(f'Task {task.name} description:')
    print()
    print(_prepare_description(task.description))


def detail(namespace):
    """Displays all information about the task."""
    task = _fetch_from_ld(namespace.target_task)
    if task is None:
        return None

    print("Task name:", task.name, "", "Task frequency:", task.frequency, "",
          "Task description:", _prepare_description(task.description), "", "Task status:", task.status, "",
          "Task wake-up date:", task.until, sep="\n")


def _display_all_warning():
    print("You are about to tasks from all lists currently logged by the program."
          "Please note that this may be demanding on your device AND that this display is view only, meaning"
          "you will NOT be able to access or edit task details.")
    if (response := input("Do you wish to proceed? (Y/N)").casefold()) == "y":
        return True
    elif response == "n":
        return False
    else:
        print("Did not understand response. Please try again.")
        return _display_all_warning()


def display_all(namespace):
    """Displays all (optionally only finished) tasks currently logged by the programme.
    Please note that this may be demanding on your device."""
    if _display_all_warning() is False:
        return False

    # Sorting out argparse or internal caller
    if namespace is True or namespace is False:
        finished = namespace
    else:
        finished = namespace.FINISHED

    global last_displayed, ld_origin
    last_displayed, ld_origin = None, "unsupported"

    i = 1
    for frequency in ordinary:
        print(frequency)
        print()
        i = _pull_file(frequency).display_alongside_others(finished, i)
    for frequency in week.values():
        print(frequency)
        print()
        i = _pull_file(frequency).display_alongside_others(finished, i)
    for frequency in months.values():
        print(frequency)
        print()
        i = _pull_file(frequency).display_alongside_others(finished, i)
    for frequency in seasons.values():
        print(frequency)
        print()
        i = _pull_file(frequency).display_alongside_others(finished, i)
    # for frequency in counting:
    #    print(frequency)
    #   print()
    #  i = _pull_file(frequency).display_alongside_others(finished, i)
    for frequency in dates:
        print(f'{frequency.month}-{frequency.day}')
        print()
        i = _pull_file(frequency).display_alongside_others(finished, i)

        if i == 1:
            if finished:
                print("You have no finished tasks.")
            else:
                print("You have no tasks. Consider making some!")
        else:
            print()
            print("And that is all.")


def display_list(frequency, status):
    """Displays all tasks (their names) of the specified frequency and status."""
    frequency = _validify_frequency(frequency)
    if frequency is None:
        return None

    global last_displayed, ld_origin

    if frequency == "all":
        # Asleep is a special case
        if status == "asleep":
            last_displayed = asleep.display_task_names()
            ld_origin = "asleep"

        # All and finished are the other special case
        elif status == "all":
            display_all(False)
        elif status == "finished":
            display_all(True)

        # All tasks from a DLTL group
        else:
            if status == "finished_today":
                status = "finished"
            last_displayed = statuses[status].display_task_names()
            ld_origin = status

    elif status == "all":
        last_displayed = _pull_file(frequency).display_task_names()
        ld_origin = frequency
    elif status == "asleep":
        last_displayed = _pull_file(frequency).display_task_names_conditional("asleep")
        ld_origin = frequency
    elif status == "finished":
        last_displayed = _pull_file(frequency).display_task_names_conditional("finished")
        ld_origin = frequency
    else:
        if status == "finished_today":
            status = "finished"
        target = statuses[status].members[frequency]
        last_displayed = target.display_task_names([None] * target.size)
        ld_origin = status


def to_do(namespace):
    """Displays all tasks on today's agenda."""
    if (size := (overdue.size + due.size)) == 0:
        print("You have finished all your tasks. Congratulations!")
        return
    global last_displayed, ld_origin
    last_displayed = [None] * size
    ld_origin = "to_do"

    initial_index = 1
    print("---- overdue ----")
    print("")
    for frequency in overdue.ordering:
        print(frequency, ":", sep="")
        last_displayed, initial_index = overdue.members[frequency].display_task_names(last_displayed, initial_index)
        print()
    print("")
    print("---- due ----")
    print("")
    for frequency in due.ordering:
        print(frequency, ":", sep="")
        last_displayed, initial_index = overdue.members[frequency].display_task_names(last_displayed, initial_index)
        print()
    print("And that is all.")


def display_list_argparse(namespace):
    """Not meant for the end user. Receives a command from argparse and converts it into the appropriate call
    to the display_list() function."""
    if namespace.command == "due":
        display_list("all", "due")
    elif namespace.command == "overdue":
        display_list("all", "overdue")
    elif namespace.command == "asleep":
        display_list("all", "asleep")
    else:
        display_list("all", "finished_today")


def due(namespace):
    """Displays all due tasks except tasks that are overdue."""
    display_list("all", "due")


def overdue(namespace):
    """Displays all overdue tasks."""
    display_list("all", "overdue")


def asleep(namespace):
    """Displays all tasks which are asleep."""
    display_list("all", "asleep")


def finished_today(namespace):
    """Displays all tasks which were finished today."""
    display_list("all", "finished_today")


def _refresh_frequency(frequency):
    temp = _pull_file(frequency)
    current = temp.head
    while current is not None:
        if current.status == "due":
            node = due.detach_node_by_name(current.name)
            node.status = current.status = "overdue"
            if current.name in overdue.glossary:
                node.name = current.name = f'{current.name} -- name collision prevention triggered {datetime.now()}'
            overdue.append_node(node, config["ordering_key"])
        elif current.status == "finished":
            if current.name in due.glossary:
                current.name = f'{current.name} -- name collision prevention triggered {datetime.now()}'
            due.append_node(dltl.TaskNode(current.name, current.frequency, current.description, "due"),
                            config["ordering_key"])
            current.status = "due"
        current = current.next
    _update_dltl(frequency, temp)
    # changed["due"] = changed["overdue"] = True -- We do this at the refresh to_do level, otherwise we would do it here


def _get_season(date_object):
    """Returns the season of the given date."""

    month, day = date_object.month, date_object.day

    # Determine the season based on month and day
    if month in {1, 2}:
        return 1        # For reasons down the line, we will differentiate between first and second winter
    if month in {3, 4, 5}:
        return 2        # Spring
    elif month in {6, 7, 8}:
        return 3
    elif month in {9, 10, 11}:
        return 4
    else:
        return 5


def refresh_to_do(namespace):
    """Updates the to-do list. Based on the system date, it wakes up sleepers, adds due tasks and potentially
    marks tasks that are overdue."""

    # Check if there is a need to refresh
    today = date.today()
    if config["last_refresh"] == today:
        print("Tasks were already refreshed today.")
        return

    global finished_today
    refresh_year, refresh_week, refresh_weekday = config["last_refresh"].isocalendar()
    refresh_month, refresh_season = config["last_refresh"].month, _get_season(config["last_refresh"])
    today_year, today_week, today_weekday = today.isocalendar()
    today_month, today_season = today.month, _get_season(today)

    if today_year != refresh_year:
        _refresh_frequency("yearly")
        for i in range(refresh_season + 1, 6):
            _refresh_frequency(seasons[i // 4])     # Refresh all season up to that year's second winter included
        for i in range(1, min(today_season, refresh_season) + 1):
            _refresh_frequency(seasons[i])

        if not (refresh_season == 5 and today_season == 1):
            _refresh_frequency("seasonally")

        _refresh_frequency("monthly")
        for i in range(refresh_month + 1, 13):
            _refresh_frequency(months[i])
        for i in range(1, min(today_month, refresh_month) + 1):
            _refresh_frequency(months[i])

        _refresh_frequency("weekly")
        for i in range(refresh_weekday + 1, 8):
            _refresh_frequency(week[i])
        for i in range(1, min(today_weekday, refresh_weekday) + 1):
            _refresh_frequency(week[i])

        # And lastly the applicable dates
        check1 = date(2020, today_month, today.day)
        check2 = date(2020, refresh_month, config["last_refresh"].day)
        for i in range(len(dates)):
            date_ = dates[i]
            if date_ <= check1 or date_ > check2:
                _refresh_frequency(date_)
            i += 1

    # The year is the same
    else:
        if refresh_season != today_season:
            _refresh_frequency("seasonally")
            for i in range(refresh_season + 1, today_season + 1):
                _refresh_frequency(seasons[i // 4])       # A trick using the differentiation of first and second winter

        if refresh_month != today_month:
            _refresh_frequency("monthly")
            for i in range(refresh_month + 1, today_month + 1):
                _refresh_frequency(months[i])

        if refresh_week != today_week:
            _refresh_frequency("weekly")
            for i in range(refresh_weekday + 1, 8):
                _refresh_frequency(week[i])
            for i in range(1, min(today_weekday, refresh_weekday) + 1):
                _refresh_frequency(week[i])

        else:
            for i in range(refresh_weekday + 1, today_weekday + 1):
                _refresh_frequency(week[i])

        # And lastly the applicable dates
        start = date(2020, refresh_month, config["last_refresh"].day)
        end = date(2020, today_month, today.day)
        for i in range(len(dates)):
            date_ = dates[i]
            if date_ > start:
                if date_ > end:
                    break
                _refresh_frequency(date_)
            i += 1

    # The following always triggers
    finished_today = dltl.DLTLGroup()       # Empties it
    _refresh_frequency("daily")
    asleep.wake_up_sleepers(today, due)
    config["last_refresh"] = today
    changed["due"] = changed["overdue"] = changed["asleep"] = changed["finished"] = changed["config"] = True
    # That might not be the case for all, but it doesn't matter, and it is neater this way

    print("Tasks successfully refreshed.")


def change_config(namespace):
    if namespace.AUTO_REFRESH == "true":
        config["auto_refresh"] = True
    else:
        config["auto_refresh"] = False
    changed["config"] = True


def _start_anew():
    """Not meant for the end user. Resets all settings and wipes TO-DO-IQ list clean, then closes the program."""
    for file_name in ordinary:
        if path.exists(f'{file_name}.pkl'):
            remove(f'{file_name}.pkl')
    for file_name in week.values():
        if path.exists(f'{file_name}.pkl'):
            remove(f'{file_name}.pkl')
    for file_name in months.values():
        if path.exists(f'{file_name}.pkl'):
            remove(f'{file_name}.pkl')
    for file_name in seasons.values():
        if path.exists(f'{file_name}.pkl'):
            remove(f'{file_name}.pkl')
    for file_name in dates:
        if path.exists(f'{file_name}.pkl'):
            remove(f'{file_name}.pkl')
    for file_name in statuses:
        if path.exists(f'{file_name}.pkl'):
            remove(f'{file_name}.pkl')
    if path.exists('dates.pkl'):
        remove('dates.pkl')
    if path.exists('config.pkl'):
        remove('config.pkl')
    exit_without_saving("yay")
