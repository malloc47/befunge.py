import unittest
import befunge
import math


def quine(filename):
    with open(filename) as f:
        source = f.read()
    output = befunge.run(filename=filename, display=False)
    return (source, output)


def runner(filename, inpt=[]):
    state = befunge.State(befunge.BefungeBoard(filename))
    state.user_input = inpt
    return befunge.run(state=state, display=False).strip()


def fac_runner(filename, n, prefix=''):
    return (runner(filename, [str(n)]), prefix + str(math.factorial(n)))

def gcd(a, b):
    if b == 0:
        return a
    else:
        return gcd(b, a % b)

def gcd_runner(filename, a, b):
    return (runner(filename, [str(a), str(b)]),
            str(gcd(a, b)))

class TestIntegration(unittest.TestCase):

    def test_hello(self):
        self.assertEqual(runner('code/hello.bf'), 'Hello World!')

    def test_hello2(self):
        self.assertEqual(runner('code/hello2.bf'), 'Hello, world!')

    def test_hello3(self):
        self.assertEqual(runner('code/hello3.bf'), 'Hello, World!')

    def test_quine1(self): self.assertEqual(*quine('code/quine.bf'))

    def test_quine2(self): self.assertEqual(*quine('code/quine2.bf'))

    def test_quine3(self): self.assertEqual(*quine('code/quine3.bf'))

    def test_quine4(self): self.assertEqual(*quine('code/kquine.bf'))

    def test_quine5(self): self.assertEqual(*quine('code/kquine2.bf'))

    def test_quine6(self): self.assertEqual(*quine('code/kquine3.bf'))

    def test_onetwothree(self): self.assertEqual(runner('code/123.bf'), '123')

    def test_count50(self):
        self.assertEqual(runner('code/count50.bf'), '1234567891011121314151617181920212223242526272829303132333435363738394041424344454647484950')

    def test_edgejumptest(self):
        self.assertEqual(runner('code/edgejumptest.bf'), 'yyyy')

    def test_binquine(self):
        self.assertEqual(runner('code/binquine.bf'), '001110100011000001100111001110100011100000110100001010100010110100100001001000110100000001011111001110000011000000110001011100000011000000111110010111110010001100100010001110100011001000100101001110000011011000101010001010110101110000110010001011110011000000110001011001110011000100101101001110100011000000110001011100000011000001011100001000110010001001011111001001000010010000101100001011000010110000101100001011000010110000101100001011000011000100101011')

    def test_fac(self):
        for i in range(1, 15):
            self.assertEqual(*fac_runner('code/fac.bf', i))

    def test_fac2(self):
        for i in range(1, 15):
            self.assertEqual(*fac_runner('code/fac2.bf', i, prefix='Please enter a number:'))

    def test_rand2(self):
        for i in range(10):     # run ten times
            self.assertIn(int(runner('code/rand2.bf')), range(0, 33))

    def test_sieve(self):
        self.assertEqual(runner('code/sieve.bf'), '2357111317192329313741434753596167717379')

    def test_euclid(self):
        for a, b in zip(range(1, 20), reversed(range(1, 20))):
            self.assertEqual(*gcd_runner('code/euclid.bf', a, b))
