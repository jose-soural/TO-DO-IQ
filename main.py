def lol(user_input):
    ld = last_displayed
    if ld["source"] in special:
        if ld["frequency"] == "all":
            freq_list = [(i, ordering[i]) for i in ld["source"]["frequencies"].keys()].sort(key=lambda x: x[1])
            for freq in freq_list:
                print(freq[0])
                ld["source"]["frequencies"][freq[0]].display_tasks()
        else:
            temp = ld["source"]["frequencies"].get(["frequency"])
    else:
        temp = _pull_file(ld["source"])

    if user_input.isdigit():
        task = temp.fetch_node_at_position(user_input).task
    else:
        task = temp.fetch_task(user_input)
    return task