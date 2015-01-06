##Regular Expression
##3.3 正则表达式
##python 3.4.1

class Pattern(object):
    def bracket(self, outer_precedence):
        if self.precedence < outer_precedence:
            return '(' + self.to_s() + ')'
        else:
            return self.to_s()

    def __str__(self):
        return '/' + self.to_s() + '/'


class Empty(Pattern):
    def __init__(self):
        self.precedence = 3
        
    def to_s(self):
        return ''


class Literal(Pattern):
    def __init__(self, character):
        self.character = character
        self.precedence = 3

    def to_s(self):
        return self.character


class Concatenate(Pattern):
    def __init__(self, first, second):
        self.first = first
        self.second = second
        self.precedence = 1

    def to_s(self):
        return ''.join([pattern.bracket(self.precedence) for pattern in [self.first, self.second]])


class Choose(Pattern):
    def __init__(self, first, second):
        self.first = first
        self.second = second
        self.precedence = 0

    def to_s(self):
        return '|'.join([pattern.bracket(self.precedence) for pattern in [self.first, self.second]])


class Repeat(Pattern):
    def __init__(self, pattern):
        self.pattern = pattern
        self.precedence = 2

    def to_s(self):
        return self.pattern.bracket(self.precedence) + '*'


##test
##为每类正则表达式定义一个类，并使用这些类的实例表示任何正则表达式的抽象语法树
pattern = Repeat(
            Choose(
                Concatenate(Literal('a'), Literal('b')),
                Literal('a')
                )
            )

print(pattern)
