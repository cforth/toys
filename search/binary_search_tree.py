#!usr/bin/env python3
## 二叉查找树
import random

class Node(object):
    def __init__(self, key, value, number, left=None, right=None):
        self.key = key
        self.value = value
        self.number = number
        self.left = left
        self.right = right


def get(key, node):
    result = None
    while node != None:
        if key > node.key:
            node = node.right
        elif key < node.key:
            node = node.left
        else:
            result = node.value
            break
    return result


def put(key, value, node):
    if node == None:
        return Node(key, value, 1)
    if key < node.key:
        node.left = put(key, value, node.left)
    elif key > node.key:
        node.right = put(key, value, node.right)
    else:
        node.value = value
    node.number = size(node.left) + size(node.right) + 1
    return node


def size(node):
    if node == None:
        return 0
    else:
        return node.number


## test
## 随机插入26个字母到二叉查找树
char_table = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
char_index = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25]
length = len(char_index)
num = random.randint(0, length-1)
index = char_index[num]
root = Node(char_index[num], char_table[index], 1)
char_index.pop(num)
length -= 1

for i in range(25):
    num = random.randint(0, length-1)
    index = char_index[num]
    put(char_index[num], char_table[index], root)
    print(char_index[num])
    char_index.pop(num)
    length -= 1
print(root.number)

## 使用深度优先遍历和广度优先遍历二叉树
def depth_first_search(root):
    stack = []
    stack.append(root)
    while len(stack) != 0 :
        node = stack[-1]
        print(node.value, end=' ')
        stack.pop()
        if node.right != None:
            stack.append(node.right)
        if node.left != None:
            stack.append(node.left)
    print('\n')

def breadth_first_search(root):
    quene = []
    quene.append(root)
    while len(quene) != 0 :
        node = quene[0]
        print(node.key, end=' ')
        quene.pop(0)
        if node.left != None:
            quene.append(node.left)
        if node.right != None:
            quene.append(node.right)
    print('\n')

depth_first_search(root)
breadth_first_search(root)
