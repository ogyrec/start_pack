from typing import List
import random

class Solution:
    def sortArray(self, nums: List[int]) -> List[int]:
        # self.quickSort(nums)
        self.mergeSort(nums)
        # self.bubbleSort(nums)
        # self.insertionSort(nums)
		# self.selectionSort(nums)
        # self.heapSort(nums)
        return nums
    
	# @bubbleSort, TLE
    def bubbleSort(self, nums):
        n = len(nums)
        for i in range(n):
            for j in range(0, n - i - 1):
                if nums[j] > nums[j + 1]:
                    nums[j], nums[j + 1] = nums[j + 1], nums[j]
                    
	# @insertionSort, TLE
    def insertionSort(self, nums): 
        for i in range(1, len(nums)): 
            key = nums[i]
            j = i-1
            while j >= 0 and key < nums[j] : 
                    nums[j + 1] = nums[j] 
                    j -= 1
            nums[j + 1] = key
		


    def quickSort(self, nums):
        if len(nums) <= 1:
            return nums

        pivot = random.choice(nums)
        lt = [v for v in nums if v < pivot]
        eq = [v for v in nums if v == pivot]
        gt = [v for v in nums if v > pivot]

        return self.quicksort(lt) + eq + self.quicksort(gt)
     
	# @mergeSort
    def mergeSort(self, nums):
        if len(nums) > 1: 
            mid = len(nums)//2
            L = nums[:mid] 
            R = nums[mid:] 

            self.mergeSort(L)
            self.mergeSort(R)

            i = j = k = 0

            while i < len(L) and j < len(R): 
                if L[i] < R[j]:
                    nums[k] = L[i]
                    i+=1
                else: 
                    nums[k] = R[j] 
                    j+=1
                k+=1
 
            while i < len(L): 
                nums[k] = L[i] 
                i+=1
                k+=1

            while j < len(R): 
                nums[k] = R[j] 
                j+=1
                k+=1
   
   # @heapSort
    def heapSort(self, nums):
        def heapify(nums, n, i): 
            l = 2 * i + 1
            r = 2 * i + 2
			
            largest = i
            if l < n and nums[largest] < nums[l]: 
                largest = l 

            if r < n and nums[largest] < nums[r]: 
                largest = r 

            if largest != i: 
                nums[i], nums[largest] = nums[largest], nums[i]
                
                heapify(nums, n, largest)
                
        n = len(nums) 

        for i in range(n//2+1)[::-1]: 
            heapify(nums, n, i) 

        for i in range(n)[::-1]: 
            nums[i], nums[0] = nums[0], nums[i]
            heapify(nums, i, 0) 


s = Solution()
a = [5,1,1,2,0,0,6,3,9]
print(s.sortArray(a))