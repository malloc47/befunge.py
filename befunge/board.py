def get_size(filename):
    """
    helper function that reads in the file to determine the grid size
    needed
    """
    rows = 1         # there must be one row
    cols = 0
    i = 0
    j = 0
    with open(filename) as f:
        while True:
            c = f.read(1)
            if not c:
                break
            if c == '\n':
                j = 0
                i += 1
            else:
                j += 1
                cols = max(j, cols)
        rows = max(i, rows)
    return (rows, cols)


class BefungeBoard(object):
    """
    wraps a matrix and provides getters/setters that cast from chr to
    int, as well as reading from flat files
    """
    def __init__(self, filename=None):
        rows, cols = 0, 0
        # autocompute size
        if filename:
            rows, cols = get_size(filename)
        rows, cols = max(rows, 25), max(cols, 80)
        self.board = [[ord(' ') for j in range(cols)] for i in range(rows)]
        if filename:
            self.read(filename)

    def size(self):
        return (len(self.board), len(self.board[0]))

    def get(self, pos):
        try:
            return self.board[pos[0]][pos[1]]
        except:
            return ord(' ')

    def put(self, pos, v):
        # auto-convert to numeric value if chr
        if type(v) is str and len(v) == 1:
            val = ord(v)
        elif type(v) is int:
            val = v
        else:
            raise TypeError
        try:
            self.board[pos[0]][pos[1]] = val
        except:
            pass

    def read(self, filename):
        i = 0
        j = 0
        with open(filename) as f:
            while True:
                c = f.read(1)
                if not c:
                    break
                if c == '\n':
                    j = 0
                    i += 1
                else:
                    self.put((i, j), c)
                    j += 1

    def __repr__(self):
        """a pretty-print, to avoid messy console dumps"""
        return '\n'.join(
            [''.join(map(chr, self.board[i])).rstrip()
             for i in range(len(self.board))]
        ).rstrip()
