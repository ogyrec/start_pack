from typing import List

class Solution:
    def longestCommonPrefix(self, strs: List[str]) -> str:
        if not strs:
            return ""
            
        shortest = min(strs,key=len)
        for i, ch in enumerate(shortest):
            for other in strs:
                if other[i] != ch:
                    return shortest[:i]
        return shortest 


a = ["flower","flow","flight"]
# a = ["dog","racecar","car"]
s = Solution()
print(s.longestCommonPrefix(a))