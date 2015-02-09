#!/usr/bin/env python3.4

"""Untyped Lambda Calculus"""

# "Understanding Computation: Impossible Code and the Meaning of Programs"
# Chapter 6.1 's Code. Use Python3.
# Authors: Chai Fei

# Python中没有类似Ruby的proc功能的函数，只能直接用lambda来实现

# 6.1.3 实现数字
ZERO = lambda p: lambda x: x
ONE = lambda p: lambda x: p(x)
TWO = lambda p: lambda x: p(p(x))
THREE = lambda p: lambda x: p(p(p(x)))
FIVE = lambda p: lambda x: p(p(p(p(p(x)))))
FIFTEEN = lambda p: lambda x: p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(x)))))))))))))))
# 一百层嵌套括号会导致Python解释器解析溢出错误，改用五十层
FIFTY = lambda p: lambda x: p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(x))))))))))))))))))))))))))))))))))))))))))))))))))
                                              
def to_integer(proc):
    return proc(lambda n: n + 1)(0)


# 6.1.4 实现布尔值
TRUE = lambda x: lambda y: x
FALSE = lambda x: lambda y: y

def to_boolean(proc):
    return proc(True)(False)


# 实现if语句
IF = lambda b: lambda x: lambda y: b(x)(y)

def to_boolean(proc):
    return IF(proc)(True)(False)


# if语句简化
IF = lambda b: b


# 6.1.5 实现谓词
IS_ZERO = lambda n: n(lambda x: FALSE)(TRUE)


# 6.1.6 有序对
PAIR = lambda x: lambda y: lambda f: f(x)(y)
LEFT = lambda p: p(lambda x: lambda y: x)
RIGHT = lambda p: p(lambda x: lambda y: y)


# 6.1.7 数值运算
INCREMENT = lambda n: lambda p: lambda x: p(n(p)(x))
SLIDE = lambda p: PAIR(RIGHT(p))(INCREMENT(RIGHT(p)))
DECREMENT = lambda n :LEFT(n(SLIDE)(PAIR(ZERO)(ZERO)))
ADD = lambda m: lambda n: n(INCREMENT)(m)
SUBTRACT = lambda m: lambda n: n(DECREMENT)(m)
MULTIPLY = lambda m: lambda n: n(ADD(m))(ZERO)
POWER = lambda m: lambda n: n(MULTIPLY(m))(ONE)

IS_LESS_OR_EQUAL = lambda m: lambda n: IS_ZERO(SUBTRACT(m)(n))

Y = lambda f: lambda x: f(x(x))(lambda x: f(x(x)))
Z = lambda f: (lambda x: f(lambda y: x(x)(y)))(lambda x: f(lambda y: x(x)(y)))

MOD = \
    Z(lambda f: lambda m: lambda n: \
        IF(IS_LESS_OR_EQUAL(n)(m))( \
            lambda x: \
                f(SUBTRACT(m)(n))(n)(x) \
        )( \
                m \
        )
      )
 
 
 # 6.1.8 列表
EMPTY = PAIR(TRUE)(TRUE)
UNSHIFT = lambda l: lambda x: PAIR(FALSE)(PAIR(x)(l))
IS_EMPTY = LEFT
FIRST = lambda l: LEFT(RIGHT(l))
REST = lambda l: RIGHT(RIGHT(l))

def to_array(proc):
    array = []
    while True:
        array.append(FIRST(proc))
        proc = REST(proc)
        if to_boolean(IS_EMPTY(proc)):
            break
    return array

# range
RANGE = \
    Z(lambda f: \
        lambda m: lambda n: \
            IF(IS_LESS_OR_EQUAL(m)(n))( \
                lambda x: \
                    UNSHIFT(f(INCREMENT(m))(n))(m)(x) \
            )( \
                EMPTY \
            
            )
    )

# 实现map
FOLD = \
    Z(lambda f: \
        lambda l: lambda x: lambda g: \
            IF(IS_EMPTY(l))( \
                x \
            )( \
               lambda y: \
                    g(f(REST(l))(x)(g))(FIRST(l))(y) \
            )
    
    )

MAP = \
    lambda k: lambda f: \
        FOLD(k)(EMPTY)( \
            lambda l: lambda x: UNSHIFT(l)(f(x))
        )


# 6.1.9 字符串
TEN = MULTIPLY(TWO)(FIVE)
B = TEN
F = INCREMENT(B)
I = INCREMENT(F)
U = INCREMENT(I)
ZED = INCREMENT(U)

