from datetime import date, timedelta
beginning = date(2024,1,1)
dates = []
for shift in range(366):
    delta = timedelta(shift)
    dates.append(beginning + delta)

x = ["once", "daily", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""]

print((date.today()-beginning).days.is_integer())
print(timedelta(15).days)
print(str(timedelta(15)))
