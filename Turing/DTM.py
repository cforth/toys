#!/usr/bin/env python3.4

"""Deterministic Turing Machine，DTM"""

# "Understanding Computation: Impossible Code and the Meaning of Programs"
# Chapter 5 's Code. Use Python3.
# Authors: Chai Fei

class Tape(object):
    def __init__(self, left, middle, right, blank):
        self.left = left
        self.middle = middle
        self.right = right
        self.blank = blank

    def __str__(self):
        left = ''.join(self.left)
        middle = self.middle
        right = ''.join(self.right)
        return '#<Tape {left}({middle}){right}>'.format(**locals())

    __repr__ = __str__

    def write(self, character):
        return Tape(self.left, character, self.right, self.blank)

    @property
    def move_head_left(self):
        left = [] if not self.left else self.left[:-1]
        middle = self.blank if not self.left else self.left[-1]
        right = [self.middle] + self.right
        return Tape(left, middle, right, self.blank)

    @property
    def move_head_right(self):
        left = self.left + [self.middle]
        middle = self.blank if not self.right else self.right[0]
        right = [] if not self.right else self.right[1:]
        return Tape(left, middle, right, self.blank)


class TMConfiguration(object):
    def __init__(self, state, tape):
        self.state = state
        self.tape = tape


class TMRule(object):
    def __init__(self, state, character, next_state, write_character, direction):
        self.state = state
        self.character = character
        self.next_state = next_state
        self.write_character = write_character
        self.direction = direction

    def applies_to(self, configuration):
        return self.state == configuration.state and self.character == configuration.tape.middle


## UnitTest
import unittest

class TestDTM(unittest.TestCase):
    """ Tests of the books's code
    """
        
    def test_Tape(self):
        tape = Tape(['1', '0', '1'], '1', [], '_')
        self.assertEqual(str(tape), '#<Tape 101(1)>')
        self.assertEqual(tape.middle, '1')
        self.assertEqual(str(tape.move_head_left), '#<Tape 10(1)1>')
        self.assertEqual(str(tape.write('0')), '#<Tape 101(0)>')
        self.assertEqual(str(tape.move_head_right), '#<Tape 1011(_)>')
        self.assertEqual(str(tape.move_head_right.write('0')), '#<Tape 1011(0)>')

    def test_TMRule(self):
        rule = TMRule(1, '0', 2, '1', 'right')
        self.assertEqual(rule.applies_to(TMConfiguration(1, Tape([], '0', [], '_'))), True)
        self.assertEqual(rule.applies_to(TMConfiguration(1, Tape([], '1', [], '_'))), False)
        self.assertEqual(rule.applies_to(TMConfiguration(2, Tape([], '0', [], '_'))), False)


if __name__ == '__main__':
    unittest.main()
