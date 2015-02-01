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

    def __str__(self):
        state = self.state
        tape = self.tape
        return '#<struct TMConfiguration state={state}, tape={tape}>'.format(**locals())

    __repr__ = __str__


class TMRule(object):
    def __init__(self, state, character, next_state, write_character, direction):
        self.state = state
        self.character = character
        self.next_state = next_state
        self.write_character = write_character
        self.direction = direction

    def applies_to(self, configuration):
        return self.state == configuration.state and self.character == configuration.tape.middle

    def follow(self, configuration):
        return TMConfiguration(self.next_state, self.next_tape(configuration))

    def next_tape(self, configuration):
        written_tape = configuration.tape.write(self.write_character)

        if self.direction == 'left':
            return written_tape.move_head_left
        elif self.direction == 'right':
            return written_tape.move_head_right


class DTMRulebook(object):
    def __init__(self, rules):
        self.rules = rules

    def next_configuration(self, configuration):
        return self.rule_for(configuration).follow(configuration)

    def rule_for(self, configuration):
        for rule in self.rules:
            if rule.applies_to(configuration):
                return rule

    def applies_to(self, configuration):
        return self.rule_for(configuration) != None


class DTM(object):
    def __init__(self, current_configuration, accept_states, rulebook):
        self.current_configuration = current_configuration
        self.accept_states = accept_states
        self.rulebook = rulebook

    @property
    def accepting(self):
        return self.current_configuration.state in self.accept_states

    @property
    def step(self):
        self.current_configuration = self.rulebook.next_configuration(self.current_configuration)

    @property
    def run(self):
        while True:
            self.step
            if self.accepting or self.if_stuck:
                break

    @property
    def if_stuck(self):
        return not self.accepting and not self.rulebook.applies_to(self.current_configuration)


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

    def test_follow(self):
        rule = TMRule(1, '0', 2, '1', 'right')
        self.assertEqual(str(rule.follow(TMConfiguration(1, Tape([], '0', [], '_')))),
                         '#<struct TMConfiguration state=2, tape=#<Tape 1(_)>>')

    def test_Rulebook(self):
        tape = Tape(['1', '0', '1'], '1', [], '_')
        rulebook = DTMRulebook([
            TMRule(1, '0', 2, '1', 'right'),
            TMRule(1, '1', 1, '0', 'left'),
            TMRule(1, '_', 2, '1', 'right'),
            TMRule(2, '0', 2, '0', 'right'),
            TMRule(2, '1', 2, '1', 'right'),
            TMRule(2, '_', 3, '_', 'left')
        ])
        configuration = TMConfiguration(1, tape)
        self.assertEqual(str(configuration), '#<struct TMConfiguration state=1, tape=#<Tape 101(1)>>')
        configuration = rulebook.next_configuration(configuration)
        self.assertEqual(str(configuration), '#<struct TMConfiguration state=1, tape=#<Tape 10(1)0>>')
        configuration = rulebook.next_configuration(configuration)
        self.assertEqual(str(configuration), '#<struct TMConfiguration state=1, tape=#<Tape 1(0)00>>')
        configuration = rulebook.next_configuration(configuration)
        self.assertEqual(str(configuration), '#<struct TMConfiguration state=2, tape=#<Tape 11(0)0>>')

    def testDTM(self):
        tape = Tape(['1', '0', '1'], '1', [], '_')
        rulebook = DTMRulebook([
            TMRule(1, '0', 2, '1', 'right'),
            TMRule(1, '1', 1, '0', 'left'),
            TMRule(1, '_', 2, '1', 'right'),
            TMRule(2, '0', 2, '0', 'right'),
            TMRule(2, '1', 2, '1', 'right'),
            TMRule(2, '_', 3, '_', 'left')
        ])        
        dtm = DTM(TMConfiguration(1, tape), [3], rulebook)
        self.assertEqual(str(dtm.current_configuration), '#<struct TMConfiguration state=1, tape=#<Tape 101(1)>>')
        self.assertEqual(dtm.accepting, False)
        dtm.step
        self.assertEqual(str(dtm.current_configuration), '#<struct TMConfiguration state=1, tape=#<Tape 10(1)0>>')
        self.assertEqual(dtm.accepting, False)
        dtm.run
        self.assertEqual(str(dtm.current_configuration), '#<struct TMConfiguration state=3, tape=#<Tape 110(0)_>>')
        self.assertEqual(dtm.accepting, True)
        
    def testStuck(self):
        tape = Tape(['1', '2', '1'], '1', [], '_')
        rulebook = DTMRulebook([
            TMRule(1, '0', 2, '1', 'right'),
            TMRule(1, '1', 1, '0', 'left'),
            TMRule(1, '_', 2, '1', 'right'),
            TMRule(2, '0', 2, '0', 'right'),
            TMRule(2, '1', 2, '1', 'right'),
            TMRule(2, '_', 3, '_', 'left')
        ])
        dtm = DTM(TMConfiguration(1, tape), [3], rulebook)
        dtm.run
        self.assertEqual(str(dtm.current_configuration), '#<struct TMConfiguration state=1, tape=#<Tape 1(2)00>>')
        self.assertEqual(dtm.accepting, False)
        self.assertEqual(dtm.if_stuck, True)


if __name__ == '__main__':
    unittest.main()
