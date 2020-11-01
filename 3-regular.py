def memoize(f):
    r = {}

    def g(*args):
        if args not in r:
            r[args] = f(*args)
        return r[args]

    return g


def coprime(x, n):
    return all(x % i != 0 or n % i != 0 for i in range(2, x + 1))


def phi(n):
    return len([x for x in range(1, n + 1) if coprime(x, n)])


@memoize
def S(n, k):  # Sphere, n darts, root of degree k
    if n <= 0 or k <= 0:
        return int(k == 0 and n == 0)
    res = S(n - 2, k + 1)
    for n_ in range(0, n - 1, 2):
        for k_ in range(k - 1):
            res += S(n - n_ - 2, k - k_ - 2) * S(n_, k_)
    return res


@memoize
def P(n, k):  # Projective plane, n darts, root of degree k
    if n <= 0 or k <= 0:
        return 0
    res = P(n - 2, k + 1) + (k - 1) * S(n - 2, k - 2)
    for n_ in range(0, n - 1, 2):
        for k_ in range(k - 1):
            res += 2 * P(n - n_ - 2, k - k_ - 2) * S(n_, k_)
    return res


@memoize
def P1(n, k):  # Projective plane, n darts, root of degree k, extra leaf
    if n <= 0 or k <= 0:
        return 0
    res = P1(n - 2, k + 1) + (k - 1) * Q1(n - 2, k - 2) + P(n - 2, k - 1)
    for n_ in range(0, n - 1, 2):
        for k_ in range(k - 1):
            res += 2 * P1(n - n_ - 2, k - k_ - 2) * S(n_, k_)
            res += 2 * P(n - n_ - 2, k - k_ - 2) * Q1(n_, k_)
    return res


@memoize
def Q1(n, k):  # Sphere, n darts, extra leaf
    if n <= 0 or k <= 0:
        return 0
    res = Q1(n - 2, k + 1) + S(n - 2, k - 1)
    for n_ in range(0, n - 1, 2):
        for k_ in range(k - 1):
            res += 2 * Q1(n - n_ - 2, k - k_ - 2) * S(n_, k_)
    return res


@memoize
def DD(n, k):  # Sphere, two roots of total degree k
    if n <= 0 or k <= 0:
        return 0
    res = DD(n - 2, k + 1) - Q1(n - 2, k) + k * (k - 1) // 2 * S(n - 2, k - 2)
    for n_ in range(0, n - 1, 2):
        for k_ in range(k - 1):
            res += 2 * S(n - n_ - 2, k - k_ - 2) * DD(n_, k_)
    return res


@memoize
def K(n, k):  # Klein bottle, n darts, root of degree k
    if n <= 0 or k <= 0:
        return 0
    res = K(n - 2, k + 1) + (k - 1) * P(n - 2, k - 2) + DD(n - 2, k - 2)
    for n_ in range(0, n - 1, 2):
        for k_ in range(k - 1):
            res += P(n - n_ - 2, k - k_ - 2) * P(n_, k_)
            res += 2 * S(n - n_ - 2, k - k_ - 2) * K(n_, k_)
    return res


