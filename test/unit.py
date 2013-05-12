import unittest
import befunge.state as state
import befunge.evaluation as evaluation
from befunge.board import BefungeBoard


class TestState(unittest.TestCase):

    def setUp(self):
        self.state = state.State(BefungeBoard())

    def test_move_left(self):
        self.state.move()
        self.assertEqual(self.state.pos, (0, 1))

    def test_move_right(self):
        self.state.move()
        self.state.direction = '<'
        self.state.move()
        self.assertEqual(self.state.pos, (0, 0))

    def test_move_down(self):
        self.state.direction = 'v'
        self.state.move()
        self.assertEqual(self.state.pos, (1, 0))

    def test_move_up(self):
        self.state.direction = 'v'
        self.state.move()
        self.state.direction = '^'
        self.state.move()
        self.assertEqual(self.state.pos, (0, 0))

    def test_left_wrap(self):
        self.state.direction = '<'
        self.state.move()
        self.assertEqual(self.state.pos, (0, 79))

    def test_right_wrap(self):
        self.state.pos = (0, 79)
        self.state.move()
        self.assertEqual(self.state.pos, (0, 0))

    def test_top_wrap(self):
        self.state.direction = '^'
        self.state.move()
        self.assertEqual(self.state.pos, (24, 0))

    def test_bottom_wrap(self):
        self.state.direction = 'v'
        self.state.pos = (24, 0)
        self.state.move()
        self.assertEqual(self.state.pos, (0, 0))

    def test_stack_push(self):
        self.state.push(1)
        self.state.push(2)
        self.state.push(3)
        self.assertEqual(self.state.stack, [1, 2, 3])

    def test_stack_pop(self):
        self.state.push(1)
        self.state.push(2)
        self.state.push(3)
        self.assertEqual(self.state.pop(), 3)
        self.assertEqual(self.state.stack, [1, 2])
        self.assertEqual(self.state.pop(), 2)
        self.assertEqual(self.state.stack, [1])
        self.assertEqual(self.state.pop(), 1)
        self.assertEqual(self.state.stack, [])
        self.assertEqual(self.state.pop(), 0)  # befunge special behavior
        self.assertEqual(self.state.stack, [])

    def test_stack_peek(self):
        self.state.push(1)
        self.state.push(2)
        self.state.push(3)
        self.assertEqual(self.state.peek(), 3)
        self.state.pop()
        self.state.pop()
        self.state.pop()
        self.assertEqual(self.state.peek(), 0)


class TestBoard(unittest.TestCase):

    def test_size(self):
        self.assertEqual(BefungeBoard().size(), (25, 80))  # befunge size
        # test if board sizes up appropriately when given larger input
        self.assertEqual(BefungeBoard('code/valix.bf').size(), (25, 98))

    def test_get(self):
        b = BefungeBoard('code/hello.bf')
        self.assertEqual(b.get((0, 0)), ord('>'))
        self.assertEqual(b.get((0, 15)), ord('v'))
        self.assertEqual(b.get((2, 1)), ord('4'))
        self.assertEqual(b.get((4, 5)), ord('@'))
        self.assertEqual(b.get((24, 79)), ord(' '))
        self.assertEqual(b.get((500, 500)), ord(' '))

    def test_put(self):
        b = BefungeBoard('code/hello.bf')
        b.put((0, 0), '@')
        self.assertEqual(b.get((0, 0)), ord('@'))
        b.put((500, 500), '@')
        self.assertEqual(b.get((500, 500)), ord(' '))


class TestSemantic(unittest.TestCase):

    def setUp(self):
        self.state = state.State(BefungeBoard())

    def test_num(self):
        evaluation.num(self.state, '0')
        self.assertEqual(self.state.peek(), 0)
        evaluation.num(self.state, '5')
        self.assertEqual(self.state.peek(), 5)
        evaluation.num(self.state, '10')
        self.assertEqual(self.state.peek(), 10)
        evaluation.num(self.state, '-2')  # not actually in spec
        self.assertEqual(self.state.peek(), -2)

    def test_add(self):
        evaluation.add(self.state, '+')
        self.assertEqual(self.state.peek(), 0)
        self.state.push(1)
        self.state.push(1)
        evaluation.add(self.state, '+')
        self.assertEqual(self.state.peek(), 2)
        self.state.push(1)
        evaluation.add(self.state, '+')
        self.assertEqual(self.state.peek(), 3)

    def test_not(self):
        evaluation.lnot(self.state, '!')
        self.assertEqual(self.state.peek(), 1)
        evaluation.lnot(self.state, '!')
        self.assertEqual(self.state.peek(), 0)
        self.state.push(5)
        evaluation.lnot(self.state, '!')
        self.assertEqual(self.state.peek(), 0)
        self.state.pop()
        self.state.pop()
        evaluation.lnot(self.state, '!')
        self.assertEqual(self.state.peek(), 1)

    def test_mdir(self):
        evaluation.mdir(self.state, '^')
        self.assertEqual(self.state.direction, '^')

    def test_rnd(self):
        evaluation.rnd(self.state, '?')
        self.assertIn(self.state.direction, ['>', '<', 'v', '^'])

    def test_iflr(self):
        evaluation.iflr(self.state, '_')
        self.assertIn(self.state.direction, ['>', '<'])

    def test_ifud(self):
        evaluation.ifud(self.state, '|')
        self.assertIn(self.state.direction, ['v', '^'])

    def test_lit(self):
        evaluation.lit(self.state, '"')
        self.assertTrue(self.state.literal)
        evaluation.lit(self.state, '"')
        self.assertFalse(self.state.literal)

    def test_dup(self):
        self.state.push(4)
        evaluation.dup(self.state, ':')
        self.assertEqual(self.state.stack[-2:], [4, 4])
        self.state.push(7)
        evaluation.dup(self.state, ':')
        self.assertEqual(self.state.stack[-2:], [7, 7])

    def test_swp(self):
        evaluation.swp(self.state, '\\')
        self.assertEqual(self.state.stack[-2:], [0, 0])
        self.state.push(4)
        self.state.push(7)
        self.assertEqual(self.state.stack[-2:], [4, 7])
        evaluation.swp(self.state, '\\')
        self.assertEqual(self.state.stack[-2:], [7, 4])

    def test_popint(self):
        self.assertEqual(evaluation.popint(self.state, '.'), '0')
        self.state.push(27)
        self.assertEqual(evaluation.popint(self.state, '.'), '27')
        self.state.push(-92)
        self.assertEqual(evaluation.popint(self.state, '.'), '-92')

    def test_popchr(self):
        self.assertEqual(evaluation.popchr(self.state, ', '), '\x00')
        self.state.push(47)
        self.assertEqual(evaluation.popchr(self.state, ', '), '/')
        self.state.push(94)
        self.assertEqual(evaluation.popchr(self.state, ', '), '^')

    def test_skp(self):
        evaluation.skp(self.state, '#')
        self.assertEqual(self.state.pos, (0, 1))

    def test_put(self):
        self.state.push(76)
        self.state.push(3)
        self.state.push(2)
        evaluation.put(self.state, 'p')
        self.assertEqual(self.state.board.get((2, 3)), ord('L'))

    def test_get(self):
        self.state.board.put((3, 2), 'K')
        self.state.push(2)
        self.state.push(3)
        evaluation.get(self.state, 'g')
        self.assertEqual(self.state.peek(), ord('K'))

if __name__ == '__main__':
    unittest.main()
