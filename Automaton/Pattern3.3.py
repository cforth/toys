##Regular Expression
##3.3 正则表达式
##python 3.4.1

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


##正则表达式
class Pattern(object):
    def bracket(self, outer_precedence):
        if self.precedence < outer_precedence:
            return '(' + self.to_s() + ')'
        else:
            return self.to_s()

    def __str__(self):
        return '/' + self.to_s() + '/'

    def matches(self, string):
        return self.to_nfa_design().accepts(string)


class Empty(Pattern):
    def __init__(self):
        self.character = None
        self.precedence = 3
        
    def to_s(self):
        return ''

    def to_nfa_design(self):
        start_state = object()
        accept_states = [start_state]
        rulebook = NFARulebook([])
        return NFADesign(start_state, accept_states, rulebook)


class Literal(Pattern):
    def __init__(self, character):
        self.character = character
        self.precedence = 3

    def to_s(self):
        return self.character

    def to_nfa_design(self):
        start_state = object()
        accept_state = object()
        rule = FARule(start_state, self.character, accept_state)
        rulebook = NFARulebook([rule])
        return NFADesign(start_state, [accept_state], rulebook)


class Concatenate(Pattern):
    def __init__(self, first, second):
        self.first = first
        self.second = second
        self.precedence = 1

    def to_s(self):
        return ''.join([pattern.bracket(self.precedence) for pattern in [self.first, self.second]])

    def to_nfa_design(self):
        first_nfa_design = self.first.to_nfa_design()
        second_nfa_design = self.second.to_nfa_design()

        start_state = first_nfa_design.start_state
        accept_states = second_nfa_design.accept_states
        rules = first_nfa_design.rulebook.rules + second_nfa_design.rulebook.rules
        extra_rules = [FARule(state, None, second_nfa_design.start_state) for state in first_nfa_design.accept_states]
        rulebook = NFARulebook(rules + extra_rules)

        return NFADesign(start_state, accept_states, rulebook)


class Choose(Pattern):
    def __init__(self, first, second):
        self.first = first
        self.second = second
        self.precedence = 0

    def to_s(self):
        return '|'.join([pattern.bracket(self.precedence) for pattern in [self.first, self.second]])

    def to_nfa_design(self):
        first_nfa_design = self.first.to_nfa_design()
        second_nfa_design = self.second.to_nfa_design()

        start_state = object()
        accept_states = first_nfa_design.accept_states + second_nfa_design.accept_states

        rules = first_nfa_design.rulebook.rules + second_nfa_design.rulebook.rules
        extra_rules = [FARule(start_state, None, nfa_design.start_state) for nfa_design in [first_nfa_design, second_nfa_design]]

        rulebook = NFARulebook(rules + extra_rules)

        return NFADesign(start_state, accept_states, rulebook)


class Repeat(Pattern):
    def __init__(self, pattern):
        self.pattern = pattern
        self.precedence = 2

    def to_s(self):
        return self.pattern.bracket(self.precedence) + '*'

    def to_nfa_design(self):
        pattern_nfa_design = self.pattern.to_nfa_design()

        start_state = object()
        accept_states = pattern_nfa_design.accept_states + [start_state]
        rules = pattern_nfa_design.rulebook.rules
        extra_rules = [FARule(accept_state, None, pattern_nfa_design.start_state) for accept_state in pattern_nfa_design.accept_states] + [FARule(start_state, None, pattern_nfa_design.start_state)]
        rulebook = NFARulebook(rules + extra_rules)

        return NFADesign(start_state, accept_states, rulebook)


##test
##为每类正则表达式定义一个类，并使用这些类的实例表示任何正则表达式的抽象语法树
pattern = Repeat(
            Choose(
                Concatenate(Literal('a'), Literal('b')),
                Literal('a')
                )
            )

print(pattern)

print('')
nfa_design = Empty().to_nfa_design()
print(nfa_design.accepts(''))
print(nfa_design.accepts('a'))
nfa_design = Literal('a').to_nfa_design()
print(nfa_design.accepts(''))
print(nfa_design.accepts('a'))
print(nfa_design.accepts('b'))

print('')
print(Empty().matches('a'))
print(Literal('a').matches('a'))

print('')
pattern = Concatenate(Literal('a'), Literal('b'))
print(pattern)
print(pattern.matches('a'))
print(pattern.matches('ab'))
print(pattern.matches('abc'))

print('')
pattern = Concatenate(
         Literal('a'),
         Concatenate(Literal('b'), Literal('c'))
   )
print(pattern)
print(pattern.matches('a'))
print(pattern.matches('ab'))
print(pattern.matches('abc'))

print('')
pattern = Choose(Literal('a'),Literal('b'))
print(pattern)
print(pattern.matches('a'))
print(pattern.matches('b'))
print(pattern.matches('c'))

print('')
pattern = Repeat(Literal('a'))
print(pattern)
print(pattern.matches(''))
print(pattern.matches('a'))
print(pattern.matches('aaaa'))
print(pattern.matches('b'))

print('')
pattern = Repeat(
                Concatenate(
                    Literal('a'),
                    Choose(Empty(),Literal('b'))
                    )
                )
print(pattern)
print(pattern.matches(''))
print(pattern.matches('a'))
print(pattern.matches('ab'))
print(pattern.matches('aba'))
print(pattern.matches('abab'))
print(pattern.matches('abaab'))
print(pattern.matches('abba'))
