##Nondeterministic Finite Automata，NFA
##3.2 非确定性有限自动机
##python 3.4.1

from functools import reduce

class FARule(object):
    def __init__(self, state, character, next_state):
        self.state = state
        self.character = character
        self.next_state = next_state

    def applies_to(self, state, character):
        return self.state == state and self.character == character

    def follow(self):
        return self.next_state


class NFARulebook(object):
    def __init__(self, rules):
        self.rules = rules

    def next_states(self, states, character):
        return set(reduce(lambda x, y: x + y, map(lambda state: self.follow_rules_for(state, character), states)))

    def follow_rules_for(self, state, character):
        return [rule.follow() for rule in self.rules_for(state, character)]

    def rules_for(self, state, character):
        return [rule for rule in self.rules if rule.applies_to(state, character)]


class NFA(object):
    def __init__(self, current_states, accept_states, rulebook):
        self.current_states = current_states
        self.accept_states = accept_states
        self.rulebook = rulebook

    def accepting(self):
        if [state for state in self.current_states if state in self.accept_states]:
            return True
        else:
            return False

    def read_character(self, character):
        self.current_states = self.rulebook.next_states(self.current_states, character)

    def read_string(self, string):
        for character in string:
            self.read_character(character)


class NFADesign(object):
    def __init__(self, start_state, accept_states, rulebook):
        self.start_state = start_state
        self.accept_states = accept_states
        self.rulebook = rulebook    

    def to_nfa(self):
        return NFA(set([self.start_state]), self.accept_states, self.rulebook)

    def accepts(self, string):
        nfa = self.to_nfa()
        nfa.read_string(string)
        return nfa.accepting()

      
##test
rulebook = NFARulebook([
    FARule(1, 'a', 1), FARule(1, 'b', 1), FARule(1, 'b', 2),
    FARule(2, 'a', 3), FARule(2, 'b', 3),
    FARule(3, 'a', 4), FARule(3, 'b', 4)
    ])

print(rulebook.next_states(set([1]), 'a'))
print(rulebook.next_states(set([1, 2]), 'a'))
print(rulebook.next_states(set([1, 3]), 'b'))

nfa_design = NFADesign(1, [4], rulebook)

print(nfa_design.accepts('bab'))
print(nfa_design.accepts('bbbbbb'))
print(nfa_design.accepts('bbabb'))
