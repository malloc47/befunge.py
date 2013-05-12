from syntax import Tokens
from evaluation import evaluations as actions
from evaluation import handle_literal
from state import State
from board import BefungeBoard


def run(filename=None, state=None, wait=0, display=True):
    """
    befunge interpreter driver that does the following:
    1) read from cell
    2) modify the stack as needed
    3) show output if relevant
    4) move PC
    5) stop if @ is reached
    """

    if not state and not filename:
        raise ValueError('neither filename or state specified')

    if not state and filename:
        state = State(BefungeBoard(filename=filename))

    while True:
        # import pdb; pdb.set_trace()
        token = chr(state.read())

        if token == Tokens.END and not state.literal:
            break

        try:
            output = (actions[token](state, token)
                      if not state.literal
                      else handle_literal(state, token))
        except KeyError:        # ignore unsupported tokens
            output = ''

        state.output(output, display)

        state.move()

        # print(str(token)+' : ' +str(state.stack))

        # allow us to slow down the simulation
        if wait:
            import time
            time.sleep(wait)
    return state.output_spool
