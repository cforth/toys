#!usr/bin/env python3
## Shell Sort Algorithm

def shell_sort(the_list):
    n = len(the_list)
    h = 1
    while h < n//3:
        h = h * 3 + 1
    while h >= 1:
        for i in range(1, n, 1):
            if i < h:
                break
            for j in range(i, h-1, -h):
                if the_list[j] < the_list[j-h]:
                    the_list[j-h], the_list[j] = the_list[j], the_list[j-h]
                else:
                    break
        h = h //3
    return the_list


## test
test_list = [0, 1, 3, 1, 4, 2, 4, 2, 3, 2, 4, 7, 6, 6, 7, 5, 0, 5, 7, 7]
shell_sort(test_list)
print(test_list)

