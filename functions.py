import pickle
import sys
from os import path, remove
from datetime import date, datetime, timedelta
from bisect import insort
import dltl     # Custom module


def pickle_into_file(contents, file_name):
    with open(f'{file_name}.pkl', "wb") as f:
        pickle.dump(contents, f)


def unpickle_file(file_name, failsafe):
    if path.exists(f'{file_name}.pkl'):
        with open(f'{file_name}.pkl', "rb") as f:
            return pickle.load(f)
    return failsafe


#   Change last_refresh default later
config = unpickle_file("config", {"last_refresh": date(2023, 1, 1),
                                  "auto_refresh": False,
                                  "ordering_key": {date(2020, 1, 1): -366, date(2020, 1, 2): -365, date(2020, 1, 3): -364, date(2020, 1, 4): -363, date(2020, 1, 5): -362, date(2020, 1, 6): -361, date(2020, 1, 7): -360, date(2020, 1, 8): -359, date(2020, 1, 9): -358, date(2020, 1, 10): -357, date(2020, 1, 11): -356, date(2020, 1, 12): -355, date(2020, 1, 13): -354, date(2020, 1, 14): -353, date(2020, 1, 15): -352, date(2020, 1, 16): -351, date(2020, 1, 17): -350, date(2020, 1, 18): -349, date(2020, 1, 19): -348, date(2020, 1, 20): -347, date(2020, 1, 21): -346, date(2020, 1, 22): -345, date(2020, 1, 23): -344, date(2020, 1, 24): -343, date(2020, 1, 25): -342, date(2020, 1, 26): -341, date(2020, 1, 27): -340, date(2020, 1, 28): -339, date(2020, 1, 29): -338, date(2020, 1, 30): -337, date(2020, 1, 31): -336, date(2020, 2, 1): -335, date(2020, 2, 2): -334, date(2020, 2, 3): -333, date(2020, 2, 4): -332, date(2020, 2, 5): -331, date(2020, 2, 6): -330, date(2020, 2, 7): -329, date(2020, 2, 8): -328, date(2020, 2, 9): -327, date(2020, 2, 10): -326, date(2020, 2, 11): -325, date(2020, 2, 12): -324, date(2020, 2, 13): -323, date(2020, 2, 14): -322, date(2020, 2, 15): -321, date(2020, 2, 16): -320, date(2020, 2, 17): -319, date(2020, 2, 18): -318, date(2020, 2, 19): -317, date(2020, 2, 20): -316, date(2020, 2, 21): -315, date(2020, 2, 22): -314, date(2020, 2, 23): -313, date(2020, 2, 24): -312, date(2020, 2, 25): -311, date(2020, 2, 26): -310, date(2020, 2, 27): -309, date(2020, 2, 28): -308, date(2020, 2, 29): -307, date(2020, 3, 1): -306, date(2020, 3, 2): -305, date(2020, 3, 3): -304, date(2020, 3, 4): -303, date(2020, 3, 5): -302, date(2020, 3, 6): -301, date(2020, 3, 7): -300, date(2020, 3, 8): -299, date(2020, 3, 9): -298, date(2020, 3, 10): -297, date(2020, 3, 11): -296, date(2020, 3, 12): -295, date(2020, 3, 13): -294, date(2020, 3, 14): -293, date(2020, 3, 15): -292, date(2020, 3, 16): -291, date(2020, 3, 17): -290, date(2020, 3, 18): -289, date(2020, 3, 19): -288, date(2020, 3, 20): -287, date(2020, 3, 21): -286, date(2020, 3, 22): -285, date(2020, 3, 23): -284, date(2020, 3, 24): -283, date(2020, 3, 25): -282, date(2020, 3, 26): -281, date(2020, 3, 27): -280, date(2020, 3, 28): -279, date(2020, 3, 29): -278, date(2020, 3, 30): -277, date(2020, 3, 31): -276, date(2020, 4, 1): -275, date(2020, 4, 2): -274, date(2020, 4, 3): -273, date(2020, 4, 4): -272, date(2020, 4, 5): -271, date(2020, 4, 6): -270, date(2020, 4, 7): -269, date(2020, 4, 8): -268, date(2020, 4, 9): -267, date(2020, 4, 10): -266, date(2020, 4, 11): -265, date(2020, 4, 12): -264, date(2020, 4, 13): -263, date(2020, 4, 14): -262, date(2020, 4, 15): -261, date(2020, 4, 16): -260, date(2020, 4, 17): -259, date(2020, 4, 18): -258, date(2020, 4, 19): -257, date(2020, 4, 20): -256, date(2020, 4, 21): -255, date(2020, 4, 22): -254, date(2020, 4, 23): -253, date(2020, 4, 24): -252, date(2020, 4, 25): -251, date(2020, 4, 26): -250, date(2020, 4, 27): -249, date(2020, 4, 28): -248, date(2020, 4, 29): -247, date(2020, 4, 30): -246, date(2020, 5, 1): -245, date(2020, 5, 2): -244, date(2020, 5, 3): -243, date(2020, 5, 4): -242, date(2020, 5, 5): -241, date(2020, 5, 6): -240, date(2020, 5, 7): -239, date(2020, 5, 8): -238, date(2020, 5, 9): -237, date(2020, 5, 10): -236, date(2020, 5, 11): -235, date(2020, 5, 12): -234, date(2020, 5, 13): -233, date(2020, 5, 14): -232, date(2020, 5, 15): -231, date(2020, 5, 16): -230, date(2020, 5, 17): -229, date(2020, 5, 18): -228, date(2020, 5, 19): -227, date(2020, 5, 20): -226, date(2020, 5, 21): -225, date(2020, 5, 22): -224, date(2020, 5, 23): -223, date(2020, 5, 24): -222, date(2020, 5, 25): -221, date(2020, 5, 26): -220, date(2020, 5, 27): -219, date(2020, 5, 28): -218, date(2020, 5, 29): -217, date(2020, 5, 30): -216, date(2020, 5, 31): -215, date(2020, 6, 1): -214, date(2020, 6, 2): -213, date(2020, 6, 3): -212, date(2020, 6, 4): -211, date(2020, 6, 5): -210, date(2020, 6, 6): -209, date(2020, 6, 7): -208, date(2020, 6, 8): -207, date(2020, 6, 9): -206, date(2020, 6, 10): -205, date(2020, 6, 11): -204, date(2020, 6, 12): -203, date(2020, 6, 13): -202, date(2020, 6, 14): -201, date(2020, 6, 15): -200, date(2020, 6, 16): -199, date(2020, 6, 17): -198, date(2020, 6, 18): -197, date(2020, 6, 19): -196, date(2020, 6, 20): -195, date(2020, 6, 21): -194, date(2020, 6, 22): -193, date(2020, 6, 23): -192, date(2020, 6, 24): -191, date(2020, 6, 25): -190, date(2020, 6, 26): -189, date(2020, 6, 27): -188, date(2020, 6, 28): -187, date(2020, 6, 29): -186, date(2020, 6, 30): -185, date(2020, 7, 1): -184, date(2020, 7, 2): -183, date(2020, 7, 3): -182, date(2020, 7, 4): -181, date(2020, 7, 5): -180, date(2020, 7, 6): -179, date(2020, 7, 7): -178, date(2020, 7, 8): -177, date(2020, 7, 9): -176, date(2020, 7, 10): -175, date(2020, 7, 11): -174, date(2020, 7, 12): -173, date(2020, 7, 13): -172, date(2020, 7, 14): -171, date(2020, 7, 15): -170, date(2020, 7, 16): -169, date(2020, 7, 17): -168, date(2020, 7, 18): -167, date(2020, 7, 19): -166, date(2020, 7, 20): -165, date(2020, 7, 21): -164, date(2020, 7, 22): -163, date(2020, 7, 23): -162, date(2020, 7, 24): -161, date(2020, 7, 25): -160, date(2020, 7, 26): -159, date(2020, 7, 27): -158, date(2020, 7, 28): -157, date(2020, 7, 29): -156, date(2020, 7, 30): -155, date(2020, 7, 31): -154, date(2020, 8, 1): -153, date(2020, 8, 2): -152, date(2020, 8, 3): -151, date(2020, 8, 4): -150, date(2020, 8, 5): -149, date(2020, 8, 6): -148, date(2020, 8, 7): -147, date(2020, 8, 8): -146, date(2020, 8, 9): -145, date(2020, 8, 10): -144, date(2020, 8, 11): -143, date(2020, 8, 12): -142, date(2020, 8, 13): -141, date(2020, 8, 14): -140, date(2020, 8, 15): -139, date(2020, 8, 16): -138, date(2020, 8, 17): -137, date(2020, 8, 18): -136, date(2020, 8, 19): -135, date(2020, 8, 20): -134, date(2020, 8, 21): -133, date(2020, 8, 22): -132, date(2020, 8, 23): -131, date(2020, 8, 24): -130, date(2020, 8, 25): -129, date(2020, 8, 26): -128, date(2020, 8, 27): -127, date(2020, 8, 28): -126, date(2020, 8, 29): -125, date(2020, 8, 30): -124, date(2020, 8, 31): -123, date(2020, 9, 1): -122, date(2020, 9, 2): -121, date(2020, 9, 3): -120, date(2020, 9, 4): -119, date(2020, 9, 5): -118, date(2020, 9, 6): -117, date(2020, 9, 7): -116, date(2020, 9, 8): -115, date(2020, 9, 9): -114, date(2020, 9, 10): -113, date(2020, 9, 11): -112, date(2020, 9, 12): -111, date(2020, 9, 13): -110, date(2020, 9, 14): -109, date(2020, 9, 15): -108, date(2020, 9, 16): -107, date(2020, 9, 17): -106, date(2020, 9, 18): -105, date(2020, 9, 19): -104, date(2020, 9, 20): -103, date(2020, 9, 21): -102, date(2020, 9, 22): -101, date(2020, 9, 23): -100, date(2020, 9, 24): -99, date(2020, 9, 25): -98, date(2020, 9, 26): -97, date(2020, 9, 27): -96, date(2020, 9, 28): -95, date(2020, 9, 29): -94, date(2020, 9, 30): -93, date(2020, 10, 1): -92, date(2020, 10, 2): -91, date(2020, 10, 3): -90, date(2020, 10, 4): -89, date(2020, 10, 5): -88, date(2020, 10, 6): -87, date(2020, 10, 7): -86, date(2020, 10, 8): -85, date(2020, 10, 9): -84, date(2020, 10, 10): -83, date(2020, 10, 11): -82, date(2020, 10, 12): -81, date(2020, 10, 13): -80, date(2020, 10, 14): -79, date(2020, 10, 15): -78, date(2020, 10, 16): -77, date(2020, 10, 17): -76, date(2020, 10, 18): -75, date(2020, 10, 19): -74, date(2020, 10, 20): -73, date(2020, 10, 21): -72, date(2020, 10, 22): -71, date(2020, 10, 23): -70, date(2020, 10, 24): -69, date(2020, 10, 25): -68, date(2020, 10, 26): -67, date(2020, 10, 27): -66, date(2020, 10, 28): -65, date(2020, 10, 29): -64, date(2020, 10, 30): -63, date(2020, 10, 31): -62, date(2020, 11, 1): -61, date(2020, 11, 2): -60, date(2020, 11, 3): -59, date(2020, 11, 4): -58, date(2020, 11, 5): -57, date(2020, 11, 6): -56, date(2020, 11, 7): -55, date(2020, 11, 8): -54, date(2020, 11, 9): -53, date(2020, 11, 10): -52, date(2020, 11, 11): -51, date(2020, 11, 12): -50, date(2020, 11, 13): -49, date(2020, 11, 14): -48, date(2020, 11, 15): -47, date(2020, 11, 16): -46, date(2020, 11, 17): -45, date(2020, 11, 18): -44, date(2020, 11, 19): -43, date(2020, 11, 20): -42, date(2020, 11, 21): -41, date(2020, 11, 22): -40, date(2020, 11, 23): -39, date(2020, 11, 24): -38, date(2020, 11, 25): -37, date(2020, 11, 26): -36, date(2020, 11, 27): -35, date(2020, 11, 28): -34, date(2020, 11, 29): -33, date(2020, 11, 30): -32, date(2020, 12, 1): -31, date(2020, 12, 2): -30, date(2020, 12, 3): -29, date(2020, 12, 4): -28, date(2020, 12, 5): -27, date(2020, 12, 6): -26, date(2020, 12, 7): -25, date(2020, 12, 8): -24, date(2020, 12, 9): -23, date(2020, 12, 10): -22, date(2020, 12, 11): -21, date(2020, 12, 12): -20, date(2020, 12, 13): -19, date(2020, 12, 14): -18, date(2020, 12, 15): -17, date(2020, 12, 16): -16, date(2020, 12, 17): -15, date(2020, 12, 18): -14, date(2020, 12, 19): -13, date(2020, 12, 20): -12, date(2020, 12, 21): -11, date(2020, 12, 22): -10, date(2020, 12, 23): -9, date(2020, 12, 24): -8, date(2020, 12, 25): -7, date(2020, 12, 26): -6, date(2020, 12, 27): -5, date(2020, 12, 28): -4, date(2020, 12, 29): -3, date(2020, 12, 30): -2, date(2020, 12, 31): -1, 'once': 1, 'daily': 2, 'weekly': 3, 'monthly': 4, 'seasonally': 5, 'yearly': 6, 'monday': 7, 'tuesday': 8, 'wednesday': 9, 'thursday': 10, 'friday': 11, 'saturday': 12, 'sunday': 13, 'january': 14, 'february': 15, 'march': 16, 'april': 17, 'may': 18, 'june': 19, 'july': 20, 'august': 21, 'september': 22, 'october': 23, 'november': 24, 'december': 25, 'winter': 26, 'spring': 27, 'summer': 28, 'fall': 29}
                                  })
