from datetime import date, datetime, timedelta
beginning = date(2024,1,1)
dates = []
for shift in range(366):
    delta = timedelta(shift)
    dates.append(beginning + delta)

x = ["once", "daily", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""]

print(str(date.today()))
