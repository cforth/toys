##Nondeterministic Finite Automata，NFA
##3.2 非确定性有限自动机
##python 3.4.1

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

    def to_nfa(self):
        return NFA(set([self.start_state]), self.accept_states, self.rulebook)

    def accepts(self, string):
        nfa = self.to_nfa()
        nfa.read_string(string)
        return nfa.accepting()

      
##NFA
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

##自由移动
rulebook2 = NFARulebook([
     FARule(1, None, 2), FARule(1, None, 4),
     FARule(2, 'a', 3),
     FARule(3, 'a', 2),
     FARule(4, 'a', 5),
     FARule(5, 'a', 6),
     FARule(6, 'a', 4),
     ])

print(rulebook2.next_states(set([1]), None))
print(rulebook2.follow_free_moves(set([1])))

nfa_design2 = NFADesign(1,[2, 4], rulebook2)

print(nfa_design2.accepts('aa'))
print(nfa_design2.accepts('aaa'))
print(nfa_design2.accepts('aaaaa'))
print(nfa_design2.accepts('aaaaaa'))
