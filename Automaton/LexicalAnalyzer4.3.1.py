#!/usr/bin/env python3.4

"""Lexical Analyzer"""

# "Understanding Computation: Impossible Code and the Meaning of Programs"
# Chapter 4.3.1 's Code. Use Python3.
# Authors: Chai Fei

import re

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

    
##test
print('y = x * 7')
print(LexicalAnalyzer('y = x * 7').analyze)

print('\n')
print('while (x < 5) { x = x * 3 }')
print(LexicalAnalyzer('while (x < 5) { x = x * 3 }').analyze)

print('\n')
print('if (x < 10) { y = true; x = 0 } else { do-nothing }')
print(LexicalAnalyzer('if (x < 10) { y = true; x = 0 } else { do-nothing }').analyze)

print('\n')
print('x = false')
print(LexicalAnalyzer('x = false').analyze)

print('\n')
print('x = falsehood')
print(LexicalAnalyzer('x = falsehood').analyze)
