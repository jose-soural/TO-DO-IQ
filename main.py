test1 = [{"name": "test_task1", "description": "", "status": "unfinished"}, {"name": "test_task2", "description": "", "status": "unfinished"}]
test2 = [i for i in test1 if "1" in i["name"]]

print("test2:\n", test2)
test2[0]["name"] = "success!"
print("test1:\n", test1)

# Create, delete, set asleep, view details, rename, change frequency, change description
