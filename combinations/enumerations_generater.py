##enumerations_generater
##枚举算法
##python 3.4
import time 

def enumerations_generater(elements, length):
    """对有N个元素的列表，取X次（可取重复的元素）。生成全部的组合情况。
       参数： elements ：有N个元素的列表。
             length ：取元素的次数，也就是生成的组合的长度。
       结果： 一个组合生成器，使用for循环进行迭代，给出所有组合。
    """
    result = [None for n in range(length)]
    base = len(elements)  
    for num in range(base ** length):
        for index in range(length):
            result[length - index - 1] = elements[num % base]
            num = num // base
        yield result
 
 
##test
t = time.time()
numbers = 0
for n in enumerations_generater([0,1,2,3,4,5,6,7,8,9], 3):
    numbers += 1
    print(n)

t = time.time() - t
print("total run time: %f" % t)
print("All numbers: %d" % numbers)
