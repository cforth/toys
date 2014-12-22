## Evaluate 2.3.2
## 大步语义
## python 3.4

class Number(object):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)
        
    def evaluate(self, environment):
        return self


class Boolean(object):
    def __init__(self, value):
        self.value = value
        
    def __str__(self):
        return str(self.value)
    
    def evaluate(self, environment):
        return self


class Variable(object):
    def __init__(self,name):
        self.name = name
        
    def evaluate(self, environment):
        return environment[self.name]


class Add(object):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def evaluate(self, environment):
        return Number(self.left.evaluate(environment).value + self.right.evaluate(environment).value)


class Multiply(object):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def evaluate(self, environment):
        return Number(self.left.evaluate(environment).value * self.right.evaluate(environment).value)


class LessThan(object):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def evaluate(self, environment):
        return Boolean(self.left.evaluate(environment).value < self.right.evaluate(environment).value)


##test
print(Number(21).evaluate({}))

print(Boolean(True).evaluate({}))

print(Variable('x').evaluate({'x':1212}))

print(LessThan(
    Add(Variable('x'), Number(2)),
    Variable('y')
    ).evaluate({'x':Number(2), 'y':Number(5)}))
