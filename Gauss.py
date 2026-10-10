def get_input() -> (list, list):
    print('Формат ввода строки: x_1 x_2 ... x_n | b')
    n = int(input('Введите количество уравнений: '))
    m = int(input('Введите количество переменных: '))

    k, f = [], []
    for i in range(n):
        raw = input(f'Введите строку №{i+1}: ')
        temp = raw.split(' | ')
        row_k = list(map(int, temp[0].split()))
        row_f = int(temp[1])

        if len(row_k) != m:
            print('Неверное количество переменных!')
            return [], []

        k.append(row_k)
        f.append(row_f)

    return k, f


def to_stairs(m: list, free: list) -> (list, list):
    rows = len(free)
    cols = len(m[0])
    top = 0
    for _ in range(rows-1):
        for row in range(top+1, rows):
            if m[top][top] == 0:
                continue

            k = m[row][top] / m[top][top]
            a = [m[row][i] - m[top][i]*k for i in range(cols)]
            m[row] = a
            free[row] -= free[top] * k

        top += 1

    for i in range(rows):
        if set(m[i]) == {0} and free[i] != 0:
            print('Матрица насогласована. Решений нет')
            return [], []

        if set(m[i]) == {0} and free[i] == 0:
            m.pop(i)
            free.pop(i)

    return m, free


def find_roots(m: list, free: list) -> (list, list):
    n = len(free)
    res = [0] * n
    for i in range(n-1, -1, -1):
        for j in range(n):

            s = sum([res[j] * m[i][j] for j in range(n) if i != j])

        res[i] = (free[i] - s) / m[i][i]

    return res, []


def inf_roots(m: list, free: list) -> (list, list):
    n = len(m[0])
    basis = len(free)

    base = [0] * n
    extra = [[0] * n for _ in range(n - basis)]
    buf = 0
    
    #  Без буквенных векторов
    for row in range(n-1, -1, -1):
        if row + 1 > basis: base[row] = 0
        else:
            for i in range(row+1, basis):
                buf += m[row][i] * base[i]

            base[row] = (free[row] - buf) / m[row][row]
            buf = 0

    
    #  поиск остальных корней
    buf = 0
    for i in range(basis, n):
        for row in range(n-1, -1, -1):
            if row == i: extra[i-basis][row] = 1
            elif row >= basis: extra[i-basis][row] = 0
            else:
                for k in range(row+1, basis):
                    buf += m[row][k] * extra[i-basis][k]

                extra[i-basis][row] = -(buf + m[row][i]) / m[row][row]
                buf = 0


    return base, extra


def inf_or_one(m: list, free: list):
    rows = len(free)
    cols = len(m[0])

    if rows == cols: return find_roots(m, free)
    else: return inf_roots(m, free)


a, b = get_input()
a, b = to_stairs(a, b)
print(inf_or_one(a, b))
