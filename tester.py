from datetime import date, timedelta
begin = date(2020, 1, 1)
i = -366
asd = {}

ordinary = {1: "once", 2: "daily", 3: "weekly", 4: "monthly", 5: "seasonally", 6: "yearly"}
week = {1: "monday", 2: "tuesday", 3: "wednesday", 4: "thursday", 5: "friday", 6: "saturday", 7: "sunday"}
months = {1: 'january', 2: 'february', 3: 'march', 4: 'april', 5: 'may', 6: 'june', 7: 'july', 8: 'august',
          9: 'september', 10: 'october', 11: 'november', 12: 'december'}
seasons = {1: "winter", 2:  "spring", 3: "summer", 4: "fall"}

for k in range(366):
    asd[begin] = i
    i += 1
    begin += timedelta(1)

j = 1
for item in ordinary.values():
    asd[item] = j
    j += 1
for item in week.values():
    asd[item] = j
    j += 1
for item in months.values():
    asd[item] = j
    j += 1
for item in seasons.values():
    asd[item] = j
    j += 1

print(asd)
