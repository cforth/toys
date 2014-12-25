##Denotation 2.4
##指称语义
##python 3.4.1

class Number(object):
    def __init__(self, value):
        self.value = value

    def to_python(self):
        return repr(self.value)


class Boolean(object):
    def __init__(self, value):
        self.value = value

    def to_python(self):
        return repr(self.value)


class Variable(object):
    def __init__(self, name):
        self.name = name

    def to_python(self):
        return self.name


class Add(object):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def to_python(self):
        left = repr(self.left.to_python())
        right = repr(self.right.to_python())
        return 'eval({left}, globals()) + eval({right}, globals())'.format(**locals())  


class Multiply(object):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def to_python(self):
        left = repr(self.left.to_python())
        right = repr(self.right.to_python())
        return 'eval({left}, globals()) * eval({right}, globals())'.format(**locals())  


class LessThan(object):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def to_python(self):
        left = repr(self.left.to_python())
        right = repr(self.right.to_python())
        return 'eval({left}, globals()) < eval({right}, globals())'.format(**locals())   


class Assign(object):
    def __init__(self, name, expression):
        self.name = name
        self.expression = expression

    def to_python(self):
        name = self.name
        expression = repr(self.expression.to_python())
        return '{name} = eval({expression}, globals())'.format(**locals())


class DoNothing(object):
    def to_python(self):
        return ''


class If(object):
    def __init__(self, condition, consequence, alternative):
        self.condition = condition
        self.consequence = consequence
        self.alternative = alternative

    def to_python(self):
        condition = self.condition.to_python()
        consequence = self.consequence.to_python()
        alternative = self.alternative.to_python()
        return 'if {condition} :\n    {consequence}\nelse:\n    {alternative}'.format(**locals())


class Sequence(object):
    def __init__(self, first, second):
        self.first = first
        self.second = second

    def to_python(self):
        first = self.first.to_python()
        second = self.second.to_python()
        return '{first}\n{second}'.format(**locals())


class While(object):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

    def to_python(self):
        condition = self.condition.to_python()
        body = self.body.to_python()
        return 'while {condition}:\n    {body}'.format(**locals())


##test

##数值表达式
proc = Number(5).to_python()
print(proc)
##python的解释器中执行表达式的函数是eval()
num = eval(proc,{})
print(num, end = '\n\n')

##布尔值表达式
proc = Boolean(True).to_python()
print(proc)
thing = eval(proc,{})
print(thing, end = '\n\n')                                                                                                       

##变量表达式
proc = Variable('x').to_python()
print(proc)
var = eval(proc,{'x':7})
print(var, end = '\n\n')

##环境
environment = {'x':3}
print(environment, end = '\n\n')

##加法表达式
proc = Add(Variable('x'), Number(1)).to_python()
print(proc)
result = eval(proc, environment)
print(result, end = '\n\n')

##乘法表达式
proc = Multiply(Variable('x'), Number(8)).to_python()
print(proc)
result = eval(proc, environment)
print(result, end = '\n\n')

##比较表达式
proc = LessThan(Variable('x'), Add(Multiply(Variable('x'), Number(8)), Number(3))).to_python()
print(proc)
result = eval(proc, environment)
print(result, end = '\n\n')

##赋值语句
environment = {'x':3}
statement = Assign('y', Number(5)).to_python()
print(statement)
##python的解释器中执行语句的函数是exec()
exec(statement, environment)
##print(environment, end = '\n\n')
##经过exec()后的environment字典，为了方便演示，下面的语句不显示内建的__builtins__对象名称与属性
print(dict([(k, v) for k, v in environment.items() if not k == '__builtins__']), end = '\n\n')

##if语句
environment = {'x':3, 'y':5}
statement = If(LessThan(Variable('x'), Variable('y')), Assign('z', Number(1)), Assign('z', Number(0))).to_python()
print(statement)
exec(statement, environment)
print(dict([(k, v) for k, v in environment.items() if not k == '__builtins__']), end = '\n\n')

##语句序列
environment = {'x':3, 'y':5, 'z':6}
statement = Sequence(Assign('x', Number(1)), Assign('y', Number(2))).to_python()
print(statement)
exec(statement , environment)
print(dict([(k, v) for k, v in environment.items() if not k == '__builtins__']), end = '\n\n')

#while语句
environment = {'x':1}
statement = While(
    LessThan(Variable('x'), Number(8)),
    Assign('x', Multiply(Variable('x'), Number(3)))
    ).to_python()
print(statement)
exec(statement , environment)
print(dict([(k, v) for k, v in environment.items() if not k == '__builtins__']), end = '\n\n')

