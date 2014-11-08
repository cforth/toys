#!usr/bin/env python3
## Selection Sort Algorithm

def selection_sort(the_list):
    length = len(the_list)
    for i in range(length):
        min_index = i
        for n in range(i, length, 1):
            if the_list[n] < the_list[min_index]:
                min_index = n
        the_list[i], the_list[min_index] = the_list[min_index], the_list[i]
    return the_list


## test
test_list = [1, 3, 1, 4, 2, 4, 2, 3, 2, 4, 7, 6, 6, 7, 5, 5, 7, 7]
selection_sort(test_list)
print(test_list)

