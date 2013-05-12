# befunge.py
Basic befunge interpreter written in Python

## Description

This interpreter implements (to a reasonable degree of conformance)
the [Befunge 93 spec][1].  The aim was to write in an fully-formed
engineering style rather than code golf, though liberties were taken
with using a functional style where immutable datastructures were
concerned.

## Features

- Python 2/3 compatible.  Tested on Python 2.7.3, 2.7.4, 3.2.3, and
  3.3.1, as well as 2.6.6 (though unit tests do not run on this
  version).
  
- Unit and integration test suite, which can be run with
  `./runtests.sh`.
  
- Reasonably `pep8` compliant (modulo assorted minor warnings) and
  `pyflakes` linted.
  
- Extensible syntax--adding new symbols is as straightforward as
  adding a new token in `befunge.syntax` and then writing an
  evaluation in `befunge.evaluation`.  Metaprogramming plumbing will
  take care of the rest.
  
- Multiple backends for befunge grids are possible by extending the
  abstract `Board` class in `befunge.board`.  The current
  implementation, `BefungeBoard`, uses nested lists, but an additional
  backend might leverage `numpy` or other higher-performance
  alternatives.
  
## Differences From Befunge 93 C Reference Implementation

There are several tradeoffs made to keep this implementation simple
relative to the [C reference implementation][6] of Befunge 93.
Specifically, the current board backend stores everything as plain
Python (yes, autopromoting and possibly negative) `int` types.
Befunge programs that rely on C-style char/int behavior will probably
not work with `befunge.py`.

Different from the reference implementation, `befunge.py` simply fails
on division by zero instead of asking the user.  Since Python has a
cleaner separation between `chr` and `int`, this implementation uses
an integer grid instead of a char grid, though there are still limits
as to the type of data that may be placed in the grid compared with
the C reference implementation.

Finally, some Befunge programs are not fully conformant with the spec,
and rely on non-standard grid sizes, non-terminating behavior when
non-instruction characters are encountered, or specific integer
specifications (see above).  To accommodate different program sizes,
`befunge.py` will resize the grid larger than the 80x25 specification
if needed to fit a large program, but otherwise makes 80x25 the
minimum for all programs run.  Like the C reference implementation
(which can be toggled), `befunge.py` will treat all non-instruction
symbols as noops, not just the space character.

Though not extensively compared, this implementation shares some
aspects in common with [befungee][4] and the [online JavaScript][5]
befunge interpreter.  These implementations appear to make similar
tradeoffs relative to the C reference implementation, and fail on
similar programs.

## Usage

Befunge code can be run from the command line with

    ./befunge.py code/hello.bf
    
To slow down the computation, the number of seconds of wait time per
step can be specified as well, e.g.,

    ./befunge.py code/hello.bf 0.01
    
Since many steps may not produce output, small numbers for this wait
time (0.01 to 0.001) are probably best for many programs.

To programmatically use the interpreter, simply `import befunge` and
use the `run` command, which can be called in a number of ways:

```python
import befunge
# standalone
befunge.run(filename='code/hello.bf')
# to string instead of stdout
str_output = befunge.run(filename='code/hello.bf',display=False)
print(str_output)
# with a modifiable state variable
state = befunge.State(befunge.BefungeBoard('code/hello.bf'))
state.pos = (3,5)
befunge.run(state=state)
```
    
Examine both `befunge.py` and `tests/{unit,integration}.py` for more
examples of usage.


## Befunge Code Attribution

The befunge programs in `code/` were taken from [here][2] and
[here][3], as well as wikis and a few other assorted locations
scattered around the internet.

## License

All those components that are not obtained elsewhere are Copyright
2013 Jarrell Waggoner. All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are
met:

   1. Redistributions of source code must retain the above copyright
      notice, this list of conditions and the following disclaimer.

   2. Redistributions in binary form must reproduce the above
      copyright notice, this list of conditions and the following
      disclaimer in the documentation and/or other materials provided
      with the distribution.

THIS SOFTWARE IS PROVIDED BY JARRELL WAGGONER ''AS IS'' AND ANY
EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL JARRELL WAGGONER OR
CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


---

Jarrell Waggoner  
/-/ [malloc47.com](http://www.malloc47.com)


[1]: https://github.com/catseye/Befunge-93/blob/master/doc/Befunge-93.markdown
[2]: https://github.com/programble/befungee/tree/master/examples
[3]: https://github.com/catseye/Befunge-93/tree/master/eg
[4]: https://github.com/programble/befungee
[5]: http://www.quirkster.com/iano/js/befunge.html
[6]: https://github.com/catseye/Befunge-93
