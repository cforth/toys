#!usr/bin/env python3
## Insertion Sort Algorithm

def insertion_sort(the_list):
    length = len(the_list)
    for i in range(length):
        for n in range(i, 0, -1):
            if the_list[n] < the_list[n-1]:
                the_list[n], the_list[n-1] = the_list[n-1], the_list[n]
            else:
                break
    return the_list


## test
test_list = [0, 1, 3, 1, 4, 2, 4, 2, 3, 2, 4, 7, 6, 6, 7, 5, 0, 5, 7, 7]
insertion_sort(test_list)
print(test_list)

