#!usr/bin/env python3
## 二叉查找树
import random
import os

class Node(object):
    """使用Node类模二叉树的节点
    """
    def __init__(self, key, value, number, left=None, right=None):
        self.key = key
        self.value = value
        self.number = number
        self.left = left
        self.right = right


def get(key, node):
    """查找二叉树中的key
    """
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
    """在二叉树中增加一个节点
    """
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
    """返回二叉树节点中的子节点（包含自己）数量
    """
    if node == None:
        return 0
    else:
        return node.number


def get_max(node):
    """返回二叉树中所有节点中最大的key
    """
    while node.right != None:
        node = node.right
    max_item = node.key
    return max_item


def get_min(node):
    """返回二叉树中所有节点中最小的key
    """
    while node.left != None:
        node = node.left
    min_item = node.key
    return min_item


def floor(key, node):
    """返回二叉树所有节点的key中，小于等于key参数的最大的节点
    """
    if node == None:
        return None
    if key == node.key:
        return node
    if key < node.key:
        return floor(key, node.left)
    else:
        right = floor(key, node.right)
        if right == None:
            return node
        else:
            return right


def floor_key(key, node):
    """返回二叉树所有节点的key中，小于等于key参数的最大的节点的key
    """
    floor_node = floor(key, node)
    if floor_node != None:
        return floor_node.key
    else:
        return None


def ceiling(key, node):
    """返回二叉树所有节点的key中，大于等于key参数的最小的节点
    """
    if node == None:
        return None
    if key == node.key:
        return node
    if key > node.key:
        return ceiling(key, node.right)
    else:
        left = ceiling(key, node.left)
        if left == None:
            return node
        else:
            return left


def ceiling_key(key, node):
    """返回二叉树所有节点的key中，大于等于key参数的最小的节点的key
    """
    ceiling_node = ceiling(key, node)
    if ceiling_node != None:
        return ceiling_node.key
    else:
        return None


def del_min(node):
    """删除二叉树中所有节点key最小的节点
    """
    if node.left == None:
        return node.right
    node.left = del_min(node.left)
    node.number = size(node.left) + size(node.right) + 1
    return node


def del_max(node):
    """删除二叉树中所有节点key最大的节点
    """
    if node.rigth == None:
        return node.left
    node.rigth = del_max(node.rigth)
    node.number = size(node.left) + size(node.right) + 1
    return node


def get_min_node(node):
    """返回二叉树中最小key的节点
    """
    if node.left == None:
        return node
    else:
        return get_min_node(node.left)


def delete(key, node):
    """删除二叉树中指定key的节点
    """
    if key > node.key:
        node.right = delete(key, node.right)
    elif key < node.key:
        node.left = delete(key, node.left)
    else:
        if node.left == None:
            return node.right
        elif node.right == None:
            return node.left
        else:
            t_left = node.left
            t_right = node.right
            node = get_min_node(t_right)
            node.right = del_min(t_right)
            node.left = t_left
    node.number = size(node.left) + size(node.right) + 1
    return node


def depth_first_search(root):
    """使用深度优先遍历二叉树
    """
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
    """使用广度优先遍历二叉树
    """
    quene = []
    quene.append(root)
    while len(quene) != 0 :
        node = quene[0]
        print(node.value, end = ' ')
        quene.pop(0)
        if node.left != None:
            quene.append(node.left)
        if node.right != None:
            quene.append(node.right)
    print('\n')


def print_tree(root):
    """未完成！打印出每个节点的value和左右子节点的value，为了下一步打印出树结构做准备
    """
    quene = []
    quene.append(root)
    while len(quene) != 0 :
        node = quene[0]
        if node.left == None:
            ll = '-'
        else:
            ll = node.left.value
        if node.right == None:
            rr = '-'
        else:
            rr = node.right.value
        print('  {n}  \n _|_ \n|   |\n{l}   {r}\n==========='.format(n = node.value, l = ll, r = rr))
        quene.pop(0)
        if node.left != None:
            quene.append(node.left)
        if node.right != None:
            quene.append(node.right)
    print('\n')


def print_tree_r(root):
    """生成符合打印tree结构图语法的字符串
    打印tree结构图的工具在/print_tree/tree.exe
    """
    if root != None:
        return '(' + root.value + print_tree_r(root.left) + print_tree_r(root.right) + ')'
    else:
        return '()'


########################################   
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
    char_index.pop(num)
    length -= 1
    
def test(root):
    print('All nodes number: %d' % root.number)
    print('Depth first search:')
    depth_first_search(root)
    print('Breadth first search:')
    breadth_first_search(root)

    print('Print Tree:')
    tree = '\\tree' + print_tree_r(root)
    print(tree + '\n')

    print('Max Key: %d' % get_max(root))
    print('Min Key: %d' % get_min(root))
    print('Floor key with 26: %d' % floor_key(26, root))
    print('Ceiling key with -1: %d' % ceiling_key(-1, root))

    print('Destroy Tree:')
    breadth_first_search(root)
    for i in range(26):
        root = delete(i, root)
        if root != None:
            breadth_first_search(root)
        else:
            print('Tree have been destroyed！')

## 打印树结构图，在终端上输入 python3 binary_search_tree.py | ../print_tree/tree.exe
if __name__ == '__main__':
    tree = '\\tree' + print_tree_r(root)
    print(tree)
