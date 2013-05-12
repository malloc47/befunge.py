#!/usr/bin/env python
import sys,os
import befunge.interpreter

def main(*args):
    filename = args[1]
    state = befunge.interpreter.init_std_befunge_state(filename)
    wait = float(args[2]) if len(args)>2 else 0
    befunge.interpreter.run(state,wait=wait)

if __name__ == '__main__':
    sys.exit(main(*sys.argv))
