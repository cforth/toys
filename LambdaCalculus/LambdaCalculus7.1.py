#!/usr/bin/env python3.4

"""Lambda Calculus"""

# "Understanding Computation: Impossible Code and the Meaning of Programs"
# Chapter 7.1 's Code. Use Python3.
# Authors: Chai Fei

# 6.1.3 实现数字
ZERO = lambda p: lambda x: x
ONE = lambda p: lambda x: p(x)
TWO = lambda p: lambda x: p(p(x))
THREE = lambda p: lambda x: p(p(p(x)))
FIVE = lambda p: lambda x: p(p(p(p(p(x)))))
FIFTEEN = lambda p: lambda x: p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(x)))))))))))))))
# 一百层嵌套括号会导致Python解释器解析溢出错误，改用九十层。cpython能解析的括号嵌套的最大层数为92层。
NINETY = lambda p: lambda x: p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(p(x))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))

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

DIV = \
    Z(lambda f: lambda m: lambda n: \
        IF(IS_LESS_OR_EQUAL(n)(m))( \
            lambda x: \
                INCREMENT(f(SUBTRACT(m)(n))(n))(x) \
        )( \
            ZERO \
        ) \
    )

PUSH = \
    lambda l: \
        lambda x: \
        FOLD(l)(UNSHIFT(EMPTY)(x))(UNSHIFT)
        
TO_DIGITS = \
    Z(lambda f: lambda n: PUSH( \
        IF(IS_LESS_OR_EQUAL(n)(DECREMENT(TEN)))( \
            EMPTY \
        )( \
            lambda x: \
                f(DIV(n)(TEN))(x) \
        ) \
    )(MOD(n)(TEN)))


# 7.1 lambda演算
TAPE        = lambda l: lambda m: lambda r: lambda b: PAIR(PAIR(l)(m))(PAIR(r)(b))
TAPE_LEFT   = lambda t: LEFT(LEFT(t))
TAPE_MIDDLE = lambda t: RIGHT(LEFT(t))
TAPE_RIGHT  = lambda t: LEFT(RIGHT(t))
TAPE_BLANK  = lambda t: RIGHT(RIGHT(t))

TAPE_WRITE  = lambda t: lambda c: TAPE(TAPE_LEFT(t))(c)(TAPE_RIGHT(t))(TAPE_BLANK(t))

TAPE_MOVE_HEAD_RIGHT = \
    lambda t: \
        TAPE( 
            PUSH(TAPE_LEFT(t))(TAPE_MIDDLE(t)) 
        )( 
            IF(IS_EMPTY(TAPE_RIGHT(t)))( 
                TAPE_BLANK(t) 
            )( 
                FIRST(TAPE_RIGHT(t)) 
            ) 
        )( 
            IF(IS_EMPTY(TAPE_RIGHT(t)))( 
                EMPTY 
            )( 
                REST(TAPE_RIGHT(t)) 
            ) 
        )( 
            TAPE_BLANK(t) 
        ) 


current_tape = TAPE(EMPTY)(ZERO)(EMPTY)(ZERO)

current_tape = TAPE_WRITE(current_tape)(ONE)

current_tape = TAPE_MOVE_HEAD_RIGHT(current_tape)

current_tape = TAPE_WRITE(current_tape)(TWO)

current_tape = TAPE_MOVE_HEAD_RIGHT(current_tape)

current_tape = TAPE_WRITE(current_tape)(THREE)

current_tape = TAPE_MOVE_HEAD_RIGHT(current_tape)

print([to_integer(p) for p in to_array(TAPE_LEFT(current_tape))])

print(to_integer(TAPE_MIDDLE(current_tape)))

print([to_integer(p) for p in to_array(TAPE_RIGHT(current_tape))])
