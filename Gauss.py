from fractions import Fraction


def get_input() -> (list, list):
    print('Формат ввода строки: x_1 x_2 ... x_n | b')
    n = int(input('Введите количество уравнений: '))
    m = int(input('Введите количество переменных: '))

    k, f = [], []
    for i in range(n):
        raw = input(f'Введите строку №{i+1}: ')
        temp = raw.split(' | ')
        row_k = list(map(Fraction, temp[0].split()))
        row_f = Fraction(temp[1])

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
    for _ in range(cols):
        for row in range(top+1, rows):
            if m[top][top] == 0:
                p = next((i for i in range(top+1, rows) if m[i][top] != 0), None)
                if p is None: continue  # Нет ведущего элемента
                
                m[top], m[p] = m[p], m[top]
                free[top], free[p] = free[p], free[top]

            k = m[row][top] / m[top][top]
            a = [m[row][i] - m[top][i]*k for i in range(cols)]
            m[row] = a
            free[row] -= free[top] * k

        top += 1

    to_pop = []
    for i in range(rows):
        if set(m[i]) == {0} and free[i] != 0:
            return [0], [0]  # Система несовместна

        if set(m[i]) == {0} and free[i] == 0:
            to_pop.append(i)

    for i in to_pop[::-1]:
        m.pop(i)
        free.pop(i)


    return m, free


def mult_rows(row_1: list, row_2: list) -> Fraction:
    res = 0
    for a, b in zip(row_1, row_2):
        res += a * b

    return res


def find_roots(m: list, free: list) -> (list, list):
    n = len(free)
    res = [Fraction(0)] * n
    for i in range(n-1, -1, -1):
        buf = mult_rows(m[i], res)
        res[i] = (free[i] - buf) / m[i][i]

    return res, []


def inf_roots(m: list, free: list) -> (list, list):
    n = len(m[0])
    basis = len(free)

    base = [Fraction(0)] * n
    extra = [[Fraction(0)] * n for _ in range(n - basis)]
    basis_inds, extra_inds = find_basis(m, n)
    
    for row in range(basis-1, -1, -1):
        buf = mult_rows(m[row], base)

        base[basis_inds[row]] = (free[row] - buf) / m[row][basis_inds[row]]


    for s in extra:
        j = extra_inds.pop(0)
        s[j] = Fraction(1)

        for row in range(basis-1, -1, -1):
            buf = mult_rows(m[row], s)

            s[basis_inds[row]] = -buf / m[row][basis_inds[row]]


    return base, extra


def inf_or_one(m: list, free: list) -> (list, list):
    if not m and not free: 
        return [], []

    if m == free == [0]:
        return [0], [0]

    rows = len(free)
    cols = len(m[0])

    if rows == cols: return find_roots(m, free)
    else: return inf_roots(m, free)


def find_basis(m: list, n: int) -> (list, list):
    universum = set(range(n))
    basis, extra = set(), set()
    i = 0
    for row in m:
        while not row[i]: i += 1
        basis.add(i)
    
    extra = list(universum.difference(basis))
    basis = list(basis)

    basis.sort()
    extra.sort()

    return basis, extra


def from_frac(f: Fraction) -> str:
    if int(f) == f:
        return str(int(f))

    if float(f) == f:
        return str(float(f))

    return str(f)


def nice_output(basis: list, extra: list):
    if not basis and not extra: 
        print('Решением является любой вектор')
        return None

    if basis == extra == [0]:
        print('Система несовместна, решений нет.')

    n_basis = tuple(map(from_frac, basis))
    n_extra = [tuple(map(from_frac, row)) for row in extra]

    if set(basis) == {0}:
        print('Однородная система. ФСР:')
        for row in n_extra:
            print(*row)

    elif not extra:
        print('Единственное решение:', *n_basis)

    else:
        print('=============================================')
        print('Частное решение:', *n_basis)
        print('ФСР:')
        for row in n_extra:
            print(*row)


def main():
    a, b = get_input()
    a, b = to_stairs(a, b)
    b, e = inf_or_one(a, b)
    nice_output(b, e)


if __name__ == '__main__':
    main()
