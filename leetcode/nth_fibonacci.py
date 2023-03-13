def nth_fibonacci(n):
    SENTINEL = -1
    # Переменная для мемоизации
    numbers = [SENTINEL] * (n + 1)

    def nth_fibonacci_(n):
        if n <= 1:
            return n
        elif numbers[n] != SENTINEL:
            return numbers[n]
        else:
            result = nth_fibonacci_(n - 1) + nth_fibonacci_(n - 2)
            numbers[n] = result
            return result

    return nth_fibonacci_(n)


def nth_fibonacci_v2(n):
    if n <= 1:
        return n
    previous, current = 0, 1
    for _ in range(n - 1):
        previous, current = current, previous + current
    return current 

print(nth_fibonacci_v2(3))