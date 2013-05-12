import sys
import operator as op
from functools import partial
import random
import inspect
from tokens import Tokens


def partial_application(f, *args):
    """this wrapper insures that the __module__ property is set to make
    some metaprogramming work out below """
    out = partial(f, *args)
    out.__module__ = __name__
    return out


def num(s, t): s.push(int(t))


def op_binary(f, s, t):
    a, b = s.pop(), s.pop()
    s.push(f(b, a))


add = partial_application(op_binary, op.add)
sub = partial_application(op_binary, op.sub)
mul = partial_application(op_binary, op.mul)
div = partial_application(op_binary, op.floordiv)  # ignore the "ask the user" part
mod = partial_application(op_binary, op.mod)
gt = partial_application(op_binary, op.gt)

def lnot(s, t): s.push(1 if s.pop() == 0 else 0)

def mdir(s, t): s.direction = t

def rnd(s, t): s.direction = random.choice(Tokens.MDIR)

def iflr(s, t): s.direction = Tokens.MDIR[0 if s.pop() == 0 else 1]

def ifud(s, t): s.direction = Tokens.MDIR[(0 if s.pop() == 0 else 1) + 2]

def lit(s, t): s.literal = not s.literal

def dup(s, t): s.push(s.peek())

def swp(s, t):
    a, b = s.pop(), s.pop()
    s.push(a)
    s.push(b)

def pop(s, t): s.pop()

def popint(s, t): return str(s.pop())

def popchr(s, t): return str(chr(s.pop()))

def skp(s, t): s.move()

def put(s, t):
    i, j, v = s.pop(), s.pop(), s.pop()
    if v in range(256):
        s.board.put((i, j), chr(v))
    else:
        s.board.put((i, j), v)  # allow non-char storage

def get(s, t):
    i, j = s.pop(), s.pop()
    s.push(s.board.get((i, j)))

def numin(s, t): return s.push(int(s.inpt()))

def chrin(s, t): return s.push(ord(s.inpt(one=True)))

def noop(s, t): return

def handle_literal(s, t):
    if t == Tokens.LIT:
        s.literal = not s.literal
    else:
        s.push(ord(t))

# Below here is some metaprogramming which kicks out a dictionary that
# associates individual token characters with the (lowercased)
# functions above

# grab functions from this module
__fnmembers__ = dict([f for f in inspect.getmembers(sys.modules[__name__])
                      if getattr(f[1], '__module__', '') == __name__])

def str_list_to_dict(lst):
    """
    We have some tokens that are associated with more than one
    character.  Here, we place all single character tokens directly
    into the dict, and then expand the tokens that have more than one
    character and duplicate them individually into the dict with the
    same value.

    """
    d = dict([(k, v) for k, v in lst if len(k) == 1])
    d.update(reduce(op.add, [[(c, v) for c in k]
                             for k, v in lst if len(k) > 1], []))
    return d

# associate token names with the (lowercased) function names in this
# module if there's a match
token_fn = str_list_to_dict([(Tokens[k], __fnmembers__[k.lower()])
                             for k in Tokens.keys() if k.lower() in
                             __fnmembers__])
