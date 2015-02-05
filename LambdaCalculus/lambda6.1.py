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
FIFTEEN = lambda p: lambda x: p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(x)))))))))))))))

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

    def test_boolean(self):
        self.assertEqual(to_boolean(TRUE), True)
        self.assertEqual(to_boolean(FALSE), False)

    def test_if(self):
        self.assertEqual(IF(TRUE)('happy')('sad'), 'happy')
        self.assertEqual(IF(FALSE)('happy')('sad'), 'sad')

    def test_is_zero(self):
        self.assertEqual(to_boolean(IS_ZERO(ZERO)), True)
        self.assertEqual(to_boolean(IS_ZERO(THREE)), False)


if __name__ == '__main__':
    unittest.main()