FIZZ = UNSHIFT(UNSHIFT(UNSHIFT(UNSHIFT(EMPTY)(ZED))(ZED))(I))(F)
BUZZ = UNSHIFT(UNSHIFT(UNSHIFT(UNSHIFT(EMPTY)(ZED))(ZED))(U))(B)
FIZZBUZZ = UNSHIFT(UNSHIFT(UNSHIFT(UNSHIFT(BUZZ)(ZED))(ZED))(I))(F)

def to_char(c):
    return '0123456789BFiuz'[to_integer(c)]

def to_string(s):
    return ''.join([to_char(c) for c in to_array(s)])


## UnitTest
import unittest

class TestLambda(unittest.TestCase):
    """ Tests of the books's code
    """
        
    def test_proc(self):
        self.assertEqual((lambda x: x + 2)(1), 3)
        self.assertEqual((lambda x:(lambda y: x + y))(3)(4), 7)
        p = lambda n: n * 2
        q = lambda x: p(x)
        self.assertEqual(p(5), 10)
        self.assertEqual(q(5), 10)

    def test_number(self):
        self.assertEqual(to_integer(ZERO), 0)
        self.assertEqual(to_integer(THREE), 3)
        self.assertEqual(to_integer(FIFTY), 50)

    def test_boolean(self):
        self.assertEqual(to_boolean(TRUE), True)
        self.assertEqual(to_boolean(FALSE), False)

    def test_if(self):
        self.assertEqual(IF(TRUE)('happy')('sad'), 'happy')
        self.assertEqual(IF(FALSE)('happy')('sad'), 'sad')

    def test_is_zero(self):
        self.assertEqual(to_boolean(IS_ZERO(ZERO)), True)
        self.assertEqual(to_boolean(IS_ZERO(THREE)), False)

    def test_pair(self):
        my_pair = PAIR(THREE)(FIVE)
        self.assertEqual(to_integer(LEFT(my_pair)), 3)
        self.assertEqual(to_integer(RIGHT(my_pair)), 5)

    def test_calculation(self):
        self.assertEqual(to_integer(INCREMENT(FIVE)), 6)
        self.assertEqual(to_integer(DECREMENT(FIVE)), 4)
        self.assertEqual(to_integer(ADD(FIVE)(THREE)), 8)
        self.assertEqual(to_integer(SUBTRACT(FIVE)(THREE)), 2)
        self.assertEqual(to_integer(MULTIPLY(FIVE)(THREE)), 15)
        self.assertEqual(to_integer(POWER(THREE)(THREE)), 27)
        self.assertEqual(to_boolean(IS_LESS_OR_EQUAL(ONE)(TWO)), True)
        self.assertEqual(to_boolean(IS_LESS_OR_EQUAL(TWO)(TWO)), True)
        self.assertEqual(to_boolean(IS_LESS_OR_EQUAL(THREE)(TWO)), False)
        self.assertEqual(to_integer(MOD(THREE)(TWO)), 1)
    
    def test_list(self):
        my_list = UNSHIFT(UNSHIFT(UNSHIFT(EMPTY)(THREE))(TWO))(ONE)
        self.assertEqual(to_integer(FIRST(my_list)), 1)
        self.assertEqual(to_integer(FIRST(REST(my_list))), 2)
        self.assertEqual(to_integer(FIRST(REST(REST(my_list)))), 3)
        self.assertEqual(to_boolean(IS_EMPTY(my_list)), False)
        self.assertEqual(to_boolean(IS_EMPTY(EMPTY)), True)
    
    def test_array(self):
        my_list = UNSHIFT(UNSHIFT(UNSHIFT(EMPTY)(THREE))(TWO))(ONE)
        self.assertEqual([to_integer(p) for p in to_array(my_list)], [1, 2, 3])

    def test_range(self):
        my_range = RANGE(ONE)(FIVE)
        self.assertEqual([to_integer(p) for p in to_array(my_range)], [1, 2, 3, 4, 5])
    
    def test_map(self):
        self.assertEqual(to_integer(FOLD(RANGE(ONE)(FIVE))(ZERO)(ADD)), 15)
        self.assertEqual(to_integer(FOLD(RANGE(ONE)(FIVE))(ONE)(MULTIPLY)), 120)
        my_list = MAP(RANGE(ONE)(FIVE))(INCREMENT)
        self.assertEqual([to_integer(p) for p in to_array(my_list)], [2, 3, 4, 5, 6])
        
    def test_string(self):
        self.assertEqual(to_char(ZED), 'z')
        self.assertEqual(to_string(FIZZBUZZ), 'FizzBuzz')


if __name__ == '__main__':
    unittest.main()
