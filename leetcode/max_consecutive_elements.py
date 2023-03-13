
"""
Нужно найти максимальное число одинаковых 
подряд идущих символов в строке
"""

def max_consecutive_elements(input_str):
    result, cur_letter_idx = 0, 0
    while cur_letter_idx < len(input_str):
        next_letter_idx = cur_letter_idx
        while next_letter_idx < len(input_str) \
        and input_str[next_letter_idx] == input_str[cur_letter_idx]:
            next_letter_idx += 1
        result = max(result, next_letter_idx - cur_letter_idx)
        cur_letter_idx = next_letter_idx
    return result


print(max_consecutive_elements('abcccdd'))