#!/usr/bin/env python3.4

"""Grammar Analyzer"""

# "Understanding Computation: Impossible Code and the Meaning of Programs"
# Chapter 4.3.2 's Code. Use Python3.
# Authors: Chai Fei

import re

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



class LexicalAnalyzer(object):
    """ 词法分析
        将代码字符串解析成符号列表
    """
    GRAMMAR = [
        { 'token': 'i', 'pattern': r'if' }, # if 关键字
        { 'token': 'e', 'pattern': r'else' }, # else 关键字
        { 'token': 'w', 'pattern': r'while' }, # while 关键字
        { 'token': 'd', 'pattern': r'do-nothing' }, # do-nothing 关键字
        { 'token': '(', 'pattern': r'\(' }, # 左小括号
        { 'token': ')', 'pattern': r'\)' }, # 右小括号
        { 'token': '{', 'pattern': r'\{' }, # 左大括号
        { 'token': '}', 'pattern': r'\}' }, # 右大括号
        { 'token': ';', 'pattern': r';' }, # 分号
        { 'token': '=', 'pattern': r'=' }, # 等号
        { 'token': '+', 'pattern': r'\+' }, # 加号
        { 'token': '*', 'pattern': r'\*' }, # 乘号
        { 'token': '<', 'pattern': r'\<' }, # 小于号
        { 'token': 'n', 'pattern': r'[0-9]+' }, # 数字
        { 'token': 'b', 'pattern': r'true|false' }, # 布尔值
        { 'token': 'v', 'pattern': r'[a-z]+' } # 变量名
    ]
    
    def __init__(self, string):
        self.string = string

    @property
    def analyze(self):
        tokens = []
        while self.more_tokens:
           tokens.append(self.next_token)
        return tokens

    @property
    def more_tokens(self):
        if self.string != '':
            return True
        else:
            return False

    @property
    def next_token(self):
        rule, match = self.rule_matching(self.string)
        self.string = self.string_after(match)
        return rule['token']

    def rule_matching(self, string):
        grammar = self.__class__.GRAMMAR
        matches = [self.match_at_beginning(rule['pattern'], string) for rule in grammar]
        rules_with_matches = [[rule, match] for rule, match in zip(grammar, matches) if match != None]
        return self.rule_with_longest_match(rules_with_matches)

    def match_at_beginning(self, pattern, string):
        result = re.match(pattern, string)
        if result == None:
            return None
        else:
            return result.group(0)

    def rule_with_longest_match(self, rules_with_matches):
        return max(rules_with_matches, key = lambda value: len(value[1]))

    def string_after(self, match):
        index = self.string.find(match) + len(match)
        return self.string[index:].strip()

    
## 语法分析
start_rule = PDARule(1, None, 2, '$', ['S', '$'])
symbol_rules = [
    # <statement> ::= <while> | <assign>
    PDARule(2, None, 2, 'S', ['W']),
    PDARule(2, None, 2, 'S', ['A']),

    # <while> ::= 'w' '(' <expression> ')' '{' <statement> '}'
    PDARule(2, None, 2, 'W', ['w', '(', 'E', ')', '{', 'S', '}']),

    # <assign> ::= 'v' '=' <expression>
    PDARule(2, None, 2, 'A', ['v', '=', 'E']),

    # <expression> ::= <less-than>
    PDARule(2, None, 2, 'E', ['L']),

    # <less-than> ::= <multiply> '<' <less-than> | <multiply>
    PDARule(2, None, 2, 'L', ['M', '<', 'L']),
    PDARule(2, None, 2, 'L', ['M']),

    # <multiply> ::= <term> '*' <multiply> | <term>
    PDARule(2, None, 2, 'M', ['T', '*', 'M']),
    PDARule(2, None, 2, 'M', ['T']),

    # <term> ::= 'n' | 'v'
    PDARule(2, None, 2, 'T', ['n']),
    PDARule(2, None, 2, 'T', ['v'])
]

token_rules = [PDARule(2, rule['token'], 2, rule['token'], []) for rule in LexicalAnalyzer.GRAMMAR]

stop_rule = PDARule(2, None, 3, '$', ['$'])

rulebook = NPDARulebook([start_rule, stop_rule] + symbol_rules + token_rules)

npda_design = NPDADesign(1, '$', [3], rulebook)

token_string = ''.join(LexicalAnalyzer('while (x < 5) { x = x * 3 }').analyze)

print('while (x < 5) { x = x * 3 }')
print(token_string)

print(npda_design.accepts(token_string))

print(npda_design.accepts(''.join(LexicalAnalyzer('while (x < 5 x = x * }').analyze)))
