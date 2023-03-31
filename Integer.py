# -*- coding: utf-8 -*-
"""
Created on Tue Mar 28 22:45:10 2023

@author: admin
"""

class Integer(object):
    
    def __init__(self, integer):
        if type(integer) == Integer:
            self.symbol = integer.symbol
            self.number = integer.number.copy()
        else:
            integer = str(integer)
            if integer[0] == "-":
                self.symbol = -1
                self.number = list(map(int, list(integer[1:])))
            else:
                self.symbol = 1
                self.number = list(map(int, list(integer[0:])))
        self.reverse_number = self.number.copy()
        self.reverse_number.reverse()
        
    def __add__(self, another):
        if type(another) != Integer:
            another = Integer(another)
        if self.symbol == another.symbol:
            extra = 0
            ans = []
            for i in range(max(len(self),len(another))):
                a = self.getitem_inv(i)
                b = another.getitem_inv(i)
                c = a+b+extra
                ans.append(c % 10)
                extra = c // 10
            if extra > 0:
                ans.append(extra)
            ans.reverse()     
            return Integer(("-" if self.symbol == -1 else "") + "".join(map(str,ans)))
        else:
            extra = 0
            ans = []
            if self.abs_ge(another):
                u = self
                l = another
                symbol = 1 * self.symbol
            else:
                u = another
                l = self
                symbol = -1 * self.symbol
            for i in range(max(len(self),len(another))):
                
                a = u.getitem_inv(i)
                b = l.getitem_inv(i)
                c = a-b+extra
                ans.append(c % 10)
                extra = c // 10
            ans.reverse()     
            return Integer(("-" if symbol == -1 else "") + "".join(map(str,ans))).reduce()
   
    def __sub__(self, another):
        return self + (-another)
        
    def __neg__(self):
        new = Integer(self)
        new.symbol *= -1
        return new
    
    def __mul__(self, another):
        if type(another) != Integer:
            another = Integer(another)
        if len(another) == 1:
            symbol = -1 if self.symbol*another.symbol<0 else 1
            another = another.getitem_inv(0)
            extra = 0
            ans = []
            for i in range(len(self)):
                a = self.getitem_inv(i)
                c = another*a + extra
                ans.append(c % 10)
                extra = c // 10
            
            if extra > 0:
                ans.append(extra)
            ans.reverse()    
            return Integer(("-" if symbol == -1 else "") + "".join(map(str,ans))).reduce()
        else:
            symbol = -1 if self.symbol*another.symbol<0 else 1
            add_list = []
            abs_self = abs(self)
            for i in range(len(another)):
                a = abs_self * another.getitem_inv(i)
                add_list.append(a.move(i))
            ans = Integer("0")
            for a in add_list:
                ans += a
            ans.symbol = symbol
            return ans.reduce()
                
    def move(self, bit):
        if bit>=0:
            self.number.extend([0]*bit)
        else:
            self.number = self.number[:bit]
        self.reverse_number = self.number.copy()
        self.reverse_number.reverse()
        return self
    
    def __rshift__(self, bit):
        if bit<0:
            raise ValueError
        return self.copy().move(bit)
    
    def __lshift__(self, bit):
        if bit<0:
            raise ValueError
        return self.copy().move(-bit)
                
    def getitem_inv(self, idx):
        if idx >= len(self):
            return 0
        else:
            return self.reverse_number[idx]
            
    def __abs__(self):
        tmp = str(self)
        if tmp[0] == "-":
            return Integer(tmp[1:])
        else:
            return Integer(tmp)
        
    def abs_ge(self, another):
        if len(self) == len(another):
            for i in range(len(self)):
                if self.number[i] > another.number[i]:
                    return True
                elif self.number[i] < another.number[i]:
                    return False
            return True
        else:
            return len(self) > len(another)
    
    def abs_gt(self, another):
        if len(self) == len(another):
            for i in range(len(self)):
                if self.number[i] > another.number[i]:
                    return True
                elif self.number[i] < another.number[i]:
                    return False
            return False
        else:
            return len(self) > len(another)
        
    def __ge__(self, another):
        if type(another) != Integer:
            another = Integer(another)
        if self.symbol == another.symbol:
            return not self.abs_gt(another) if self.symbol == -1 else self.abs_ge(another)
        else:
            return self.symbol >= another.symbol
    
    def __gt__(self, another):
        if type(another) != Integer:
            another = Integer(another)
        if self.symbol == another.symbol:
            return not self.abs_ge(another) if self.symbol == -1 else self.abs_gt(another)
        else:
            return self.symbol > another.symbol
        
    def __eq__(self, another):
        if type(another) != Integer:
            another = Integer(another)
        return self.symbol == another.symbol and self.number == another.number
    
    def __radd__(self, another):
        return self + another

    def __rmul__(self, another):
        return self * another
    
    def __rsub__(self, another):
        return  - self + another

    def __int__(self):
        return int(str(self))
    
    def __len__(self):
        return len(self.number)
    
    def __floordiv__(self, another):
        return divmod(self, another)[0]
    
    def __mod__(self, another):
        return divmod(self, another)[1]
    
    def __divmod__(self, another):
        if type(another) != Integer:
            another = Integer(another)
        symbol = self.symbol * another.symbol
        symbol_mod = another.symbol
        another = abs(another)
        if another.abs_gt(self):
            return Integer("0") if symbol == 1 else Integer("-1"), self.copy() if self.symbol == symbol_mod else self + symbol_mod*another
        else:
            table = [i*another for i in range(11)]
            length = len(another)
            ans = []
            tmp = abs(self.copy())
            i = len(tmp)-length
            while i>=0:
                num = tmp<<i
                for j, item in enumerate(table):
                    if item > num:
                        break
                ans.append(j-1)
                tmp -= (table[j-1] >> i)
                i -= 1
                
            return Integer(("-" if symbol == -1 else "") + "".join(map(str,ans))).reduce(), tmp if tmp.symbol == symbol_mod else tmp + symbol_mod*another
        
    def __repr__(self):
        return ("-" if self.symbol == -1 else "") + "".join(map(str,self.number))
    
    def __rfloordiv__(self, another):
        if type(another) != Integer:
            another = Integer(another)
        return divmod(another, self)[0]
    
    def __rmod__(self, another):
        if type(another) != Integer:
            another = Integer(another)
        return divmod(another, self)[1]
        
    def reduce(self):
        i = 0
        while self.number[i] == 0:
            if i == len(self) - 1:
                break
            i += 1
        self.number = self.number[i:]
        self.reverse_number = self.number.copy()
        self.reverse_number.reverse()
        return self
    
    def copy(self):
        return Integer(self)
    
    def to_bin(self):
        tmp = self.copy()
        ans = []
        while tmp > 0:
            tmp, res = divmod(tmp, 2)
            ans.append(res)
        ans.reverse()
        return ans
