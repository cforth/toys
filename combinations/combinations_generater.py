##combinations_generater
##组合算法
##python 3.4
import time
import codecs

def intx(the_list, base):
    num = 0
    for i in range(len(the_list)):
        num = num * base + the_list[i]
    return num


def change_base(num, base):
    result = []
    while True:
        result.insert(0, num % base)
        num = num // base
        if num <= 0:
            return result

    
def combination_sieve(num_list_start, num_list_end, base):
    for num in range(intx(num_list_start, base), intx(num_list_end, base) + 1, 1):
        num_list = change_base(num, base)
        choose = True
        for index in range(len(num_list) - 1):
            if num_list[index] >= num_list[index + 1]:
                choose = False
                break
        if choose:
            yield(num_list)


def combinations_generater(elements, length):
    list_length = len(elements)
    index_start = []
    index_end = []
    
    for i in range(length):
        index_start.append(i+1)
    for j in range(list_length - length, list_length, 1):
        index_end.append(j+1)
    base = list_length + 1

    for index in combination_sieve(index_start, index_end, base):
        result = []
        for k in index:
            result.append(elements[k-1])
        yield(result)


##test
##Super Lotto(35 choose 5 and 12 choose 2)
        
##35 choose 5
t1 = time.time()
the_list =  []
for i in range(1, 36, 1):
    the_list.append(str(i))
length = 5

result_35c5 = {}
numbers = 0
for n in combinations_generater(the_list, length):
    numbers += 1
    result_35c5[numbers] = n

t1 = time.time() - t1
print("35 choose 5 total run time: %f" % t1)
print("All numbers: %d" % numbers)


##12 choose 2
t2 = time.time()
the_list =  []
for i in range(1, 13, 1):
    the_list.append(str(i))
length = 2

result_12c2 = {}
numbers = 0
for n in combinations_generater(the_list, length):
    numbers += 1
    result_12c2[numbers] = n

t2 = time.time() - t2
print("12 choose 2 total run time: %f" % t2)
print("All numbers: %d" % numbers)


##35 choose 5 and 12 choose 2
t3 = time.time()
numbers = 0
with codecs.open('f:/temp/all', 'w', 'utf-8') as f:
    for i in range(1, 324632+1, 1):
        for j in range(1, 66+1, 1):
            numbers += 1
            c5 = ','.join(result_35c5[i])
            c2 = ','.join(result_12c2[j])
            result = c5 + ',' + c2 + '\n'
            f.write(result)

t3 = time.time() - t3
print("35 choose 5 and 12 choose 2 total run time: %f" % t3)
print("All numbers: %d" % numbers)
