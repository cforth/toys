#!usr/bin/env python3
## Stack & Queue

## Stack Class
class Stack(object):
    def __init__(self, stack=None):
        if stack == None:
            self._stack = []
        else:
            self._stack = stack

    def push(self, item):
        self._stack.append(item)

    def pop(self):
        return self._stack.pop()

    def is_empty(self):
        if self.size() > 0:
            return False
        else:
            return True

    def size(self):
        return len(self._stack)


## Queue Class
class Queue(object):
    def __init__(self, queue=None):
        if queue == None:
            self._queue = []
        else:
            self._queue = queue

    def enqueue(self, item):
        self._queue.append(item)

    def dequeue(self):
        return self._queue.pop(0)

    def is_empty(self):
        if self.size() > 0:
            return False
        else:
            return True

    def size(self):
        return len(self._queue)


## test
def main():
    operation = Stack()
    values = Stack()
    char_array = input()           ## '(1+((2+3)*(4*5)))'

    for s in char_array:
        if s == '(':
            pass
        elif s == '+' or s == '*':
            operation.push(s)
        elif s == ')':
            op = operation.pop()
            if op == '+':
                values.push(values.pop() + values.pop())
            elif op == '*':
                values.push(values.pop() * values.pop())
        else:
            values.push(int(s))

    print(values.pop())

