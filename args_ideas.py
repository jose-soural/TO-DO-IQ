import argparse

parser = argparse.ArgumentParser(
                    prog='ProgramName -- něco výstižného',
                    description='What the program does',
                    argument_default=False,
                    epilog='Text at the bottom of help')

parser.add_argument('filename')           # positional argument
parser.add_argument('-c', '--count')      # option that takes a value
parser.add_argument('-v', '--verbose',
                    action='store_true')  # on/off flag

args = parser.parse_args()
print(args.filename, args.count, args.verbose)


User defined functions can be used as well:
def hyphenated(string):
    return '-'.join([word[:4] for word in string.casefold().split()])

parser = argparse.ArgumentParser()
_ = parser.add_argument('short_title', type=hyphenated)
parser.parse_args(['"The Tale of Two Cities"'])
Namespace(short_title='"the-tale-of-two-citi')


argument default