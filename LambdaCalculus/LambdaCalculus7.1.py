#!/usr/bin/env python3.4

"""Lambda Calculus"""

# "Understanding Computation: Impossible Code and the Meaning of Programs"
# Chapter 7.1 's Code. Use Python3.
# Authors: Chai Fei

# 有序对
PAIR  = lambda x: lambda y: lambda f: f(x)(y)
LEFT  = lambda p: p(lambda x: lambda y: x)
RIGHT = lambda p: p(lambda x: lambda y: y)

TAPE        = lambda l: lambda m: lambda r: lambda b: PAIR(PAIR(l)(m))(PAIR(r)(b))
TAPE_LEFT   = lambda t: LEFT(LEFT(t))
TAPE_MIDDLE = lambda t: RIGHT(LEFT(t))
TAPE_RIGHT  = lambda t: LEFT(RIGHT(t))
TAPE_BLANK  = lambda t: RIGHT(RIGHT(t))
