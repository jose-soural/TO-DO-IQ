#example = [2, {1: {"name": "test_task", "description": "", "status": "unfinished"}, 2: {"name": "test_task_no2", "description": "", "status": "unfinished"}}, {"name": {"name": "test_task", "description": "", "status": "unfinished"}}]
#example[2]["name2"] = example[1][2]
#example[2]["name"] = example[1][2]
#print(example)

due = [{"daily": [0,{},{}]},{}]
temp = [{1: "a", 2: "b"},{}]
for item in due[0][3]:
    print("Yahaha!")


# Create, delete, mark as done, set asleep, view details, rename, change frequency, change description
