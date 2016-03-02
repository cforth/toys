#!usr/bin/env python3
## Radix Sort Algorithm

def counting_part(arr_in, arr_out, bit):
    #bit为要排序的位
    bucket = [0 for i in range(11)]

    for i in range(len(arr_in)):
        j = arr_in[i]//(10**bit)%10
        bucket[j] = bucket[j] + 1

    for i in range(1, 11):
        bucket[i] = bucket[i] + bucket[i-1]

    for i in range(len(arr_in)-1, -1, -1):
        j = arr_in[i]//(10**bit)%10
        arr_out[bucket[j]-1] = arr_in[i]
        bucket[j] = bucket[j] - 1


def radix_count(arr, maxbit):
    for i in range(0, maxbit):
        bucket = [0 for j in range(len(arr))]
        counting_part(arr, bucket, i)
        arr = bucket[:]

    return arr
        


#test
def main():
    arr = [329, 457, 657, 839, 436, 720, 355]
    print(arr)
    print(radix_count(arr, 3))


if __name__ == '__main__':
    main()
