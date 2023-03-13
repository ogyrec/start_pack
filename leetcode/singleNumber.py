from typing import List


class Solution:
    def singleNumber(self, nums: List[int]) -> int:
        res = 0
        for n in nums:
            print(n, '^', res)            
            res = n ^ res
            print(res, '\n')            
        return res
    
s = Solution()
print(s.singleNumber([1,2,3,5,3,2,1]))


# Initializing two integer variables
a = 45
b = 21

# Printing a and b before swapping
print("a before swap =", a)
print("b before swap =", b)

print()

# Swapping a and b using XOR operator
a = a ^ b
b = a ^ b
a = a ^ b

# Printing a and b after swapping using XOR
print("a before swap =", a)
print("b before swap =", b)