# specific dates should go in the front I guess

due = unpickle_file("due", dltl.DLTLGroup())
overdue = unpickle_file("overdue", dltl.DLTLGroup())
finished_today = unpickle_file("finished", dltl.DLTLGroup())
asleep = unpickle_file("asleep", dltl.SleeperDLTL())
groups = {"due": due, "overdue": overdue, "finished_today": finished_today}
statuses = {"due": due, "overdue": overdue, "asleep": asleep, "finished": finished_today}

ordinary = {1: "once", 2: "daily", 3: "weekly", 4: "monthly", 5: "seasonally", 6: "yearly"}
week = {1: "monday", 2: "tuesday", 3: "wednesday", 4: "thursday", 5: "friday", 6: "saturday", 7: "sunday"}
months = {1: 'january', 2: 'february', 3: 'march', 4: 'april', 5: 'may', 6: 'june', 7: 'july', 8: 'august',
          9: 'september', 10: 'october', 11: 'november', 12: 'december'}
seasons = {1: "winter", 2:  "spring", 3: "summer", 0: "fall"}
# counting = unpickle_file("counting")
dates = unpickle_file("dates", [])      # An ordered list of dates we are using.

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
            temp = unpickle_file(frequency, None)
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


def _push_file(frequency):
    """Not meant for the end user. Pushes the current state of the given task list into the corresponding file."""
    if in_memory[frequency].size == 0:
        _delete_file(frequency)     # Prevents us saving empty lists and cluttering the folder
    else:
        pickle_into_file(in_memory[frequency], frequency)
    changed.pop(frequency, None)


