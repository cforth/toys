#!usr/bin/env python3
## Quick Sort Algorithm

def partition(array, lo, hi):
    i = lo
    j = hi + 1
    while(True):
        i += 1
        while array[i] < array[lo]:
            if i == hi:
                break
            i += 1
        j -= 1
        while array[j] > array[lo]:
            if j == lo:
                break
            j -= 1
        if i >= j:
            break
        array[i], array[j] = array[j], array[i]

    array[lo], array[j] = array[j], array[lo]
    return j


def sort(array, lo, hi):
    if lo >= hi:
        return
    index = partition(array, lo, hi)
    sort(array, lo, index - 1)
    sort(array, index + 1, hi)


def quick_sort(array):
    sort(array, 0, len(array) - 1)


## test
arr = [0, 1, 3, 1, 4, 2, 4, 2, 3, 2, 4, 7, 6, 6, 7, 5, 0, 5, 7, 7]
quick_sort(arr)
print(arr)
