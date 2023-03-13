class Solution:
    def maxNumberOfBalloons(self, text: str) -> int:
        dct = {k:0 for k in 'balloon'}
        for t in text:
           if t in dct.keys():
               dct[t] += 1
        dct['o'] = dct['o'] //2
        dct['l'] = dct['l'] //2
        return min(dct.values())


s = Solution()
print(s.maxNumberOfBalloons('nlaebolko'))