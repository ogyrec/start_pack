from typing import List

class Solution:
    def pivotIndex(self, nums: List[int]) -> int:
        
        for index in range(1, len(nums)):
            if sum(nums[:index]) == sum(nums[index+1:]):
                return index
        return -1
            


            


s = Solution()
print(s.pivotIndex(nums = [1,7,3,6,5,6]))