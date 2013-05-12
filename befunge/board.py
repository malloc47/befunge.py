def get_size(filename):
    rows = 0
    cols = 0
    i=0
    j=0
    with open(filename) as f:
        while True:
            c = f.read(1)
            if not c:
                break
            if c == '\n':
                j = 0
                i += 1
            else:
                cols = max(j,cols)
                j += 1
        rows = max(i+1,rows)
    return (rows,cols+1)

class BefungeBoard(object):
    def __init__(self,filename=None):
        # autocompute size
        if filename:
            rows,cols = get_size(filename)
        else:
            rows,cols = 25,80
        self.board = [[' ' for j in range(cols)] for i in range(rows)]
        if filename:
            self.read(filename)

    def size(self):
        return (len(self.board),len(self.board[0]))

    def get(self,pos):
        return self.board[pos[0]][pos[1]]

    def put(self,pos,v):
        self.board[pos[0]][pos[1]] = v

    def read(self,filename):
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
                    self.put((i,j),c)
                    j += 1

    def __repr__(self):
        """a pretty-print, to avoid messy console dumps"""
        return '\n'.join(
            [ ''.join(self.board[i]).rstrip() 
              for i in range(len(self.board))]
        ).rstrip()
