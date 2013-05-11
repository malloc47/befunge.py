#!/usr/bin/env python
import sys,os
import befunge.interpreter

def main(*args):
    filename = args[1]
    state = befunge.interpreter.init_std_befunge_state(filename)
    befunge.interpreter.run(state)

if __name__ == '__main__':
    sys.exit(main(*sys.argv))
