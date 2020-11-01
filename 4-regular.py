_Fact = {0: 1}


# Factorial
def Fact(n):
    if n not in _Fact:
        _Fact[n] = Fact(n - 1) * n
    return _Fact[n]


_S = {(0, 0): 1}


# Maps on the sphere with n darts and root of degree d.
def S(*args):
    if args in _S:
        return _S[args]
    n, d = args
    if not 0 < d <= n or n % 2 == 1 or d % 2 == 1:
        return 0
    _S[args] = S(n - 2, d + 2)
    for i in range(0, n, 2):
        for j in range(d - 1):
            _S[args] += S(n - i - 2, d - j - 2) * S(i, j)
    return _S[args]


_S2 = {}


# Maps on the sphere with n darts and root of degrees k and l.
def S2(*args):
    if args in _S2:
        return _S2[args]
    n, k, l = args
    if not k + l <= n or k <= 0 or l <= 0 or n % 2 == 1 or (k + l) % 2 == 1:
        return 0
    _S2[args] = S2(n - 2, k + 2, l) + l * S(n - 2, k + l - 2)
    for i in range(0, n, 2):
        for j in range(k - 1):
            _S2[args] += S2(n - i - 2, k - j - 2, l) * S(i, j)
            _S2[args] += S(n - i - 2, k - j - 2) * S2(i, j, l)
    return _S2[args]


# Maps on the sphere with n darts, root of degree d, and 1 branch point in a face.
def S_bp(n, d):
    s = S(n, d)
    if s == 0:
        return 0
    e = n // 2
    v = (n - d) // 4 + 1
    return (2 + e - v) * s


_Q1 = {}


# Maps on the sphere with n darts, root of degree d, and one more distinguished vertex of degree 1.
def Q1(*args):
    if args in _Q1:
        return _Q1[args]
    n, d = args
    if not 0 < d <= n or n % 2 == 1 or d % 2 == 0:
        return 0
    _Q1[args] = Q1(n - 2, d + 2) + S(n - 2, d - 1)
    for i in range(0, n, 2):
        for j in range(d - 1):
            _Q1[args] += 2 * S(n - i - 2, d - j - 2) * Q1(i, j)
    return _Q1[args]


_Q2 = {}


# Maps on the sphere with n darts, root of degree d, and one more distinguished vertices of degree 2.
def Q2(*args):
    if args in _Q2:
        return _Q2[args]
    n, d = args
    if not 0 < d <= n or n % 2 == 1 or d % 2 == 1:
        return 0
    _Q2[args] = Q2(n - 2, d + 2) + 2 * S(n - 2, d)
    for i in range(0, n, 2):
        for j in range(d - 1):
            _Q2[args] += 2 * S(n - i - 2, d - j - 2) * Q2(i, j)
    return _Q2[args]


_QQ = {}


# Maps on the sphere with n darts, root of degree d, and two more distinguished vertices of degree 1.
def QQ(*args):
    if args in _QQ:
        return _QQ[args]
    n, d = args
    if not 0 < d <= n or n % 2 == 1 or d % 2 == 1:
        return 0
    _QQ[args] = QQ(n - 2, d + 2) + Q1(n - 2, d - 1)
    for i in range(0, n, 2):
        for j in range(d - 1):
            _QQ[args] += 2 * S(n - i - 2, d - j - 2) * QQ(i, j)
            _QQ[args] += Q1(n - i - 2, d - j - 2) * Q1(i, j)
    return _QQ[args]


_P = {}


# Maps on the projective plane with n darts and root of degree d.
def P(*args):
    if args in _P:
        return _P[args]
    n, d = args
    if not 0 < d <= n or n % 2 == 1 or d % 2 == 1:
        return 0
    _P[args] = P(n - 2, d + 2) + (d - 1) * S(n - 2, d - 2)
    for i in range(0, n, 2):
        for j in range(d - 1):
            _P[args] += 2 * S(n - i - 2, d - j - 2) * P(i, j)
    return _P[args]


