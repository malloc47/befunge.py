import sys
from befunge.syntax import Tokens, directions
from befunge.board import BefungeBoard


class State(object):
    """keeps track of all state, along with the board and stack"""

    def __init__(self, board=BefungeBoard()):
        self.pos = (0, 0)
        self.direction = Tokens.MDIR[0]
        self.literal = False
        self.board = board
        self.stack = []
        self.user_input = []
        self.output_spool = ''

    def move(self):
        """handle moving in self.direction and wrapping the board"""
        def wrap(pos, size):
            return pos if pos < size and pos >= 0 else (pos - size) % size
            # move pointer and then wrap the coordinates if needed
        self.pos = tuple(map(wrap,
                             map(
                                 sum,
                                 zip(
                                     self.pos,
                                     directions[self.direction])),
                             self.board.size()))

    def push(self, n): self.stack.append(n)

    def pop(self): return self.stack.pop() if len(self.stack) > 0 else 0

    def peek(self): return self.stack[-1] if len(self.stack) > 0 else 0

    def read(self): return self.board.get(self.pos)

    def inpt(self, one=False):
        # try to read from user_input first, in cause we're being
        # automated instead of interactively run
        try:
            return self.user_input.pop()
        except:
            return sys.stdin.read(1) if one else input()

    def output(self, s, display=True):
        """either spool up the output strings or push them to stdout"""
        if not s: return
        if display:
            sys.stdout.write(str(s))
            sys.stdout.flush()
        else:
            self.output_spool += s

    def __repr__(self):
        return ('<pos: ' + str(self.pos) + ', direction: '
                + str(self.direction) + ', literal: ' + str(self.literal))
