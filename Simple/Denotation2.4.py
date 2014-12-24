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
        return 'eval(' + repr(self.left.to_python()) + ') + eval(' + repr(self.right.to_python()) + ')'   


class Multiply(object):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def to_python(self):
        return 'eval(' + repr(self.left.to_python()) + ') * eval(' + repr(self.right.to_python()) + ')'   


class LessThan(object):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def to_python(self):
        return 'eval(' + repr(self.left.to_python()) + ') < eval(' + repr(self.right.to_python()) + ')'    


class Assign(object):
    def __init__(self, name, expression):
        self.name = name
        self.expression = expression

    def to_python(self):
        return self.name + ' = ' + self.expression.to_python()


class DoNothing(object):
    def to_python(self):
        return ''


class If(object):
    def __init__(self, condition, consequence, alternative):
        self.condition = condition
        self.consequence = consequence
        self.alternative = alternative

    def to_python(self):
        return 'if ' + self.condition.to_python() + ' :\n    ' + self.consequence.to_python() + '\nelse:\n    ' + self.alternative.to_python()


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
proc = Assign('y', Number(5)).to_python()
print(proc)
##python的解释器中执行语句的函数是exec()
exec(proc, environment)
##print(environment, end = '\n\n')
##经过exec()后的environment字典，为了方便演示，下面的语句不显示内建的__builtins__对象名称与属性
print(dict([(k, v) for k, v in environment.items() if not k == '__builtins__']), end = '\n\n')

##if语句
environment = {'x':3, 'y':5}
proc = If(LessThan(Variable('x'), Variable('y')), Assign('z', Number(1)), Assign('z', Number(0))).to_python()
print(proc)
exec(proc, environment)
##print(environment, end = '\n\n')
print(dict([(k, v) for k, v in environment.items() if not k == '__builtins__']), end = '\n\n')