def _push_special_file(file_name, contents):
    pickle_into_file(contents, file_name)
    changed.pop(file_name, None)


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
    print()
    print("Putting task to sleep. Please input the date you would like the task to awaken on.")
    print("If you would like to give the number of days instead, type 'days'.")
    print()

    if (until := input(f'Type the date in the format YYYY-MM-DD\n')) == "days":
        if (until := _convert_to_date(input(f'Please type in the number of days, without spaces:\n'))) is None:
            print("Error: Did not receive a positive integer. Please try again from the beginning.")
            print()
            until = _set_until_date()

    else:
        try:
            until = date(int(until[0:4]), int(until[5:7]), int(until[8:10]))
        except (ValueError, TypeError, IndexError):
            print("Error: Did not receive a date in the specified format. Please try again from the beginning.")
            print()
            until = _set_until_date()
    return until


def save_changes(namespace):        # The namespace is only to prevent "expected 0 arguments received 1 error"
    """Saves all changes and progress made to all tasks as well as programme configurations."""
    for name, status_list in statuses.items():
        if changed.pop(name, None) is not None:
            _push_special_file(name, status_list)
    if changed.pop("config", None) is not None:
        _push_special_file("config", config)
    hold = changed.pop("dates", None)           # In order for the empty date dltls to get removed properly (1/2)

    for frequency in list(changed.keys()):      # The list is there since we are changed the dict while iterating
        _push_file(frequency)

    if changed.pop("dates", None) is not None or hold is not None:
        _push_special_file("dates", dates)  # and also not meltdown, we have to do it weirdly like this (2/2)

    print("Changes successfully saved!")
    print()


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
          "Do you wish to save data before exiting? (Y/N)\n")
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
            print()
            continue


