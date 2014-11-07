def my_map(function, the_list):
    return [function(each_item) for each_item in the_list]


def f(x):
    return x * x


foo = my_map(f, [1,2,3,4,5,6,7,8,9])

print(foo)

## [1, 4, 9, 16, 25, 36, 49, 64, 81]


def my_reduce(function, the_list):
    result = the_list[0]
    the_list = the_list[1:]
    for each_item in the_list:
        result = function(result, each_item)
    return result


def f(x, y):
    return x * y

def f2(str1, str2):
    return str1 + ':' +str2


foo = my_reduce(f, [1,2,3,4,5,6])

print(foo)

## 720

foo2 = my_reduce(f2, ['hello', 'ni', 'hao'])

print(foo2)

## hello:ni:hao
