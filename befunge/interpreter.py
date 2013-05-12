from tokens import Tokens
from semantic import token_fn as actions
from semantic import handle_literal

def run(state,wait=0,display=True):
    """
    befunge interpreter driver that simply follows:

    1) read from cell
    2) modify the stack as needed
    3) show output if relevant
    4) move PC
    5) stop if @ is reached
    """
    while True:
        # import pdb; pdb.set_trace()
        token = state.read()

        if token == Tokens.END and not state.literal:
            break

        output = (actions[token](state,token)
                  if not state.literal
                  else handle_literal(state,token))
        state.output(output,display)

        state.move()

        # print(str(token)+' : ' +str(state.stack))

        # allow us to slow down the simulation
        if wait:
            import time
            time.sleep(wait)
    return state.output_spool

def init_std_befunge_state(filename):
    from state import State
    from board import BefungeBoard
    return State(BefungeBoard(filename=filename)) # defaults to 25x80