def list_valid_frequencies(namespace):
    """Displays a list of all valid task frequencies (= trigger conditions)."""
    print()
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
    print()
    print("Last but not least, the following are also supported:")
    for freq in ordinary.values():
        print(f"'{freq}'", end=", ")
    print()
    print()


def _validify_frequency(frequency):
    """Not meant for the end user. Checks whether the user input a frequency supported by the program. If so, formats
    it to the program's needs. More specific frequency restrictions are handled by the caller function itself."""
    frequency = frequency.casefold()
    if (frequency in ordinary.values() or frequency in week.values() or frequency in months.values()
            or frequency in seasons.values() or frequency == "all"):
        return frequency

    # It isn't in the above, so it would have to be a date. If it isn't, then it's not valid
    if len(frequency) != 5:
        print("Error: The inputted frequency could not be matched to a frequency supported by the program, and was"
              "too long/short to be a date. Aborting process.")
        print()
        return None
    try:
        frequency = date(2020, int(frequency[0:2]), int(frequency[3:5]))    # 2020 is a placeholder (leap year)
    except (TypeError, ValueError) as e:
        print(f'Error: The inputted frequency could not be matched to a frequency supported by the program, and '
              f'could not be confirmed as a date -- reason: {e}. Aborting process.')
        print()
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
        print("Error: Cannot create a task with frequency 'all'. Aborting process.")
        print()
        return None

    # Checks other validity concerns
    if frequency == "once" and status == "finished":
        print("Error: Cannot create a 'once' task that is already 'finished'. Task was NOT created.")
        print()
        return None
    temp = _pull_file(frequency)
    if name in temp.glossary:
        print(f'Error: Task with name {name} and frequency {frequency} already exists. Task was NOT created.')
        print()
        return None
    if name in statuses[status].glossary:
        print(f'Error: Task with name {name} and status {status} already exists. Task was NOT created.')
        print()
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
    print()
    return True     # Just to signal successful completion


