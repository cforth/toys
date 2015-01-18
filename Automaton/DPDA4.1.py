#!/usr/bin/env python3.4

"""Deterministic PushDown Automaton，DPDA"""

# "Understanding Computation: Impossible Code and the Meaning of Programs"
# Chapter 4.1 's Code. Use Python3.
# Authors: Chai Fei

class Stack(object):
    """ The realization of the stack
    """
    def __init__(self, contents):
        self.contents = contents

    def push(self, character):
        return Stack([character] + self.contents)

    @property
    def pop(self):
        return Stack(self.contents[1:])

    @property
    def top(self):
        return self.contents[0]

    def __str__(self):
        top = self.contents[0]
        underside = ''.join(self.contents[1:])
        return '#<Stack ({top})#{underside}>'.format(**locals())

    __repr__ = __str__


## UnitTest
import unittest

class TestDPDA(unittest.TestCase):
    """ Tests of the books's code
    """
        
    def test_stack(self):
        stack = Stack(['a','b','c','d','e'])
        self.assertEqual(str(stack), '#<Stack (a)#bcde>')
        self.assertEqual(stack.pop.pop.top, 'c')
        self.assertEqual(stack.push('x').push('y').top, 'y')
        self.assertEqual(stack.push('x').push('y').pop.top, 'x')


if __name__ == '__main__':
    unittest.main()