_P1 = {}


# Maps on the projective plane with n darts, root of degree d, and a distinguished leaf.
def P1(*args):
    if args in _P1:
        return _P1[args]
    n, d = args
    if not 0 < d <= n or n % 2 == 1 or d % 2 == 0:
        return 0
    _P1[args] = P1(n - 2, d + 2) + P(n - 2, d - 1) + (d - 1) * Q1(n - 2, d - 2)
    for i in range(0, n, 2):
        for j in range(d - 1):
            _P1[args] += 2 * Q1(n - i - 2, d - j - 2) * P(i, j)
            _P1[args] += 2 * S(n - i - 2, d - j - 2) * P1(i, j)
    return _P1[args]


_D = {}


# Maps on the sphere with two distinguished vertices of total degree d.
def D(*args):
    if args in _D:
        return _D[args]
    n, d = args
    if not 0 < d <= n or n % 2 == 1:
        return 0
    _D[args] = D(n - 2, d + 2) - Q1(n - 2, d + 1) - Q2(n - 2, d) + d * (d - 1) // 2 * S(n - 2, d - 2)
    for i in range(0, n, 2):
        for j in range(d - 1):
            _D[args] += 2 * S(n - i - 2, d - j - 2) * D(i, j)
    return _D[args]


_K = {}


# Maps on the Klein bottle with n darts and root of degree d.
def K(*args):
    if args in _K:
        return _K[args]
    n, d = args
    if not 0 < d <= n or n % 2 == 1 or d % 2 == 1:
        return 0
    _K[args] = K(n - 2, d + 2) + (d - 1) * P(n - 2, d - 2) + D(n - 2, d - 2)
    for i in range(0, n, 2):
        for j in range(d - 1):
            _K[args] += 2 * S(n - i - 2, d - j - 2) * K(i, j) + P(n - i - 2, d - j - 2) * P(i, j)
    return _K[args]


_D_out = {(0, 0): 1}


# Maps on the disk with n darts and root of degree d lying on the boundary;
# root darts is the leftmost dart incident to its vertex.
def D_out(*args):
    if args in _D_out:
        return _D_out[args]
    n, d = args
    if not 0 < d <= n:
        return 0
    _D_out[args] = D_out(n - 2, d + 2) + D_out(n - 1, d - 1) + D_out(n - 2, d)
    for i in range(n - 1):
        _D_out[args] += D_out(i, 1) * D_out(n - i - 2, d - 1)
    for i in range(n - 1):
        for j in range(d - 1):
            _D_out[args] += S(i, j) * D_out(n - 2 - i, d - 2 - j)
    return _D_out[args]


_D_out1 = {}


# Maps on the disk with n darts and root of degree d lying on the boundary;
# root darts is the leftmost dart incident to its vertex. There is one more distingiushed leaf.
def D_out1(*args):
    if args in _D_out1:
        return _D_out1[args]
    n, d = args
    if not 0 < d <= n:
        return 0
    _D_out1[args] = D_out1(n - 2, d + 2) + D_out(n - 2, d - 1) + D_out1(n - 1, d - 1) + D_out1(n - 2, d)
    for i in range(n - 1):
        _D_out1[args] += D_out1(i, 1) * D_out(n - i - 2, d - 1)
        _D_out1[args] += D_out(i, 1) * D_out1(n - i - 2, d - 1)
    for i in range(n - 1):
        for j in range(d - 1):
            _D_out1[args] += Q1(i, j) * D_out(n - 2 - i, d - 2 - j)
            _D_out1[args] += S(i, j) * D_out1(n - 2 - i, d - 2 - j)
    return _D_out1[args]


_D_out2 = {}


