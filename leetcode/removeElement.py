class Solution:
    def removeElement(self, nums, val):
        length = 0

        for i in range(len(nums)):
            if nums[i] != val:
                nums[length] = nums[i]
                length += 1

        return length    
            
s = Solution()
print(s.removeElement(nums = [0,1,2,2,3,0,4,2], val = 2))            
                
        