def create_task_argparse(namespace):
    """Not meant for the end user. Handles the passing of the arguments received from the user by argparse onto
    the create_task() function. Purely for refactoring purposes"""
    namespace.description = ' '.join(namespace.description)
    if create_task(namespace.task_name, namespace.frequency, namespace.description, namespace.status) is None:
        return None


def _fetch_position_from_ld(position: int):
    """Not meant for the end user. Fetches a task node by its position in the last_displayed list."""
    if position < 1 or position > len(last_displayed):
        print("Error: Invalid position. Aborting process.")
        print()
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
    if ld_origin is None:
        print("Error: Please display a list first before trying to access the tasks in it.")
        print()
        return None
    if ld_origin == "unsupported":
        print("Error: The last displayed list is too broad and as such does not allow interaction with tasks. Please "
              "display a more specialized list to access specific tasks.")
        print()
        return None

    task = ' '.join(task)       # From argparse we receive a list
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


def _arglist_into_text(argparse_list):
    """Not meant for the end user. Takes in a list of words created by argparse from user input and recreates the
    text it was originally"""
    return ' '.join(argparse_list)


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

    print()
    print("Task successfully deleted.")
    print()


def change_name(namespace):
    """Changes the name of the specified task."""
    status_copy, frequency_copy = _fetch_both_copies(namespace.target_task)
    new_name = namespace.new
    if frequency_copy is None:  # The status copy may not exist if status == "finished"
        return False

    # First the frequency copy
    freq = _pull_file(frequency_copy.frequency)
    if new_name in freq.glossary:
        print(f'Error: Task with name {new_name} and frequency {frequency_copy.frequency}'
              f'already exists. Name change was aborted.')
        print()
        return False
    freq.rename_node(frequency_copy, new_name)
    _update_dltl(frequency_copy.frequency, freq)

    # Then the status copy
    if status_copy is not None:
        temp = statuses[status_copy.status]
        temp.rename_node(status_copy, new_name)
        changed[status_copy.status] = True

    print()
    print("Task successfully renamed.")
    print()


