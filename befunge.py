#!/usr/bin/env python
import sys
import befunge


def main(*args):
    if len(args) < 2:
        print("""Usage: {} filename [seconds to pause each step]""".format(str(args[0])))
        return 1
    filename = args[1]
    wait = float(args[2]) if len(args) > 2 else 0
    befunge.run(filename=filename, wait=wait, display=True)
    return 0


if __name__ == '__main__':
    sys.exit(main(*sys.argv))
