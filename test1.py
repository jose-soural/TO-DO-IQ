import argparse


def tester(namespace):
    print("Hello!")


entry_parser = argparse.ArgumentParser(prog="TO-DO-IQ",
                                       description="An intelligent TO-DO list. Supports a wide variety of task"
                                                   "frequencies and handles automatic renewing of tasks.",
                                       epilog="----------\nHelp displayed. Continuing execution."
                                       )
# One subparser for each end-user function
commands = entry_parser.add_subparsers(title="Available commands:", required=True)

p_test = commands.add_parser("test", aliases=['t'], help="Just a test.")
p_test.set_defaults(func=tester)

try:
    p_test = entry_parser.parse_args(["test"])
    p_test.func(p_test)
except SystemExit as e:
    print(f'{e} Occurred. Continuing on...')
