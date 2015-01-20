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
        return '#<Stack ({top}){underside}>'.format(**locals())

    __repr__ = __str__


class PDAConfiguration(object):
    """ Used to store the PDA configuration (a state and a stack)
    """
    STUCK_STATE = object()
    
    def __init__(self, state, stack):
        self.state = state
        self.stack = stack

    @property
    def stuck(self):
        return PDAConfiguration(self.__class__.STUCK_STATE, self.stack)

    @property
    def if_stuck(self):
        return self.state == self.__class__.STUCK_STATE

    def __str__(self):
        state = self.state
        stack = repr(self.stack)
        return '#<struct PDAConfiguration state={state}, stack={stack}>'.format(**locals())

    __repr__ = __str__


class PDARule(object):
    """ Used to express a rule, in a rule book of PDA
    """
    def __init__(self, state, character, next_state, pop_character, push_characters):
        self.state = state
        self.character = character
        self.next_state = next_state
        self.pop_character = pop_character
        self.push_characters = push_characters

    def applies_to(self, configuration, character):
        return self.state == configuration.state and \
                self.pop_character == configuration.stack.top and \
                self.character == character

    def follow(self, configuration):
        return PDAConfiguration(self.next_state, self.next_stack(configuration))

    def next_stack(self, configuration):
        popped_stack = configuration.stack.pop
        for item in self.push_characters[::-1]:
            popped_stack = popped_stack.push(item)
        return popped_stack

    def __str__(self):
        s = repr(self.state)
        char = repr(self.character)
        nexts = repr(self.next_state)
        pop_char = repr(self.pop_character)
        push_chars = repr(self.push_characters)
        
        return '#<struct PDARule\n\
        state={s},\n\
        character={char},\n\
        next_state={nexts},\n\
        pop_character={pop_char},\n\
        push_characters={push_chars}'.format(**locals())

    __repr__ = __str__


class DPDARulebook(object):
    """ The realization of DPDA-Rule-Book
    """
    def __init__(self, rules):
        self.rules = rules

    def next_configuration(self, configuration, character):
        return self.rule_for(configuration, character).follow(configuration)

    def rule_for(self, configuration, character):
        for rule in self.rules:
            if rule.applies_to(configuration, character):
                return rule
        return None

    def applies_to(self, configuration, character):
        return self.rule_for(configuration, character) != None

    def follow_free_moves(self, configuration):
        if self.applies_to(configuration, None):
            return self.follow_free_moves(self.next_configuration(configuration, None))
        else:
            return configuration


class DPDA(object):
    """ Use the rule book to construct a DPDA object.
        It will be reads characters from the input,
        tracking machine's current configuration at the same time. 
    """
    def __init__(self, current_configuration, accept_states, rulebook):
        self._current_configuration = current_configuration
        self.accept_states = accept_states
        self.rulebook = rulebook

    @property
    def current_configuration(self):
        return self.rulebook.follow_free_moves(self._current_configuration)

    @property
    def accepting(self):
        if self.current_configuration.state in self.accept_states:
            return True
        else:
            return False

    def next_configuration(self, character):
        if self.rulebook.applies_to(self.current_configuration, character):
            return self.rulebook.next_configuration(self.current_configuration, character)
        else:
            return self.current_configuration.stuck
        
    @property
    def if_stuck(self):
        return self.current_configuration.if_stuck

    def read_character(self, character):
        self._current_configuration = self.next_configuration(character)

    def read_string(self, string):
        for char in string:
            if not self.if_stuck:
                self.read_character(char)


class DPDADesign(object):
    """ DPDA package into the DPDADesign
    """
    def __init__(self, start_state, bottom_character, accept_states, rulebook):
        self.start_state = start_state
        self.bottom_character = bottom_character
        self.accept_states = accept_states
        self.rulebook = rulebook

    def accepts(self, string):
        dpda = self.to_dpda
        dpda.read_string(string)
        return dpda.accepting

    @property
    def to_dpda(self):
        start_stack = Stack([self.bottom_character])
        start_configuration = PDAConfiguration(self.start_state, start_stack)
        return DPDA(start_configuration, self.accept_states, self.rulebook)


## UnitTest
import unittest

