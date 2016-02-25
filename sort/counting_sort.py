#!usr/bin/env python3
## Counting Sort Algorithm

def counting_sort(A, B, k):
    #let C[0..k] be a new array
    C = [0 for i in range(0, k+1)]

    for j in range(0, len(A)):
        C[A[j]] = C[A[j]] + 1
    #C[i] now contains the number of elements equals to i.
    for i in range(1, k+1):
        C[i] = C[i] + C[i-1]
    #C[i] now contains the number of elements less than or equal to i.
    for j in range(len(A)-1, -1, -1):
        B[C[A[j]]-1] = A[j]
        C[A[j]] = C[A[j]] - 1
        


## test
arr = [0, 1, 3, 1, 4, 2, 4, 2, 3, 2, 4, 7, 6, 6, 7, 5, 0, 5, 7, 7]
arr_out = [0 for i in range(0, len(arr))]
counting_sort(arr, arr_out, 7)
print(arr)
print(arr_out)
