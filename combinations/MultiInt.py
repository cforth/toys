## Multi-hexadecimal Integer Number Class
## python 3.4

class MultiInt(object):
    """Multi-hexadecimal Integer Number Class
    example:
        num_list = [2, 3, 8]
        base = 12
        self._num = 2 * base**2 + 3 * base**1 + 8 * base**0
    """   
    def __init__(self, num_list=None, base=None):
        self._num_list = num_list
        self._base = base
        self._num = self.__change_to_base_10()

    def __change_to_base_10(self):
        result = 0
        for i in range(len(self._num_list)):
            result = result * self._base + self._num_list[i]
        return result

    def __add1(self):
        self._num += 1
        return self._num

    def __sub1(self):
        self._num -= 1
        return self._num

    def __num_list(self):
        num = self._num
        result = []
        while True:
            result.insert(0, num % self._base)
            num = num // self._base
            if num <= 0:
                return result        

    def __add__(self, obj):
        if isinstance(obj, MultiInt):
            return self._num + obj.num
        elif isinstance(obj, int):
            return self._num + obj
        else:
            raise BaseException('__add__ Error: Obj Not MultiInt Class!')

    def __sub__(self, obj):
        if isinstance(obj, MultiInt):
            return self._num - obj.num
        elif isinstance(obj, int):
            return self._num - obj
        else:
            raise BaseException('__sub__ Error: Obj Not MultiInt Class!')

    def __mul__(self, obj):
        if isinstance(obj, MultiInt):
            return self._num * obj.num
        elif isinstance(obj, int):
            return self._num * obj
        else:
            raise BaseException('__mul__ Error: Obj Not MultiInt Class!')

    def __truediv__(self, obj):
        if isinstance(obj, MultiInt):
            return self._num / obj.num
        elif isinstance(obj, int):
            return self._num / obj
        else:
            raise BaseException('__truediv__ Error: Obj Not MultiInt Class!')

    def __floordiv__(self, obj):
        if isinstance(obj, MultiInt):
            return self._num // obj.num
        elif isinstance(obj, int):
            return self._num // obj
        else:
            raise BaseException('__floordiv__ Error: Obj Not MultiInt Class!')

    def __mod__(self, obj):
        if isinstance(obj, MultiInt):
            return self._num % obj.num
        elif isinstance(obj, int):
            return self._num % obj
        else:
            raise BaseException('__mod__ Error: Obj Not MultiInt Class!')

    def change_base(self, base):
        num = self._num
        result = []
        while True:
            result.insert(0, num % base)
            num = num // base
            if num <= 0:
                return MultiInt(result, base)

    @property
    def add1(self):
        return self.__add1()

    @property
    def sub1(self):
        return self.__sub1()
        
    @property
    def num(self):
        return self._num

    @property
    def base(self):
        return self._base

    @property
    def num_list(self):
        return self.__num_list()


## UnitTest
import unittest

class TestMultiInt(unittest.TestCase):

    def test_init(self):
        a = MultiInt([2, 3, 8], base=12)
        self.assertEqual(a.num, 332)
        self.assertEqual(a.base, 12)
        self.assertTrue(isinstance(a, MultiInt))

    def test_num_list(self):
        a = MultiInt([2, 3, 8], base=12)
        self.assertEqual(a.num_list, [2,3,8])       

    def test_add1(self):
        a = MultiInt([2, 3, 8], base=10)
        a.add1
        self.assertEqual(a.num, 239)

    def test_sub1(self):
        a = MultiInt([2, 3, 9], base=10)
        a.sub1
        self.assertEqual(a.num, 238)

    def test_add(self):
        a = MultiInt([2, 3, 8], base=12)
        b = MultiInt([2, 3, 8], base=10)
        self.assertEqual(a + b, 570)
        self.assertEqual(a + 238, 570)

    def test_sub(self):
        a = MultiInt([2, 3, 8], base=12)
        b = MultiInt([2, 3, 8], base=10)
        self.assertEqual(a - b, 94)
        self.assertEqual(a - 238, 94)

    def test_mul(self):
        a = MultiInt([2, 3, 8], base=12)
        b = MultiInt([2, 3, 8], base=10)
        self.assertEqual(a * b, 79016)
        self.assertEqual(a * 238, 79016)

    def test_truediv(self):
        a = MultiInt([2, 3, 8], base=12)
        b = MultiInt([2, 3, 8], base=10)
        self.assertEqual(a / b, 1.3949579831932772)
        self.assertEqual(a / 238, 1.3949579831932772)

    def test_floordiv(self):
        a = MultiInt([2, 3, 8], base=12)
        b = MultiInt([2, 3, 8], base=10)
        self.assertEqual(a // b, 1)
        self.assertEqual(a // 238, 1)

    def test_mod(self):
        a = MultiInt([2, 3, 8], base=12)
        b = MultiInt([2, 3, 8], base=10)
        self.assertEqual(a % b, 94)
        self.assertEqual(a % 238, 94)

    def test_change_base(self):
        a = MultiInt([2, 3, 8], base=12)
        b = MultiInt([3, 3, 2], base=10)
        self.assertTrue(isinstance(a.change_base(10), MultiInt))
        self.assertEqual(a.change_base(10).num, b.num)


if __name__ == '__main__':
    unittest.main()
