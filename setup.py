import sys
import functions

if (response := input("Do you wish to clear all settings and tasks, starting fresh with an empty"
                      "TO-DO-IQ list? (yes/no)").casefold()) == "yes":
    functions._start_anew()
    print("Initialization successful. Boot up 'main.py' to begin.")
else:
    print("User did not confirm. Aborting process.")
sys.exit(42)