def _change_freq_ask_user():
    if (response := input("Warning: Changing the frequency of a 'finished' task to 'once' will remove the task."
                          "Do you wish to proceed? (Y/N):\n").casefold()) == "y":
        return True
    elif response == "n":
        print()
        print("Understood. Aborting process.")
        print()
        return False
    else:
        print("Did not understand answer. Please try again.")
        print()
        return _change_freq_ask_user()


def change_frequency(namespace):
    """Changes the frequency (trigger condition) of the specified task."""

    # Checks whether the user inputted a valid frequency
    new_frequency = _validify_frequency(namespace.new)
    if new_frequency is None:
        return None
    elif new_frequency == "all":
        print("Error: Cannot create a task with frequency 'all'.")
        print()
        return None

    status_copy, frequency_copy = _fetch_both_copies(namespace.target_task)
    if frequency_copy is None:  # The status copy may not exist if status == "finished"
        return False
    name, old_frequency = frequency_copy.name, frequency_copy.frequency

    if new_frequency == old_frequency:
        print("Error: The given task already has said frequency. Process aborted.")
        print()
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
        print()
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

    print()
    print("Task frequency change successful.")
    print()


def change_description(namespace):
    """Changes the description of the specified task."""
    status_copy, frequency_copy = _fetch_both_copies(namespace.target_task)
    new_description = ' '.join(namespace.new)
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

    print()
    print("Task description change successful.")
    print()


def _change_status(task, new_status):
    """not for user -- umbrella function -- but not for asleep"""
    status_copy, frequency_copy = _fetch_both_copies(task)
    if frequency_copy is None:  # The status copy may not exist if status == "finished"
        return False

    name, old_status = frequency_copy.name, frequency_copy.status
    if old_status == new_status:
        print(f'Error: The given task is already {new_status}. Aborting process.')
        print()
        return False
    if name in statuses[new_status].glossary:
        print(
            f'Error: Task with name {name} and status {new_status} already exists.'
            f'Aborting process.')
        print()
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
    status_copy = dltl.TaskNode(name, frequency_copy.frequency, frequency_copy.description, new_status)
    statuses[new_status].append_node(status_copy, config["ordering_key"])
    changed[new_status] = True

    print()
    print("Task status change successful.")
    print()


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
        print()
        return False

    frequency_copy.until = _set_until_date()

    # First the frequency copy
    freq = _pull_file(frequency_copy.frequency)
    freq.change_status(frequency_copy, "asleep")
    _update_dltl(frequency_copy.frequency, freq)

    # Then the status copy
    if status_copy is not None:
        temp = statuses[status_copy.status]
        temp.detach_node(status_copy)
        changed[status_copy.status] = True
    status_copy = dltl.TaskNode(frequency_copy.name, frequency_copy.frequency, frequency_copy.description, "asleep", frequency_copy.until)
    asleep.add_sleeper(status_copy)
    changed["asleep"] = True

    print()
    print("Task was successfully set asleep.")
    print()


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
        delete_task(namespace)
        print()
        print("A once task was finished. Keep up the good work!")
        print()
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
    print()


