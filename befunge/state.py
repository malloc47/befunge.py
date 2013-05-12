from tokens import Tokens, directions

class State(object):
    def __init__(self,board):
        self.pos = (0,0)
        self.direction = Tokens.MDIR[0]
        self.literal = False
        self.board = board
        self.stack = []

    def move(self):
        def wrap(pos,size):
            return pos if pos<size and pos >=0 else (pos-size)%size
        # move pointer and then wrap the coordinates if needed
        self.pos = map(wrap,
                       tuple(
                           map(
                               sum,
                               zip(
                                   self.pos,
                                   directions[self.direction]))),
                       self.board.size())

    def push(self,n): self.stack.append(n)
    def pop(self): return self.stack.pop() if len(self.stack) > 0 else 0
    def peek(self): return self.stack[-1] if len(self.stack) > 0 else 0

    def read(self): return self.board.get(self.pos)

    def __repr__(self):
        return ('<pos: '+str(self.pos)+', direction: '
                +str(self.direction)+', literal: '+str(self.literal))
