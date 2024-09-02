import sys
import functions

if (response := input("Do you wish to clear all settings and tasks, starting fresh with an empty"
                      "TO-DO-IQ list? (Y/N)\n").casefold()) == "y":
    print()
    functions._start_anew()
else:
    print("User did not confirm. Aborting process.")
    print()
sys.exit(42)
