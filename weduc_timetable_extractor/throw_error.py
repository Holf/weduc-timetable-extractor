import sys


def throw_error(error_message):
    sys.stderr.write("\n" + error_message + "\n")
    sys.exit(2)
