##NFA Simulation
##3.4 等价性
##python 3.4.1

from pprint import pprint
##NFA
class FARule(object):
    def __init__(self, state, character, next_state):
        self.state = state
        self.character = character
        self.next_state = next_state

    def applies_to(self, state, character):
        return self.state == state and self.character == character

    def follow(self):
        return self.next_state

    def __str__(self):
        state = self.state
        character = self.character
        next_state = self.next_state
        return '<FARule #<Set: {state}> --{character}--> #<Set: {next_state}>>'.format(**locals())

    __repr__ = __str__


class DFARulebook(object):
    def __init__(self, rules):
        self.rules = rules

    def next_state(self, state, character):
        return self.rule_for(state, character).follow()

    def rule_for(self, state, character):
        for rule in self.rules:
            if rule.applies_to(state, character):
                return rule


class DFA(object):
    def __init__(self, current_state, accept_states, rulebook):
        self.current_state = current_state
        self.accept_states = accept_states
        self.rulebook = rulebook

    def accepting(self):
        return self.current_state in self.accept_states

    def read_character(self, character):
        self.current_state = self.rulebook.next_state(self.current_state, character)

    def read_string(self, string):
        for character in string:
            self.read_character(character)


class DFADesign(object):
    def __init__(self, start_state, accept_states, rulebook):
        self.start_state = start_state
        self.accept_states = accept_states
        self.rulebook = rulebook

    def to_dfa(self):
        return DFA(self.start_state, self.accept_states, self.rulebook)

    def accepts(self, string):
        dfa = self.to_dfa()
        dfa.read_string(string)
        return dfa.accepting()


class NFARulebook(object):
    def __init__(self, rules):
        self.rules = rules

    def next_states(self, states, character):
        nexts = []
        for state in states:
            nexts += self.follow_rules_for(state, character) 
        return set(nexts)

    def follow_rules_for(self, state, character):
        return [rule.follow() for rule in self.rules_for(state, character)]

    def rules_for(self, state, character):
        return [rule for rule in self.rules if rule.applies_to(state, character)]

    def follow_free_moves(self, states):
        more_states = self.next_states(states, None)
        if more_states.issubset(states):
            return states
        else:
            return self.follow_free_moves(states.union(more_states))

    def alphabet(self):
        return(list(set([rule.character for rule in self.rules if  not rule.character == None])))


class NFA(object):
    def __init__(self, current_states, accept_states, rulebook):
        self._current_states = current_states
        self.accept_states = accept_states
        self.rulebook = rulebook

    @property
    def current_states(self):
        return self.rulebook.follow_free_moves(self._current_states)
    
    def accepting(self):
        if [state for state in self.current_states if state in self.accept_states]:
            return True
        else:
            return False

    def read_character(self, character):
        '''读取一个字符，获取通过自由移动能到达的所有状态集合，再计算出包含所有下一个状态的集合
        '''
        self._current_states = self.rulebook.next_states(self.current_states, character)

    def read_string(self, string):
        for character in string:
            self.read_character(character)


class NFADesign(object):
    def __init__(self, start_state, accept_states, rulebook):
        self.start_state = start_state
        self.accept_states = accept_states
        self.rulebook = rulebook

    def to_nfa(self, current_states = None):
        if current_states == None:
            current_states = set([self.start_state])
        return NFA(current_states, self.accept_states, self.rulebook)

    def accepts(self, string):
        nfa = self.to_nfa()
        nfa.read_string(string)
        return nfa.accepting()


class NFASimulation(object):
    def __init__(self, nfa_design):
        self.nfa_design = nfa_design

    def next_state(self, state, character):
        nfa = self.nfa_design.to_nfa(state)
        nfa.read_character(character)
        return nfa.current_states

    def rules_for(self, state):
        return [FARule(state, character, self.next_state(state, character))
                for character in self.nfa_design.rulebook.alphabet()]

    def discover_states_and_rules(self, states):
        rules = []
        for state in states:
            rules += self.rules_for(state)  
        more_states = [rule.follow() for rule in rules]

        temp = []
        for s in more_states:
            if s not in states:
                temp += [s]
        
        if temp:        
            return self.discover_states_and_rules(states + temp)
        else:
            return [states, rules]

    def to_dfa_design(self):
        start_state = self.nfa_design.to_nfa().current_states
        states, rules = self.discover_states_and_rules([set(start_state)])
        accept_states = [state for state in states if self.nfa_design.to_nfa(state).accepting()]

        return DFADesign(start_state, accept_states, DFARulebook(rules))


##test
rulebook = NFARulebook([
                    FARule(1, 'a', 1), FARule(1, 'a', 2), FARule(1, None, 2),
                    FARule(2, 'b', 3),
                    FARule(3, 'b', 1), FARule(3, None, 2)
                ])

nfa_design = NFADesign(1, [3], rulebook)
print(nfa_design.to_nfa().current_states)
print(nfa_design.to_nfa(set([2])).current_states)
print(nfa_design.to_nfa(set([3])).current_states)

print('')
nfa = nfa_design.to_nfa(set([2, 3]))
nfa.read_character('b')
print(nfa.current_states)

print('')
simulation = NFASimulation(nfa_design)
print(simulation.next_state(set([1, 2]), 'a'))
print(simulation.next_state(set([1, 2]), 'b'))
print(simulation.next_state(set([3, 2]), 'b'))
print(simulation.next_state(set([1, 3, 2]), 'b'))
print(simulation.next_state(set([1, 3, 2]), 'a'))

print('')
print(rulebook.alphabet())
pprint(simulation.rules_for(set([1, 2])))

print('')
pprint(simulation.rules_for(set([3, 2])))

print('')
start_state = nfa_design.to_nfa().current_states
print(start_state)
pprint(simulation.discover_states_and_rules([start_state]))

print('')
dfa_design = simulation.to_dfa_design()
print(dfa_design.accepts('aaa'))
print(dfa_design.accepts('aab'))
print(dfa_design.accepts('bbbabb'))