# Maps on the disk with n darts and root of degree d lying on the boundary;
# root darts is the leftmost dart incident to its vertex. There is one more distinguished degree 2 vertex.
def D_out2(*args):
    if args in _D_out2:
        return _D_out2[args]
    n, d = args
    if not 0 < d <= n:
        return 0
    _D_out2[args] = D_out2(n - 2, d + 2) + D_out(n - 2, d) + D_out2(n - 1, d - 1) + D_out2(n - 2, d)
    for i in range(n - 1):
        _D_out2[args] += D_out2(i, 1) * D_out(n - i - 2, d - 1)
        _D_out2[args] += D_out(i, 1) * D_out2(n - i - 2, d - 1)
    for i in range(n - 1):
        for j in range(d - 1):
            _D_out2[args] += (i - 2) // 2 * S(i - 2, j) * D_out(n - 2 - i, d - 2 - j)
            _D_out2[args] += S(i, j) * D_out2(n - 2 - i, d - 2 - j)
    return _D_out2[args]


_D_in = {}


# Maps on the disk with n darts and root of degree d lying in the interior.
def D_in(*args):
    if args in _D_in:
        return _D_in[args]
    n, d = args
    if not 0 < d <= n:
        return 0
    _D_in[args] = D_in(n - 2, d + 2) + D_out(n - 1, d - 1) + 2 * D_out(n - 2, d)
    for i in range(n - 1):
        for j in range(d - 1):
            _D_in[args] += 2 * S(i, j) * D_in(n - 2 - i, d - 2 - j)
    return _D_in[args]


_D_in1 = {}


# Maps on the disk with n darts, root of degree d lying in the interior, and a distinguished leaf
def D_in1(*args):
    if args in _D_in1:
        return _D_in1[args]
    n, d = args
    if not 0 < d <= n:
        return 0
    _D_in1[args] = D_in1(n - 2, d + 2) + D_in(n - 2, d - 1) + D_out1(n - 1, d - 1) + 2 * D_out1(n - 2, d)
    for i in range(n - 1):
        for j in range(d - 1):
            _D_in1[args] += 2 * Q1(i, j) * D_in(n - 2 - i, d - 2 - j)
            _D_in1[args] += 2 * S(i, j) * D_in1(n - 2 - i, d - 2 - j)
    return _D_in1[args]


_D_in2 = {}


# Maps on the disk with n darts, root of degree d lying in the interior, and a distinguished degree 2 vertex
def D_in2(*args):
    if args in _D_in2:
        return _D_in2[args]
    n, d = args
    if not 0 < d <= n:
        return 0
    _D_in2[args] = D_in2(n - 2, d + 2) + D_in(n - 2, d) + D_out2(n - 1, d - 1) + 2 * D_out2(n - 2, d)
    for i in range(n - 1):
        for j in range(d - 1):
            _D_in2[args] += (i - 2) * S(i - 2, j) * D_in(n - 2 - i, d - 2 - j)
            _D_in2[args] += 2 * S(i, j) * D_in2(n - 2 - i, d - 2 - j)
    return _D_in2[args]


_D_out_bp = {}


