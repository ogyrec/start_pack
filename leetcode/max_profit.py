from typing import List

class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        max_profit = 0
        for i in range(1, len(prices)):
            if prices[i] > prices[i-1]:
                max_profit += prices[i] - prices[i-1]
        return max_profit
    


a = [7,1,5,3,6,4]
s = Solution()
print(s.maxProfit(a))

        # max_profit = 0
        # for i in range(1, len(prices)):
        #     if prices[i] > prices[i-1]:
        #         max_profit += prices[i] - prices[i-1]
        # return max_profit