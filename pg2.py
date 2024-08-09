import json
from os import path
from os import remove
from datetime import date
today = date.today()



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
    if status == "unfinished" and __viability(frequency):
        add it to the list
    print(f'Task "{name}" successfully created!')


def __locate_task(task_list, name):
    position = -1
    i = 0
    while i < len(task_list):
        if task_list[i]["name"] == name:
            position = i
            break
        i += 1
    return position


def __delete_task(task_list, position):
    task_list.pop(position)


def __rename_task(task_list, position, new_name):
    task_list[position]["name"] = new_name


def __change_description(task_list, position, new_description):
    task_list[position]["description"] = new_description


def __print_description(task_list, position):
    return task_list[position]["description"]


# def __change_frequency(task_list, position, new_frequency):
 #   task = task_list[position]
 #   task_list.pop(position)
 #   file1 = __pull_file(task["current"])
 #   hmmm


def __finish_task(task_list, position):
    task_list[position]["status"] = "finished"
    task_list[position]["timestamp"] = today


def __sleep_task(task_list, position, until):
    task_list[position]["status"] = "asleep"
    task_list[position]["until"] = until


def __renew_task(task_list, position):
    task_list[position]["status"] = "finished"
    task_list[position]["timestamp"] = today


def __display_tasks(frequency, status="all"):
    temp = __pull_file(frequency)
    if status == "all":
        output = temp
    else:
        output = [item for item in temp if item["status"] == status]
    return output





create_task("test_task")
