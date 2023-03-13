class Solution:
    # def isIsomorphic(self, s: str, t: str) -> bool:
    #     zipped_set = set(zip(s, t))
    #     return len(zipped_set) == len(set(s)) == len(set(t))
    
    def isIsomorphic(self, s, t):
        d1, d2 = {}, {}
        for i, val in enumerate(s):
            d1[val] = d1.get(val, []) + [i]
        for i, val in enumerate(t):
            d2[val] = d2.get(val, []) + [i]
        return sorted(d1.values()) == sorted(d2.values())    
    

s = Solution()
print(s.isIsomorphic(s = "paper", t = "title"))