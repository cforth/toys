#!/usr/bin/env python3.4

"""Untyped Lambda Calculus"""

# "Understanding Computation: Impossible Code and the Meaning of Programs"
# Chapter 6.1 's Code. Use Python3.
# Authors: Chai Fei

# Python中没有类似Ruby的proc功能的函数，只能直接用lambda来实现
(lambda x: x +2)(1)

(lambda x:(lambda y: x + y))(3)(4)

p = lambda n: n * 2
q = lambda x: p(x)

print(p(5), q(5))


ZERO = lambda p: lambda x: x
ONE = lambda p: lambda x: p(x)
TWO = lambda p: lambda x: p(p(x))
THREE = lambda p: lambda x: p(p(p(x)))


def to_integer(proc):
    return proc(lambda n: n + 1)(0)


print(to_integer(ZERO), to_integer(THREE))
