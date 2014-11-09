#!usr/bin/env python3
## Merge Sort Algorithm

class MergeSort(object):
    def __init__(self, array):
        self._array = array
        self._aux = [None] * len(array)
        
    def __merge(self, lo, mid, hi):
        i = lo
        j = mid + 1
        for k in range(lo, hi+1):
            self._aux[k] = self._array[k]        
        for k in range(lo, hi+1, 1):
            if i > mid:
                self._array[k] = self._aux[j]
                j += 1
            elif j > hi:
                self._array[k] = self._aux[i]
                i += 1
            elif self._aux[i] < self._aux[j]:
                self._array[k] = self._aux[i]
                i += 1
            else:
                self._array[k] = self._aux[j]
                j += 1

    def __sort(self, lo, hi):
        if lo >= hi:
            return
        mid = lo + ((hi - lo) // 2)
        self.__sort(lo, mid)
        self.__sort(mid+1, hi)
        self.__merge(lo, mid, hi)

    def sort(self):
        self.__sort(0, len(self._array)-1)

    @property
    def array(self):
        return self._array


## test
arr = [0, 1, 3, 1, 4, 2, 4, 2, 3, 2, 4, 7, 6, 6, 7, 5, 0, 5, 7, 7]
test_sort = MergeSort(arr)
test_sort.sort()
print(test_sort.array)