def detail(namespace):
    """Displays all information about the task."""
    task = _fetch_from_ld(namespace.target_task)
    if task is None:
        return None

    print()
    print("Task name:", task.name, "", "Task frequency:", task.frequency, "",
          "Task description:", _prepare_description(task.description), "", "Task status:", task.status, "",
          "Task wake-up date:", task.until, sep="\n")
    print()
    print()


def _display_all_warning():
    print("You are about to tasks from all lists currently logged by the program. "
          "Please note that this may be demanding on your device AND that this display is view only, meaning "
          "you will NOT be able to access or edit task details.")
    if (response := input("Do you wish to proceed? (Y/N)\n").casefold()) == "y":
        return True
    elif response == "n":
        print("Understood. Aborting process.")
        print()
        return False
    else:
        print("Did not understand response. Please try again.")
        print()
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
        finished = namespace.finished

    global last_displayed, ld_origin
    last_displayed, ld_origin = None, "unsupported"

    i = 1
    for frequency in ordinary.values():
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

    print()
    print()
    if i == 1:
        if finished:
            print("You have no finished tasks.")
        else:
            print("You have no tasks. Consider making some!")
    else:
        print("And that is all.")
    print()
    print()


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
        target = statuses[status].members.get(frequency)
        if target is None:
            print("The chosen list is empty.")
            print()
            return None
        last_displayed = target.display_task_names([None] * target.size)
        ld_origin = status

    print()
    print("And that is all.")
    print()


def to_do(namespace):
    """Displays all tasks on today's agenda."""

    if (size := (overdue.size + due.size)) == 0:
        print("You have finished all your tasks. Congratulations!")
        print()
        return
    global last_displayed, ld_origin
    last_displayed = [None] * size
    ld_origin = "to_do"

    initial_index = 1
    print("---- overdue ----")
    print()
    for frequency in overdue.ordering:
        target = overdue.members.get(frequency)
        if target is None:
            continue
        print(frequency, ":", sep="")
        last_displayed, initial_index = target.display_task_names(last_displayed, initial_index)
        print()
    print()
    print("---- due ----")
    print()
    for frequency in due.ordering:
        target = due.members.get(frequency)
        if target is None:
            continue
        print(frequency, ":", sep="")
        last_displayed, initial_index = target.display_task_names(last_displayed, initial_index)
        print()
    print("And that is all.")
    print()
    print()


def display_list_argparse(namespace):
    display_list(namespace.frequency, namespace.status)


def display_status_list(namespace):
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


def _wake_up_sleepers(end_date):
    """Wakes up all sleepers whose wake-up ('until') date is before the end_date (included)
    and appends them to due."""
    while asleep.head is not None and asleep.head.until <= end_date:
        status_copy = asleep.wake_up_head()
        temp = _pull_file(status_copy.frequency)
        frequency_copy = temp.fetch_node(status_copy.name)

        # Prevent name collision
        if status_copy.name in due.glossary:
            status_copy.name = frequency_copy.name = f'{status_copy.name} -- name collision prevention triggered {datetime.now()}'

        status_copy.status = frequency_copy.status = "due"
        status_copy.until = frequency_copy.until = None

        due.append_node(status_copy, config["ordering_key"])
        _update_dltl(frequency_copy.frequency, temp)        # we update asleep and due in the caller


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
        print()
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
    _wake_up_sleepers(today)
    config["last_refresh"] = today
    changed["due"] = changed["overdue"] = changed["asleep"] = changed["finished"] = changed["config"] = True
    # That might not be the case for all, but it doesn't matter, and it is neater this way

    print("Tasks successfully refreshed.")
    print()


def change_config(namespace):
    if namespace.auto_refresh == "true":
        config["auto_refresh"] = True
        print("Auto-refresh enabled.")
    else:
        config["auto_refresh"] = False
        print("Auto-refresh disabled.")
    changed["config"] = True
    print()


def _start_anew():
    """Not meant for the end user. Resets all settings and wipes TO-DO-IQ list clean, then closes the program."""
    for file_name in ordinary.values():
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
    print("Initialization successful. Boot up 'main.py' to begin.")
    exit_without_saving("yay")


if config["auto_refresh"]:
    refresh_to_do("on_startup")
