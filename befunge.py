#!/usr/bin/env python
import sys
import befunge


def main(*args):
    filename = args[1]
    state = befunge.init_std_befunge_state(filename)
    wait = float(args[2]) if len(args) > 2 else 0
    befunge.run(state, wait=wait, display=True)
    # output = befunge.run(state, wait=wait, display=True)
    # print(output)


if __name__ == '__main__':
    sys.exit(main(*sys.argv))
