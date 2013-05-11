import sys
import operator as op
from functools import partial
import random
import inspect
from tokens import Tokens

def num(s,t): s.push(int(t))

def op_binary(f,s,t):
    a, b = s.pop(), s.pop()
    s.push(f(b,a))

add = partial(op_binary, op.add)
sub = partial(op_binary, op.sub)
mul = partial(op_binary, op.mul)
div = partial(op_binary, op.floordiv) # ignore the "ask the user" part
mod = partial(op_binary, op.mod)
gt  = partial(op_binary, op.gt)

def lnot(s,t): s.push(1 if s.pop()==0 else 0)

def mdir(s,t): s.direction = t

def rnd(s,t): s.direction = random.choice(Tokens.MDIR)

def iflr(s,t): s.direction = Tokens.MDIR[0 if s.pop()==0 else 1]

def ifud(s,t): s.direction = Tokens.MDIR[(0 if s.pop()==0 else 1)+2]

def lit(s,t): s.literal = not s.literal

def dup(s,t): s.push(s.peek())

def swp(s,t):
    a, b = s.pop(), s.pop()
    s.push(a)
    s.push(b)

def pop(s,t): s.pop()

def popint(s,t): return s.pop()

def popchr(s,t): return chr(s.pop())

def skp(s,t): s.move()

def put(s,t):
    i, j, v = s.pop(), s.pop(), s.pop()
    s.board.put((i,j),chr(v))

def get(s,t):
    i, j = s.pop(), s.pop()
    s.push(ord(s.board.get((i,j))))

def numin(s,t): return 47       # todo: get number as input

def chrin(s,t): return 'j'      # todo: get char as input

def noop(s,t): return

def handle_literal(s,t):
    if t == Tokens.LIT:
        s.literal = not s.literal
    else:
        s.push(ord(t))

# Below here is some metaprogramming which kicks out a dictionary that
# associates individual token characters with the (lowercased)
# functions above

# grab functions from this module
__fnmembers__ = dict(inspect.getmembers(sys.modules[__name__], inspect.isfunction))

def str_list_to_dict(lst):
    """
    We have some tokens that are associated with more than one
    character.  Here, we place all single character tokens directly
    into the dict, and then expand the tokens that have more than one
    character and duplicate them individually into the dict with the
    same value.

    """
    d = dict([(k,v) for k,v in lst if len(k)==1])
    d.update(reduce(op.add,[ [ (c,v) for c in k] 
                             for k,v in lst if len(k)>1],[]))
    return d

# associate token names with the (lowercased) function names in this
# module if there's a match
token_fn = str_list_to_dict([ (Tokens[k], __fnmembers__[k.lower()])
                              for k in Tokens.keys() if k.lower() in
                              __fnmembers__ ])
