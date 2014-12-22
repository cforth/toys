## Virtual Machine 2.3.1
## 小步语义  -- 表达式、语句、控制结构、语句序列
## python 3.4
class Number(object):
    """ 数值符号类
    """
    def __init__(self, value):
        self.value = value

    def reducible(self):
        return False

    def to_s(self):
        return str(self.value)


class Boolean(object):
    """ 布尔值符号类型
    """
    def __init__(self, value):
        self.value = value

    def reducible(self):
        return False

    def to_s(self):
        return str(self.value)



class Add(object):
    """ 加法符号类
    """
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def reducible(self):
        return True

    def reduce(self, environment):
        if self.left.reducible():
            return Add(self.left.reduce(environment), self.right)
        elif self.right.reducible():
            return Add(self.left, self.right.reduce(environment))
        else:
            return Number(self.left.value + self.right.value)

    def to_s(self):
        return self.left.to_s() + ' + ' + self.right.to_s()
    

class Multiply(object):
    """ 乘法符号类
    """
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def reducible(self):
        return True

    def reduce(self, environment):
        if self.left.reducible():
            return Multiply(self.left.reduce(environment), self.right)
        elif self.right.reducible():
            return Multiply(self.left, self.right.reduce(environment))
        else:
            return Number(self.left.value * self.right.value)
        
    def to_s(self):
        return self.left.to_s() + ' * ' + self.right.to_s()


class LessThan(object):
    """ 小于符号类
    """
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def reducible(self):
        return True

    def reduce(self, environment):
        if self.left.reducible():
            return LessThan(self.left.reduce(environment), self.right)
        elif self.right.reducible():
            return LessThan(self.left, self.right.reduce(environment))
        else:
            return Boolean(self.left.value < self.right.value)

    def to_s(self):
        return self.left.to_s() + ' < ' + self.right.to_s()


class Variable(object):
    """ 变量符号类
    """
    def __init__(self, name):
        self.name = name

    def reducible(self):
        return True

    def reduce(self, environment):
        return environment[self.name]

    def to_s(self):
        return str(self.name)
    

class DoNothing(object):
    """ 什么都不做
    """
    def to_s(self):
        return 'do-nothing'

    def __eq__(self, other_statement):
        return isinstance(other_statement, DoNothing)

    def reducible(self):
        return False


class Assign(object):
    """ 变量赋值语句的实现
    """
    def __init__(self, name, expression):
        self.name = name
        self.expression = expression

    def to_s(self):
        return '{name} = {exp}'.format(name=self.name, exp=self.expression.to_s())

    def reducible(self):
        return True

    def reduce(self, environment):
        if self.expression.reducible():
            return Assign(self.name, self.expression.reduce(environment)), environment
        else:
            return DoNothing(), dict(environment, **{self.name:self.expression})


class If(object):
    """ IF控制语句的实现
    """
    def __init__(self, condition, consequence, alternative):
        self.condition = condition
        self.consequence = consequence
        self.alternative = alternative

    def to_s(self):
        return 'if (%s) {%s} else {%s}' % (self.condition.to_s(), self.consequence.to_s(), self.alternative.to_s())

    def reducible(self):
        return True

    def reduce(self, environment):
        if self.condition.reducible():
            return If(self.condition.reduce(environment), self.consequence, self.alternative), environment
        else:
            if self.condition.value == Boolean(True).value:
                return self.consequence, environment
            elif self.condition.value == Boolean(False).value:
                return self.alternative, environment


class Sequence(object):
    """语句序列
    """
    def __init__(self, first, second):
        self.first = first
        self.second = second

    def to_s(self):
        return '{first}; {second}'.format(first=self.first.to_s(), second=self.second.to_s())

    def reducible(self):
        return True

    def reduce(self, environment):
        if self.first == DoNothing():
            return self.second, environment
        else:
            reduced_first, reduced_environment = self.first.reduce(environment)
            return Sequence(reduced_first, self.second), reduced_environment


class While(object):
    """ while循环语句实现
    """
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

    def to_s(self):
        return 'while (%s) {%s}' % (self.condition.to_s(), self.body.to_s())

    def reducible(self):
        return True

    def reduce(self, environment):
        return If(self.condition, Sequence(self.body, self), DoNothing()), environment


class Machine(object):
    """ 虚拟机
    """
    def __init__(self, statement, environment):
        self.statement = statement
        self.environment = environment

    def step(self):
        self.statement, self.environment = self.statement.reduce(self.environment)

    def run(self):
        while self.statement.reducible():
            print(self.statement.to_s(), end=', ')
            print(dict([(k, v.value) for k, v in self.environment.items()]))
            self.step()
        print(self.statement.to_s(), end=', ')
        print(dict([(k, v.value) for k, v in self.environment.items()]))


##test
##x = 2; x = x + 1; x = 3
Machine(
    Assign('x', Add(Variable('x'), Number(1))),
    {'x': Number(2)}
    ).run()

print('')

##x = True; if (x) {y = 1} else {y = 2}   
Machine(
    If(
        Variable('x'),
        Assign('y', Number(1)),
        Assign('y', Number(2))
        ),
    {'x':Boolean(True)}
    ).run()

print('')

##x = 1 + 1; y = x + 3
Machine(
    Sequence(
        Assign('x', Add(Number(1), Number(1))),
        Assign('y', Add(Variable('x'), Number(3)))
        ),
    {}
    ).run()

print('')

##while (x < 5) { x = x * 3 }
Machine(
    While(
        LessThan(Variable('x'), Number(5)),
        Assign('x', Multiply(Variable('x'), Number(3)))
        ),
    {'x':Number(1)}
    ).run()
