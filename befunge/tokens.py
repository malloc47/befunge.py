from enum import enum

Tokens = enum(NUM='0123456789',
              ADD='+',
              SUB='-',
              MUL='*',
              DIV='/',
              MOD='%',
              LNOT='!',
              GT='`',
              MDIR='><v^',
              RND='?',
              IFLR='_',
              IFUD='|',
              LIT='"',
              DUP=':',
              SWP='\\',
              POP='$',
              POPINT='.',
              POPCHR=',',
              SKP='#',
              PUT='p',
              GET='g',
              NUMIN='&',
              CHRIN='~',
              END='@',
              NOOP=' ')

directions = {
    '>': (0, 1),
    '<': (0, -1),
    'v': (1, 0),
    '^ ': (-1, 0)
}
