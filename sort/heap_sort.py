#!usr/bin/env python3
## Heap Sort Algorithm

def sink(pq, k, end_num):
    while 2*k < end_num:
        j = 2 * k
        if pq[j] < pq[j+1]:
            j += 1
        if pq[k] > pq[j]:
            break
        pq[k], pq[j] = pq[j], pq[k]
        k = j


def heap_sort(pq):
    end_num = len(arr) - 1
    for k in range(end_num//2, 0, -1):
        sink(pq, k, end_num)
        

    while end_num > 1:
        pq[1], pq[end_num] = pq[end_num], pq[1]
        end_num -= 1
        sink(pq, 1, end_num)
        
        

## test
arr = [0, 1, 3, 1, 4, 2, 4, 2, 3, 2, 4, 7, 6, 6, 7, 5, 0, 5, 7, 7]
arr.insert(0, None)
heap_sort(arr)
arr.pop(0)
print(arr)
