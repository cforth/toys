## Virtual Machine
## python 3.4

class Number(object):
    def __init__(self, value):
        self.value = value

    def reducible(self):
        return False

    def to_s(self):
        return str(self.value)


class Add(object):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def reducible(self):
        return True

    def reduce(self):
        if self.left.reducible():
            return Add(self.left.reduce(), self.right)
        elif self.right.reducible():
            return Add(self.left, self.right.reduce())
        else:
            return Number(self.left.value + self.right.value)

    def to_s(self):
        return self.left.to_s() + ' + ' + self.right.to_s()
    

class Multiply(object):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def reducible(self):
        return True

    def reduce(self):
        if self.left.reducible():
            return Add(self.left.reduce(), self.right)
        elif self.right.reducible():
            return Add(self.left, self.right.reduce())
        else:
            return Number(self.left.value * self.right.value)
        
    def to_s(self):
        return self.left.to_s() + ' * ' + self.right.to_s()

class Machine(object):
    def __init__(self, expression):
        self.expression = expression

    def step(self):
        self.expression = self.expression.reduce()

    def run(self):
        while self.expression.reducible():
            print(self.expression.to_s())
            self.step()
        print(self.expression.value)
            
            


##test
Machine(Add(Multiply(Number(1), Number(2)),
            Multiply(Number(3), Number(4)))
        ).run()

