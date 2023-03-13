"""
Задача. Дан массив целых чисел arr и целое число X. 
Определите, существует ли в массиве такой 
непрерывный подмассив, что сумма его элементов равна X.
"""

def subarray_sum(non_negative_arr, target):
    right, current_sum = 0, 0
    for left in range(len(non_negative_arr)):
        # пересчитываем сумму
        if left > 0:
            current_sum -= non_negative_arr[left - 1]

        # при необходимости двигаем правую границу
        while right < len(non_negative_arr) and current_sum < target:
            current_sum += non_negative_arr[right]
            right += 1

        if current_sum == target:
            return True

    return False 

non_negative_arr = [1, 2, 4, 7, 11, 31, 44]
target = 49
print(subarray_sum(non_negative_arr, target))

