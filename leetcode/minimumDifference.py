from typing import List

class Solution:
    def minimumDifference(self, nums: List[int], k: int) -> int:
        nums.sort()
        l, r = 0, k - 1
        res = int("inf")
        
        while r < len(nums):
            res = min(res, nums[r] - nums[l])
            l, r = l + 1, r + 1
        return res
    
s = Solution()
print(s.minimumDifference(nums = [9,4,1,7], k = 2))

