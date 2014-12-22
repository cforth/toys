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


class Assign(object):
    def __init__(self, name, expression):
        self.name = name
        self.expression = expression

    def evaluate(self, environment):
        return dict(environment, **{self.name:self.expression.evaluate(environment)} )


class DoNothing(object):
    def evaluate(self, environment):
        return environment


class If(object):
    def __init__(self, condition, consequence, alternative):
        self.condition = condition
        self.consequence = consequence
        self.alternative = alternative

    def evaluate(self, environment):
        if self.condition.evaluate(environment).value == Boolean(True).value:
            return self.consequence.evaluate(environment)
        elif self.condition.evaluate(environment).value == Boolean(False).value:
            return self.alternative.evaluate(environment)


class Sequence(object):
    def __init__(self, first, second):
        self.first = first
        self.second = second

    def evaluate(self, environment):
        return self.second.evaluate(self.first.evaluate(environment))


class While(object):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

    def evaluate(self, environment):
        if self.condition.evaluate(environment).value == Boolean(True).value:
            return self.evaluate(self.body.evaluate(environment))
        elif self.condition.evaluate(environment).value == Boolean(False).value:
            return environment


##test
print(Number(21).evaluate({}))

print(Boolean(True).evaluate({}))

print(Variable('x').evaluate({'x':1212}))

print(LessThan(
    Add(Variable('x'), Number(2)),
    Variable('y')
    ).evaluate({'x':Number(2), 'y':Number(5)}))


statement = Sequence(
    Assign('x', Add(Number(1), Number(1))),
    Assign('y', Add(Variable('x'), Number(3)))
    )
print(statement.evaluate({}))
print(dict([(k, v.value) for k,v in statement.evaluate({}).items()]))


statement = While(
    LessThan(Variable('x'), Number(5)),
    Assign('x', Multiply(Variable('x'), Number(3)))
    )

print(statement.evaluate({'x': Number(1)}))
print(dict([(k, v.value) for k,v in statement.evaluate({'x': Number(1)}).items()]))
