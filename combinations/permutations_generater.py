##permutations_generater
##排列算法
##python 3.4
import time


def permutations_generater(elements, length):
    result = [None for n in range(length)]
    base = len(elements)  
    for num in range(base ** length):
        choose = True
        temp_set = set()
        for index in range(length):
            result[length-index-1] = elements[num % base]
            num = num // base
        for n in result:
            if n not in temp_set:
                temp_set.add(n)
            else:
                choose = False
        if choose:
            yield result


##test
t = time.time()
numbers = 0
for i in permutations_generater([0,1,2,3,4,5,6,7,8,9], 3):
    numbers += 1
    print(i)

t = time.time() - t
print("10 choose 3 run time: %f" % t)
print("All numbers: %d" % numbers)

