from datetime import date
today = date.today()
configuration = {"last_refresh": None, "another_key": "something"}
last_refresh = None

# User configurations of the program
refresh_auto = False
season_starts = [date(today.year, 3, 1), date(today.year, 6, 1), date(today.year, 9, 1), date(today.year, 12, 1)]


def copy_content(file):
    with open(file, encoding="utf-8") as f:
        size = int(f.readline())
        a = [""]*size
        i = 0
        for line in f:
            a[i] = line
            i += 1
    print(a)
    with open("test2.txt", "w", encoding="utf-8") as f:
        f.write(f'{i}\n')
        for task in a:
            f.write(task)


copy_content("test.txt")