class TestDPDA(unittest.TestCase):
    """ Tests of the books's code
    """
        
    def test_Stack(self):
        stack = Stack(['a','b','c','d','e'])
        self.assertEqual(str(stack), '#<Stack (a)bcde>')
        self.assertEqual(stack.pop.pop.top, 'c')
        self.assertEqual(stack.push('x').push('y').top, 'y')
        self.assertEqual(stack.push('x').push('y').pop.top, 'x')

    def test_PDARule(self):
        rule = PDARule(1, '(', 2, '$', ['b', '$'])
        configuration = PDAConfiguration(1, Stack(['$']))
        print(rule, end = '\n\n')
        self.assertEqual(str(configuration), '#<struct PDAConfiguration state=1, stack=#<Stack ($)>>')
        self.assertEqual(rule.applies_to(configuration, '('), True)

        self.assertEqual(str(rule.follow(configuration)), '#<struct PDAConfiguration state=2, stack=#<Stack (b)$>>')

    def test_DPDARulebook(self):
        rulebook = DPDARulebook([
            PDARule(1, '(', 2, '$', ['b', '$']),
            PDARule(2, '(', 2, 'b', ['b', 'b']),
            PDARule(2, ')', 2, 'b', []),
            PDARule(2, None, 1, '$', ['$'])
        ])
        configuration = PDAConfiguration(1, Stack(['$']))
        configuration = rulebook.next_configuration(configuration, '(')
        self.assertEqual(str(configuration), '#<struct PDAConfiguration state=2, stack=#<Stack (b)$>>')
        configuration = rulebook.next_configuration(configuration, '(')
        self.assertEqual(str(configuration), '#<struct PDAConfiguration state=2, stack=#<Stack (b)b$>>')
        configuration = rulebook.next_configuration(configuration, ')')
        self.assertEqual(str(configuration), '#<struct PDAConfiguration state=2, stack=#<Stack (b)$>>')

    def test_DPDA(self):
        rulebook = DPDARulebook([
            PDARule(1, '(', 2, '$', ['b', '$']),
            PDARule(2, '(', 2, 'b', ['b', 'b']),
            PDARule(2, ')', 2, 'b', []),
            PDARule(2, None, 1, '$', ['$'])
        ])
        dpda = DPDA(PDAConfiguration(1, Stack(['$'])), [1], rulebook)
        self.assertEqual(dpda.accepting, True)
        dpda.read_string('(()')
        self.assertEqual(dpda.accepting, False)
        self.assertEqual(str(dpda.current_configuration), '#<struct PDAConfiguration state=2, stack=#<Stack (b)$>>')

    def test_follow_free_moves(self):
        rulebook = DPDARulebook([
            PDARule(1, '(', 2, '$', ['b', '$']),
            PDARule(2, '(', 2, 'b', ['b', 'b']),
            PDARule(2, ')', 2, 'b', []),
            PDARule(2, None, 1, '$', ['$'])
        ])
        configuration = PDAConfiguration(2, Stack(['$']))
        self.assertEqual(str(configuration), '#<struct PDAConfiguration state=2, stack=#<Stack ($)>>')
        self.assertEqual(str(rulebook.follow_free_moves(configuration)), '#<struct PDAConfiguration state=1, stack=#<Stack ($)>>')

    def test_DPDA_follow_free_moves(self):
        rulebook = DPDARulebook([
            PDARule(1, '(', 2, '$', ['b', '$']),
            PDARule(2, '(', 2, 'b', ['b', 'b']),
            PDARule(2, ')', 2, 'b', []),
            PDARule(2, None, 1, '$', ['$'])
        ])
        dpda = DPDA(PDAConfiguration(1, Stack(['$'])), [1], rulebook)
        dpda.read_string('(()(')
        self.assertEqual(dpda.accepting, False)
        self.assertEqual(str(dpda.current_configuration), '#<struct PDAConfiguration state=2, stack=#<Stack (b)b$>>')
        dpda.read_string('))()')
        self.assertEqual(dpda.accepting, True)
        self.assertEqual(str(dpda.current_configuration), '#<struct PDAConfiguration state=1, stack=#<Stack ($)>>')

    def test_DPDADesign(self):
        rulebook = DPDARulebook([
            PDARule(1, '(', 2, '$', ['b', '$']),
            PDARule(2, '(', 2, 'b', ['b', 'b']),
            PDARule(2, ')', 2, 'b', []),
            PDARule(2, None, 1, '$', ['$'])
        ])
        dpda_design = DPDADesign(1, '$', [1], rulebook)
        self.assertEqual(dpda_design.accepts('(((((((((())))))))))'), True)
        self.assertEqual(dpda_design.accepts('()(())((()))(()(()))'), True)
        self.assertEqual(dpda_design.accepts('(()(()(()()(()()))()'), False)

    def test_DPDA_stuck(self):
       rulebook = DPDARulebook([
            PDARule(1, '(', 2, '$', ['b', '$']),
            PDARule(2, '(', 2, 'b', ['b', 'b']),
            PDARule(2, ')', 2, 'b', []),
            PDARule(2, None, 1, '$', ['$'])
        ])
       dpda = DPDA(PDAConfiguration(1, Stack(['$'])), [1], rulebook)
       dpda_design = DPDADesign(1, '$', [1], rulebook)
       dpda.read_string('())')
       self.assertEqual(dpda.accepting, False)
       self.assertEqual(dpda.if_stuck, True)
       self.assertEqual(dpda_design.accepts('())'), False)


if __name__ == '__main__':
    unittest.main()