@memoize
def Pm(n, m):  # Projective plane with a branch point, lifts to 3-regular, n darts, branch index m
    res = P(n, 3) * (1 + n // 6)  # F
    if m == 3:
        res += P(n, 1) * n  # V
    if m == 2:
        res += P(n + 1, 1) * n  # E
    return res


@memoize
def Din(n, k):  # Disk, n darts, root of degree k in interior
    if n <= 0 or k <= 0:
        return 0
    res = Din(n - 2, k + 1) + Dout(n - 1, k - 1) + 2 * Dout(n - 3, k)
    for n_ in range(n - 1):
        for k_ in range(k - 1):
            res += 2 * Din(n - n_ - 2, k - k_ - 2) * S(n_, k_)
    return res


@memoize
def Din_1(n, k):  # Disk, n darts, root of degree k in interior, one more leaf
    if n <= 0 or k <= 0:
        return 0
    res = Din_1(n - 2, k + 1) + Dout_1(n - 1, k - 1) + 2 * Dout_1(n - 3, k) + Din(n - 2, k - 1)
    for n_ in range(n - 1):
        for k_ in range(k - 1):
            res += 2 * Din_1(n - n_ - 2, k - k_ - 2) * S(n_, k_)
            res += 2 * Din(n - n_ - 2, k - k_ - 2) * Q1(n_, k_)
    return res


@memoize
def Dout(n, k):  # Disk, n darts, root of degree k on exterior, no boundary edges at root
    if n <= 0 or k <= 0:
        return int(k == 0 and n == 0)
    res = Dout(n - 2, k + 1) + Dout(n - 1, k - 1) + Dout(n - 3, k)
    for n_ in range(n - 1):
        for k_ in range(k - 1):
            res += Dout(n - n_ - 2, k - k_ - 2) * S(n_, k_)
    for n_ in range(n - 2):
        res += Dout(n - n_ - 3, k - 1) * Dout(n_, 1)
    return res


@memoize
def Dout_1(n, k):  # Disk, n darts, root of degree k on exterior, no boundary edges at root, extra leaf in interior
    if n <= 0 or k <= 0:
        return 0
    res = Dout_1(n - 2, k + 1) + Dout_1(n - 1, k - 1) + Dout_1(n - 3, k) + Dout(n - 2, k - 1)
    for n_ in range(n - 1):
        for k_ in range(k - 1):
            res += Dout_1(n - n_ - 2, k - k_ - 2) * S(n_, k_)
            res += Dout(n - n_ - 2, k - k_ - 2) * Q1(n_, k_)
    for n_ in range(n - 2):
        res += Dout_1(n - n_ - 3, k - 1) * Dout(n_, 1)
        res += Dout(n - n_ - 3, k - 1) * Dout_1(n_, 1)
    return res


@memoize
def D1(n, k):  # Disk, n darts, root of degree k on exterior, one distinguished boundary leaf
    if n <= 0 or k <= 0:
        return 0
    res = D1(n - 2, k + 1) + D1(n - 1, k - 1) + D1(n - 3, k) + Dout(n - 2, k - 1)
    for n_ in range(n - 1):
        for k_ in range(k - 1):
            res += D1(n - n_ - 2, k - k_ - 2) * S(n_, k_)
    for n_ in range(n - 2):
        res += Dout(n - n_ - 3, k - 1) * D1(n_, 1)
        res += D1(n - n_ - 3, k - 1) * Dout(n_, 1)
    return res


@memoize
def Cout(n, k):  # Annulus, n darts, root of degree k on exterior, no boundary edges at root
    if n <= 0 or k <= 0:
        return 0
    res = Cout(n - 2, k + 1) + Cout(n - 1, k - 1) + Cout(n - 3, k) + D1(n - 3, k - 1)
    for n_ in range(n - 1):
        for k_ in range(k - 1):
            res += Cout(n - n_ - 2, k - k_ - 2) * S(n_, k_)
            res += Dout(n - n_ - 2, k - k_ - 2) * Din(n_, k_)
    for n_ in range(n - 2):
        res += Dout(n - n_ - 3, k - 1) * Cout(n_, 1)
        res += Cout(n - n_ - 3, k - 1) * Dout(n_, 1)
    return res


@memoize
def Cin(n, k):  # Annulus, n darts, root of degree k in interior
    if n <= 0 or k <= 0:
        return 0
    res = Cin(n - 2, k + 1) + Cout(n - 1, k - 1) + 2 * Cout(n - 3, k)
    for n_ in range(n - 1):
        for k_ in range(k - 1):
            res += 2 * Cin(n - n_ - 2, k - k_ - 2) * S(n_, k_)
            res += Din(n - n_ - 2, k - k_ - 2) * Din(n_, k_)
    return res


@memoize
def Mout(n, k):  # Möbius band, n darts, root of degree k on exterior, no boundary edges at root
    if n <= 0 or k <= 0:
        return 0
    res = Mout(n - 2, k + 1) + Mout(n - 1, k - 1) + Mout(n - 3, k) + D1(n - 3, k - 1) + (k - 1) * Dout(n - 2, k - 2)
    for n_ in range(n - 1):
        for k_ in range(k - 1):
            res += Mout(n - n_ - 2, k - k_ - 2) * S(n_, k_)
            res += Dout(n - n_ - 2, k - k_ - 2) * P(n_, k_)
    for n_ in range(n - 2):
        res += Dout(n - n_ - 3, k - 1) * Mout(n_, 1)
        res += Mout(n - n_ - 3, k - 1) * Dout(n_, 1)
    return res


@memoize
def Min(n, k):  # Möbius band, n darts, root of degree k in interior
    if n <= 0 or k <= 0:
        return 0
    res = Min(n - 2, k + 1) + Mout(n - 1, k - 1) + 2 * Mout(n - 3, k)
    res += (k - 1) * Din(n - 2, k - 2)
    for n_ in range(n - 1):
        for k_ in range(k - 1):
            res += 2 * Min(n - n_ - 2, k - k_ - 2) * S(n_, k_)
            res += 2 * Din(n - n_ - 2, k - k_ - 2) * P(n_, k_)
    return res


@memoize
def Din_F(n, k):  # Disk, n darts, root of degree k in interior, 1 distinguished face
    if n <= 0 or k <= 0:
        return 0
    res = Din_F(n - 2, k + 1) + Dout_F(n - 1, k - 1) + 2 * Dout_F(n - 3, k)
    for n_ in range(n - 1):
        for k_ in range(k - 1):
            res += 2 * Din(n - n_ - 2, k - k_ - 2) * S(n_, k_) * (1 + (2 * k_ + n_) // 6)
            res += 2 * Din_F(n - n_ - 2, k - k_ - 2) * S(n_, k_)
    return res


@memoize
def Din_2F(n, k):  # Disk, n darts, root of degree k in interior, 1 distinguished face
    if n <= 0 or k <= 0:
        return 0
    res = Din_2F(n - 2, k + 1) + Dout_2F(n - 1, k - 1) + 2 * Dout_2F(n - 3, k)
    for n_ in range(n - 1):
        for k_ in range(k - 1):
            res += 2 * Din(n - n_ - 2, k - k_ - 2) * S(n_, k_) * (1 + (2 * k_ + n_) // 6) * (2 * k_ + n_) // 12
            res += 2 * Din_F(n - n_ - 2, k - k_ - 2) * S(n_, k_) * (1 + (2 * k_ + n_) // 6)
            res += 2 * Din_2F(n - n_ - 2, k - k_ - 2) * S(n_, k_)
    return res


@memoize
def Dout_F(n, k):  # Disk, n darts, root of degree k on exterior, no boundary edges at root, 1 distinguished face
    if n <= 0 or k <= 0:
        return 0
    res = Dout_F(n - 2, k + 1) + Dout_F(n - 1, k - 1) + Dout_F(n - 3, k)
    for n_ in range(n - 1):
        for k_ in range(k - 1):
            res += Dout_F(n - n_ - 2, k - k_ - 2) * S(n_, k_)
            res += Dout(n - n_ - 2, k - k_ - 2) * S(n_, k_) * (1 + (2 * k_ + n_) // 6)
    for n_ in range(n - 2):
        res += Dout_F(n - n_ - 3, k - 1) * Dout(n_, 1)
        res += Dout(n - n_ - 3, k - 1) * Dout_F(n_, 1)
    return res


@memoize
def Dout_2F(n, k):  # Disk, n darts, root of degree k on exterior, no boundary edges at root, 2 distinguished faces
    if n <= 0 or k <= 0:
        return 0
    res = Dout_2F(n - 2, k + 1) + Dout_2F(n - 1, k - 1) + Dout_2F(n - 3, k)
    for n_ in range(n - 1):
        for k_ in range(k - 1):
            res += Dout_2F(n - n_ - 2, k - k_ - 2) * S(n_, k_)
            res += Dout_F(n - n_ - 2, k - k_ - 2) * S(n_, k_) * (1 + (2 * k_ + n_) // 6)
            res += Dout(n - n_ - 2, k - k_ - 2) * S(n_, k_) * (1 + (2 * k_ + n_) // 6) * (2 * k_ + n_) // 12
    for n_ in range(n - 2):
        res += Dout_2F(n - n_ - 3, k - 1) * Dout(n_, 1)
        res += Dout(n - n_ - 3, k - 1) * Dout_2F(n_, 1)
        res += Dout_F(n - n_ - 3, k - 1) * Dout_F(n_, 1)
    return res


@memoize
def Dm(n, m):  # Disk with a branch point, lifts to 3-regular, n darts, branch index m
    res = Din_F(n, 3) + 3 * Dout_F(n - 1, 2)
    if m == 2:
        res += Din(n + 1, 1) * n
    if m == 3:
        res += Din(n, 1) * n
    return res


@memoize
def Mm(n):  # Möbius band, lifts to 3-regular
    res = Min(n, 3) + 3 * Mout(n - 1, 2)
    return res


@memoize
def Cm(n):  # Annulus, lifts to 3-regular
    res = Cin(n, 3) + 3 * Cout(n - 1, 2)
    return res


# Projective plane, unsensed
def P_unsensed(n):
    # n = 2*|V|
    res = P(6 * n, 3)
    for L in range(2, 6 * n + 1):
        if (6 * n) % L != 0:
            continue
        n_ = 6 * n // L
        if L % 2 == 0:
            res += phi(L) * Dm(n_, L)
        else:
            res += phi(L) * Pm(n_, L)
    if res % (6 * n) != 0:
        raise AssertionError('%d %d' % (res, 6 * n))

    return res // (12 * n)


def div(n, k):
    if n % k != 0:
        raise AssertionError('%s // %s' % (n, k))
    return n // k


# Disc, two branch points, lifts to Klein bottle
def K_D(n):
    s = 0
    s += Din_2F(n, 3) + 3 * Dout_2F(n - 1, 2)  # F F
    s += n * Din_F(n + 1, 1)  # E F
    s += div(n * Din_1(n + 2, 1), 2)  # E E
    return s


# Projective plane, two branch points, lifts to Klein bottle
def K_P(n):
    s = 0
    s += div(P(n, 3) * (1 + n // 6) * n, 12)  # F F
    s += n * P(n + 1, 1) * (1 + n // 6)  # E F
    s += div(n * P1(n + 2, 1), 2)  # E E
    return s


# Klein bottle, unsensed
def K_unsensed(n):
    n = 3 * n  # n = edges
    s = K(2 * n, 3)
    for l in range(2, 2 * n + 1):
        if (2 * n) % l != 0:
            continue
        if l % 2 == 0:
            s += phi(l) * Cm(2 * n // l)
        if l == 2:
            s += K_D(n)
        if l % 2 == 1:
            s += phi(l) * K(2 * n // l, 3)
        if l % 4 == 2:
            s += 2 * phi(l) * K(2 * n // l, 3)
        if l % 2 == 0:
            s += phi(l) * Mm(2 * n // l)
        if l == 2:
            s += 2 * K_P(n)
    return s // (4 * n), s % (4 * n)


def assert_(expr, want):
    got = eval(expr)
    if got != want:
        print('Assertion failed:', expr, '=', got, '!=', want)
        raise AssertionError()


assert_('D1(2, 1)', 1)
assert_('D1(3, 2)', 2)
assert_('D1(2, 1)', 1)
assert_('Dout(1, 1)', 1)
assert_('D1(5, 1)', 4)
assert_('Mout(2, 2)', 1)
assert_('Min(3, 3)', 3)
assert_('Mout(3, 1)', 0)
assert_('Mm(3)', 6)
assert_('Cin(4, 4)', 2)
assert_('Din_1(3,2)', 2)
assert_('14 * Din(15,1)', Din_1(15, 3) + 3 * Dout_1(14, 2))

print('\nP')
for i in range(1, 15):
    print('%4s %18s' % (i, P_unsensed(i)))
print('\nK')
for i in range(1, 15):
    print('%4s %18s' % (i, K_unsensed(i)))
