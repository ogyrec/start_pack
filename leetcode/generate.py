"""
Рассмотрим простой алгоритм сжатия строки. 
Если в строке есть несколько подряд идущих одинаковых подстрок, 
можно заменить их на группу. Например, 
строку aabaabaab можно записать как 3(aab). 
Можно алгоритм применить к сжатой строке, 
получив вложенные группы: 3(2ab).
Дана сжатая строка, требуется её распаковать. 
Например, для строки a2(a2(bc))3db ответ будет aabcbcabcbcdddb.    
"""

def generate(n):
    result = []

    def generate_(left_open, left_closed, accum):
        if not left_open and not left_closed:
            result.append(''.join(accum))
            return
        if left_open:
            accum.append('(')
            generate_(left_open - 1, left_closed, accum)
            accum.pop()
        if left_closed > left_open:
            accum.append(')')
            generate_(left_open, left_closed - 1, accum)
            accum.pop()

    generate_(n, n, [])
    return result 

print(generate('aabcbcabcbcdddb'))