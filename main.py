task = "nothing"
due = {"entries": {"daily": [0, {}, {}]}, "glossary": {}}
temp = due["entries"]["monthly"]
print(temp)
temp["length"] += 1
temp["entries"][temp["length"]] = task
temp["glossary"][name] = temp["entries"][temp["length"]]

# Create, delete, mark as done, set asleep, view details, rename, change frequency, change description
