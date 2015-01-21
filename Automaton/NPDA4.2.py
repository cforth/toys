#!/usr/bin/env python3.4

"""Nondeterministic PushDown Automaton，NPDA"""

# "Understanding Computation: Impossible Code and the Meaning of Programs"
# Chapter 4.2 's Code. Use Python3.
# Authors: Chai Fei
from pprint import pprint

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


class NPDARulebook(object):
    """ The realization of NDPDA-Rule-Book
    """
    def __init__(self, rules):
        self.rules = rules

    def next_configurations(self, configurations, character):
        nexts = []
        for config in configurations:
            nexts += self.follow_rules_for(config, character)
        
        return set(nexts)

    def follow_rules_for(self, configuration, character):
        return [rule.follow(configuration) for rule in self.rules_for(configuration, character)]

    def rules_for(self, configuration, character):
        return [rule for rule in self.rules if rule.applies_to(configuration, character)]

    def follow_free_moves(self, configurations):
        more_configurations = self.next_configurations(configurations, None)

        ## 必须将configuration转为字符串后，才能比较互相是否相同
        not_in_configs = []
        for more in more_configurations:
            flag = False
            for config in configurations:
                if str(more) == str(config):
                    flag = True
            if not flag:
                not_in_configs += [more]

        if not not_in_configs:
            return configurations
        else:
            return self.follow_free_moves(configurations.union(set(not_in_configs)))


class NPDA(object):
    """ NPDA
    """
    def __init__(self, current_configurations, accept_states, rulebook):
        self._current_configurations = current_configurations
        self.accept_states = accept_states
        self.rulebook = rulebook

    @property
    def current_configurations(self):
        return self.rulebook.follow_free_moves(self._current_configurations)

    @property
    def accepting(self):
        if [config for config in self.current_configurations if config.state in self.accept_states]:
            return True
        else:
            return False

    def read_character(self, character):
        self._current_configurations = self.rulebook.next_configurations(self.current_configurations, character)

    def read_string(self, string):
        for character in string:
            self.read_character(character)


class NPDADesign(object):
    """ NPDA package into the NPDADesign
    """
    def __init__(self, start_state, bottom_character, accept_states, rulebook):
        self.start_state = start_state
        self.bottom_character = bottom_character
        self.accept_states = accept_states
        self.rulebook = rulebook

    def accepts(self, string):
        npda = self.to_npda
        npda.read_string(string)
        return npda.accepting

    @property
    def to_npda(self):
        start_stack = Stack([self.bottom_character])
        start_configuration = PDAConfiguration(self.start_state, start_stack)
        return NPDA(set([start_configuration]), self.accept_states, self.rulebook)


## UnitTest
import unittest

class TestNDPDA(unittest.TestCase):
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
        self.assertEqual(str(configuration), '#<struct PDAConfiguration state=1, stack=#<Stack ($)>>')
        self.assertEqual(rule.applies_to(configuration, '('), True)

        self.assertEqual(str(rule.follow(configuration)), '#<struct PDAConfiguration state=2, stack=#<Stack (b)$>>')

    def test_NPDA(self):
        rulebook = NPDARulebook([
            PDARule(1, 'a', 1, '$', ['a', '$']),
            PDARule(1, 'a', 1, 'a', ['a', 'a']),
            PDARule(1, 'a', 1, 'b', ['a', 'b']),
            PDARule(1, 'b', 1, '$', ['b', '$']),
            PDARule(1, 'b', 1, 'a', ['b', 'a']),
            PDARule(1, 'b', 1, 'b', ['b', 'b']),
            PDARule(1, None, 2, '$', ['$']),
            PDARule(1, None, 2, 'a', ['a']),
            PDARule(1, None, 2, 'b', ['b']),
            PDARule(2, 'a', 2, 'a', []),
            PDARule(2, 'b', 2, 'b', []),
            PDARule(2, None, 3, '$', ['$'])
        ])
        configuration = PDAConfiguration(1, Stack(['$']))
        self.assertEqual(str(configuration), '#<struct PDAConfiguration state=1, stack=#<Stack ($)>>')
        npda = NPDA(set([configuration]), [3], rulebook)
        self.assertEqual(npda.accepting, True)
        pprint(npda.current_configurations)

        npda.read_string('abb')
        self.assertEqual(npda.accepting, False)
        pprint(npda.current_configurations)

        npda.read_character('a')
        self.assertEqual(npda.accepting, True)
        pprint(npda.current_configurations)

    def test_NPDADesign(self):
        rulebook = NPDARulebook([
            PDARule(1, 'a', 1, '$', ['a', '$']),
            PDARule(1, 'a', 1, 'a', ['a', 'a']),
            PDARule(1, 'a', 1, 'b', ['a', 'b']),
            PDARule(1, 'b', 1, '$', ['b', '$']),
            PDARule(1, 'b', 1, 'a', ['b', 'a']),
            PDARule(1, 'b', 1, 'b', ['b', 'b']),
            PDARule(1, None, 2, '$', ['$']),
            PDARule(1, None, 2, 'a', ['a']),
            PDARule(1, None, 2, 'b', ['b']),
            PDARule(2, 'a', 2, 'a', []),
            PDARule(2, 'b', 2, 'b', []),
            PDARule(2, None, 3, '$', ['$'])
        ])
        npda_design = NPDADesign(1, '$', [3], rulebook)
        self.assertEqual(npda_design.accepts('abba'), True)
        self.assertEqual(npda_design.accepts('babbaabbab'), True)
        self.assertEqual(npda_design.accepts('abb'), False)
        self.assertEqual(npda_design.accepts('baabaa'), False)


if __name__ == '__main__':
    unittest.main()