# Maps on the disk with n darts, root of degree d lying on the boundary, and one branch point in a face.
# Root dart is the leftmost dart incident to its vertex.
def D_out_bp(*args):
    if args in _D_out_bp:
        return _D_out_bp[args]
    n, d = args
    if not 0 < d <= n:
        return 0
    _D_out_bp[args] = D_out_bp(n - 2, d + 2) + D_out_bp(n - 1, d - 1) + D_out_bp(n - 2, d)
    for i in range(n - 1):
        _D_out_bp[args] += D_out_bp(i, 1) * D_out(n - i - 2, d - 1)
        _D_out_bp[args] += D_out(i, 1) * D_out_bp(n - i - 2, d - 1)
    for i in range(0, n - 1, 2):
        for j in range(d - 1):
            if i % 4 != j % 4:
                continue
            _D_out_bp[args] += S(i, j) * D_out_bp(n - 2 - i, d - 2 - j)
            _D_out_bp[args] += (1 + (i + j) // 4) * S(i, j) * D_out(n - 2 - i, d - 2 - j)
    return _D_out_bp[args]


_D_out_bp2 = {}


# Maps on the disk with n darts, root of degree d lying on the boundary, and two branch point in faces.
# Root darts is the leftmost dart incident to its vertex.
def D_out_bp2(*args):
    if args in _D_out_bp2:
        return _D_out_bp2[args]
    n, d = args
    if not 0 < d <= n:
        return 0
    _D_out_bp2[args] = D_out_bp2(n - 2, d + 2) + D_out_bp2(n - 1, d - 1) + D_out_bp2(n - 2, d)
    for i in range(n - 1):
        _D_out_bp2[args] += D_out_bp2(i, 1) * D_out(n - i - 2, d - 1)
        _D_out_bp2[args] += D_out(i, 1) * D_out_bp2(n - i - 2, d - 1)
        _D_out_bp2[args] += D_out_bp(i, 1) * D_out_bp(n - i - 2, d - 1)
    for i in range(0, n - 1, 2):
        for j in range(d - 1):
            if i % 4 != j % 4:
                continue
            _D_out_bp2[args] += S(i, j) * D_out_bp2(n - 2 - i, d - 2 - j)
            _D_out_bp2[args] += S_faces(i, j) * S(i, j) * D_out_bp(n - 2 - i, d - 2 - j)
            _D_out_bp2[args] += S_faces(i, j) * (S_faces(i, j) - 1) // 2 * S(i, j) * D_out(n - 2 - i, d - 2 - j)
    return _D_out_bp2[args]


_D_in_bp = {}


# Maps on the disk with n darts, root of degree d lying in the interior, and one branch point in a face.
def D_in_bp(*args):
    if args in _D_in_bp:
        return _D_in_bp[args]
    n, d = args
    if not 0 < d <= n:
        return 0
    _D_in_bp[args] = D_in_bp(n - 2, d + 2) + D_out_bp(n - 1, d - 1) + 2 * D_out_bp(n - 2, d)
    for i in range(0, n - 1, 2):
        for j in range(d - 1):
            if i % 4 != j % 4:
                continue
            _D_in_bp[args] += 2 * S(i, j) * D_in_bp(n - 2 - i, d - 2 - j)
            _D_in_bp[args] += 2 * (1 + (i + j) // 4) * S(i, j) * D_in(n - 2 - i, d - 2 - j)
    return _D_in_bp[args]


_D_in_bp2 = {}


# Maps on the disk with n darts, root of degree d lying in the interior, and two branch point in faces.
def D_in_bp2(*args):
    if args in _D_in_bp2:
        return _D_in_bp2[args]
    n, d = args
    if not 0 < d <= n:
        return 0
    _D_in_bp2[args] = D_in_bp2(n - 2, d + 2) + D_out_bp2(n - 1, d - 1) + 2 * D_out_bp2(n - 2, d)
    for i in range(0, n - 1, 2):
        for j in range(d - 1):
            if i % 4 != j % 4:
                continue
            _D_in_bp2[args] += 2 * S(i, j) * D_in_bp2(n - 2 - i, d - 2 - j)
            _D_in_bp2[args] += 2 * S_faces(i, j) * S(i, j) * D_in_bp(n - 2 - i, d - 2 - j)
            _D_in_bp2[args] += S_faces(i, j) * (S_faces(i, j) - 1) * S(i, j) * D_in(n - 2 - i, d - 2 - j)
    return _D_in_bp2[args]


_D1 = {}

# Maps on the disk with n darts, root of degree d lying in the interior, and a distinguished boundary leaf.
def D1(*args):
    if args in _D1:
        return _D1[args]
    n, d = args
    if not 0 < d <= n:
        return 0
    _D1[args] = D1(n - 2, d + 2) + D1(n - 1, d - 1) + D1(n - 2, d) + D_out(n - 2, d - 1)
    for i in range(n - 1):
        _D1[args] += D_out(i, 1) * D1(n - i - 2, d - 1)
        _D1[args] += D1(i, 1) * D_out(n - i - 2, d - 1)
    for i in range(n - 1):
        for j in range(d - 1):
            _D1[args] += S(i, j) * D1(n - 2 - i, d - 2 - j)
    return _D1[args]


_C_out = {}


# Maps on the annulus with n darts and root of degree d lying on the boundary;
# root darts is the leftmost dart incident to its vertex.
def C_out(*args):
    if args in _C_out:
        return _C_out[args]
    n, d = args
    if not 0 < d <= n:
        return 0
    _C_out[args] = C_out(n - 2, d + 2) + C_out(n - 1, d - 1) + D1(n - 2, d - 1) + C_out(n - 2, d)
    for i in range(n - 1):
        _C_out[args] += D_out(i, 1) * C_out(n - i - 2, d - 1)
        _C_out[args] += C_out(i, 1) * D_out(n - i - 2, d - 1)
    for i in range(n - 1):
        for j in range(d - 1):
            _C_out[args] += S(i, j) * C_out(n - 2 - i, d - 2 - j)
            _C_out[args] += D_out(i, j) * D_in(n - 2 - i, d - 2 - j)
    return _C_out[args]


_C_in = {}


# Maps on the annulus with n darts and root of degree d lying in the interior.
def C_in(*args):
    if args in _C_in:
        return _C_in[args]
    n, d = args
    if not 0 < d <= n:
        return 0
    _C_in[args] = C_in(n - 2, d + 2) + C_out(n - 1, d - 1) + 2 * C_out(n - 2, d)
    for i in range(n - 1):
        for j in range(d - 1):
            _C_in[args] += 2 * S(i, j) * C_in(n - 2 - i, d - 2 - j)
            _C_in[args] += D_in(i, j) * D_in(n - 2 - i, d - 2 - j)
    return _C_in[args]


_M_out = {}


# Maps on the Möbius band with n darts and root of degree d lying on the boundary;
# root dart is the leftmost dart incident to its vertex.
def M_out(*args):
    if args in _M_out:
        return _M_out[args]
    n, d = args
    if not 0 < d <= n:
        return 0
    _M_out[args] = M_out(n - 2, d + 2) + M_out(n - 1, d - 1) + M_out(n - 2, d)
    _M_out[args] += D1(n - 2, d - 1) + (d - 1) * D_out(n - 2, d - 2)
    for i in range(n - 1):
        _M_out[args] += D_out(i, 1) * M_out(n - i - 2, d - 1)
        _M_out[args] += M_out(i, 1) * D_out(n - i - 2, d - 1)
    for i in range(n - 1):
        for j in range(d - 1):
            _M_out[args] += S(i, j) * M_out(n - 2 - i, d - 2 - j)
            _M_out[args] += D_out(i, j) * P(n - 2 - i, d - 2 - j)
    return _M_out[args]


_M_in = {}


# Maps on the Möbius band with n darts and root of degree d lying in the interior.
def M_in(*args):
    if args in _M_in:
        return _M_in[args]
    n, d = args
    if not 0 < d <= n:
        return 0
    _M_in[args] = M_in(n - 2, d + 2) + M_out(n - 1, d - 1) + 2 * M_out(n - 2, d) + (d - 1) * D_in(n - 2, d - 2)
    for i in range(n - 1):
        for j in range(d - 1):
            _M_in[args] += 2 * S(i, j) * M_in(n - 2 - i, d - 2 - j)
            _M_in[args] += 2 * D_in(i, j) * P(n - 2 - i, d - 2 - j)
    return _M_in[args]

# Maps on the annulus that lift to 4-regular maps
def C_4(n):
    s = C_in(n, 4) + 2 * C_out(n, 2)
    for k in range(1, n + 1):
        s += div(n * D_in(n - k, k), k)
        # print('c4_1', k, div(n * D_in(n - k, k), k))
    for k in range(1, n - 2):
        for l in range(1, n - k - 1):
            s += div(n * S2(n - k - l, k, l), 2 * k * l)
            # print('c4_2', k, l, div(n * S2(n - k - l, k, l), 2 * k * l))
    return s

# Maps on the Möbius band that lift to 4-regular maps
def M_4(n):
    s = M_in(n, 4) + 2 * M_out(n, 2)
    for k in range(1, n + 1):
        s += div(n * P(n - k, k), k)
        # print('m4', k, div(n * P(n - k, k), k))
    return s


def div(n, k):
    if n % k != 0:
        raise AssertionError('%s // %s' % (n, k))
    return n // k


def rel_prime(n, i):
    return not [d for d in range(2, n + 1) if n % d == 0 and i % d == 0]


def phi(n):
    return len([i for i in range(n) if rel_prime(n, i)])


# Unsensed maps on the projective plane with 2n edges.
def P_unsensed(n):
    n = 2 * n  # set n = num edges
    s = P(2 * n, 4)
    for l in range(2, 2 * n + 1):
        if (2 * n) % l:
            continue
        # ==== Projective Plane Maps ====
        if l % 2 == 1:  # F
            # e = n/l; v = n/(2l); f = 1+n/l-n/(2l)
            s += phi(l) * P(2 * n // l, 4) * (1 + n // (2 * l))
            # print('z', P(2 * n // l, 4) * (1 + n // (2 * l)))
            continue

        # ==== Disc maps, no edges along boundary ====
        if l == 4:  # V
            s += phi(l) * D_in(n // 2, 1) * (n // 2)
            # print('a', D_in(2 * n // l, 1) * (2 * n // l))
        if l == 2:  # V
            s += D_in(n, 2) * (n // 2)
            # print('b', D_in(n, 2) * (n // 2))
        if l == 2:  # E
            s += D_in(n + 1, 1) * n
            # print('c', D_in(n + 1, 1) * n)
        s += phi(l) * D_in_bp(2 * n // l, 4)  # F
        # print('d', l, D_in_bp(2 * n // l, 4))
        s += phi(l) * 2 * D_out_bp(2 * n // l, 2)  # F
        # print('e', l, 2 * D_out_bp(2 * n // l, 2))

        # ==== Disc maps, edges along boundary ====
        for i in range(1, 2 * n // l + 1):
            # e = n/l-i/2; v = n/4l-3i/8+1; f = 2+n/l-i/2

            s += phi(l) * div(S(2 * n // l - i, i) * (2 * n // l) * (1 + n // (2 * l)), i)  # F
            # s += phi(l) * div(S_bp(2 * n // l - i, i) * (2 * n // l), i)  # F

            # print('f', l, i, div(S(2 * n // l - i, i) * (2 * n // l), i))
            if l == 4:  # V
                s += phi(l) * div(Q1(n // 2 - i, i) * n, 2 * i)
                # print('g', l, i, div(Q1(2 * n // l - i, i) * (2 * n // l), i))
            if l == 2:  # V
                s += div(S(n - i - 2, i) * (n - i - 2) * n, 2 * i)
                # print('h', l, i, div(S(n - i - 2, i) * (n - i - 2) * n // l, i))
            if l == 2:  # E
                s += div(Q1(n - i + 1, i) * n, i)
                # print('i', l, i, div(Q1(n - i + 1, i) * (2 * n // l), i))

    return div(s, (4 * n))


def P_faces(*args):
    n = args[0]
    v = (n - sum(args[1:])) // 4 + len(args) - 1
    return 1 + n // 2 - v


def S_faces(*args):
    n = args[0]
    v = (n - sum(args[1:])) // 4 + len(args) - 1
    return 2 + n // 2 - v


def K_unsensed(n):
    n = 2 * n  # n = edges
    s = K(2 * n, 4)
    for l in range(2, 2 * n + 1):
        if (2 * n) % l != 0:
            continue
        if l % 2 == 0:
            s += phi(l) * C_4(2 * n // l)
        if l == 2:
            s += D_in_bp2(n, 4)  # F F
            s += 2 * D_out_bp2(n, 2)  # F F
            s += div(D_in_bp(n, 2) * n, 2)  # F V
            s += D_in_bp(n + 1, 1) * n  # F E
            s += div(D_in1(n + 2, 1) * n, 2)  # E E
            s += div(D_in2(n, 2) * n, 4)  # V V
            s += div(D_in1(n + 1, 2) * n, 2)  # E V
            for i in range(1, n + 1):
                s += div(S(n - i, i) * n * S_faces(n - i, i) * (S_faces(n - i, i) - 1), 2 * i)  # F F
                s += div(QQ(n - i + 2, i) * n, i)  # E E
                s += div(Q1(n - i - 1, i) * n * (n - i - 1), 2 * i)  # E V
                s += div(S(n - i - 4, i) * n * (n - i - 4) * (n - i - 2), 8 * i)  # V V
                s += div(Q1(n - i + 1, i) * n * S_faces(n - i + 1, i, 1), i)  # E F
                s += div(S(n - i - 2, i) * n * (n - i - 2) * S_faces(n - i - 2, i), 2 * i)  # V F
        if l % 2 == 1:
            s += phi(l) * K(2 * n // l, 4)
        if l % 4 == 2:
            s += 2 * phi(l) * K(2 * n // l, 4)
        if l % 2 == 0:
            s += phi(l) * M_4(2 * n // l)
        if l == 2:
            s += 2 * P(n, 4) * P_faces(n, 4) * (P_faces(n, 4) - 1) // 2  # F F
            s += 2 * div(P1(n + 2, 1) * n, 2)  # E E
            s += 2 * div(P(n, 2) * n * P_faces(n, 2), 2)  # V F
            s += 2 * div(P(n - 2, 2) * n * (n - 2), 8)  # V V
    return div(s, (4 * n))


def assert_(expr, want):
    got = eval(expr)
    if got != want:
        print('Assertion failed:', expr, '=', got, '!=', want)
        raise AssertionError()


assert_('K(4, 4)', 4)
assert_('QQ(4, 2)', 1)
assert_('QQ(2, 2)', 0)
assert_('QQ(9, 2)', 0)
assert_('QQ(6, 4)', 6)
assert_('P1(6, 1)', 3)
assert_('P(2, 2)', 1)
assert_('P_faces(4, 4)', 2)
assert_('S_faces(2, 2)', 2)
assert_('S_faces(4, 2, 2)', 2)
assert_('P_faces(4, 4, 2)', 2)
assert_('K(8, 4)', 68)
assert_('S2(2,1,1)', 1)
assert_('S2(22,1,1)', 10206)
assert_('S(8,4)', 9)
assert_('S2(8,4,4)', 9 * 4)
assert_('S2(10,4,2)', 9 * 8)
assert_('C_4(2)', 2)
assert_('M_in(4,4)', 6)
assert_('M_out(4,2)', 2)
assert_('M_4(4)', 12)
assert_('C_4(4)', 16)
assert_('C_in(4,4)', 2)
assert_('C_out(4,2)', 1)
assert_('K(16, 4)', 12836)
assert_('D_out(0, 0)', 1)
assert_('D_in(1, 1)', 1)
assert_('D_in(2, 2)', 1)
assert_('D_in(3, 1)', 2)
assert_('D_in(4, 2)', 6)
assert_('D_in_bp(4, 4)', 4)
assert_('D_out_bp(4, 2)', 1)
assert_('D_out_bp(5, 1)', 2)
assert_('D_out_bp(4, 4)', 7)
assert_('D_out_bp(6, 2)', 10)
assert_('Q1(22, 1)', 10206)
assert_('P_unsensed(1)', 2)
assert_('P_unsensed(2)', 6)

print('\nP')
for i in range(1, 15):
    print('%4s %18s' % (i, P_unsensed(i)))
print('\nK')
for i in range(1, 15):
    print('%4s %18s' % (i, K_unsensed(i)))
