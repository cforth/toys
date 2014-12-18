## Virtual Machine 2.3.1
## 小步语义 -- 表达式
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


class Machine(object):
    """ 虚拟机
    """
    def __init__(self, expression, environment):
        self.expression = expression
        self.environment = environment

    def step(self):
        self.expression = self.expression.reduce(self.environment)

    def run(self):
        while self.expression.reducible():
            print(self.expression.to_s())
            self.step()
        print(self.expression.value)
            

## test
## 在虚拟机中运行表达式

##1 * 2 + 3 * 4 = 14
Machine(Add(Multiply(Number(1), Number(2)),
            Multiply(Number(3), Number(4))),
        {}
        ).run()

print('')

##5 < 2 + 2
Machine(
    LessThan(Number(5), Add(Number(2), Number(2))),
    {}
    ).run()

print('')


##x = 3; y = 4; x + y = 7
Machine(
    Add(Variable('x'), Variable('y')),
    {'x':Number(3), 'y':Number(4)}
    ).run()

