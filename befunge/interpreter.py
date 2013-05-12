import sys
from tokens import Tokens
from semantic import token_fn as actions
from semantic import handle_literal

def show_output(result):
    if result:
        sys.stdout.write(str(result))

def run(state,wait=0):
    """
    befunge interpreter driver that simply follows:

    1) read from cell
    2) modify the stack as needed
    3) show output if relevant
    4) move PC
    5) stop if @ is reached
    """
    while True:
        token = state.read()

        if token == Tokens.END:
            break

        output = (actions[token](state,token)
                  if not state.literal
                  else handle_literal(state,token))
        show_output(output)

        state.move()

        # allow us to slow down the simulation
        if wait:
            import time
            time.sleep(wait)

def init_std_befunge_state(filename):
    from state import State
    from board import BefungeBoard
    return State(BefungeBoard(filename=filename)) # defaults to 25x80
