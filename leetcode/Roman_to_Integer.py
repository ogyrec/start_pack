roman = {'I':1,'V':5,'X':10,'L':50,'C':100,'D':500,'M':1000}
class Solution:
    def romanToInt(self, S: str) -> int:
        summ= 0
        for i in range(len(S)-1,-1,-1):
            num = roman[S[i]]
            if 3*num < summ: 
                summ = summ-num
            else: 
                summ = summ+num
        return summ


class Solution:
    def reverse(self, x):
        sign = [1,-1][x < 0]
        rst = sign * int(str(abs(x))[::-1])
        return rst if -(2**31)-1 < rst < 2**31 else 0
    

s = Solution()
s.reverse(321)

