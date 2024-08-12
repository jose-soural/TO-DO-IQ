import json
from os import path
from os import remove
from datetime import date, timedelta
import heapq
today = date.today()
due = []
overdue = []
sleepers = []
finished_today = []
displayed_list = []


def __to_date(days):
    delta = timedelta(days)
    return today + delta

x = __to_date(-1089)
if x < today:
    print("Oh, no no")
