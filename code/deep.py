#!/usr/bin/env python3
"""Deep verification: drive n high enough that the residual pins the NEXT
coefficient to many digits, and Richardson-extrapolate to kill the n^-1 tail.

Precision is set generously relative to n so rounding never limits the result:
at n = 10^k the residual is ~n^-6 relative, so we need well over 7k digits.
"""
from decimal import Decimal, getcontext
from fractions import Fraction as F
import sys, json

NMAX_POW = int(sys.argv[1]) if len(sys.argv) > 1 else 9
PREC     = int(sys.argv[2]) if len(sys.argv) > 2 else 200
getcontext().prec = PREC

def x(n):
    one = Decimal(1)
    return (Decimal(n) * ((one + one / Decimal(n)).ln())).exp()

def D(n):
    return x(n + 1) - x(n)

def y(n):
    v = x(n); return v + 1 / v

def Dy(n):
    return y(n + 1) - y(n)

E = Decimal(1).exp()
COEF = [(2, F(1,2)), (3, F(-17,12)), (4, F(51,16)), (5, F(-9587,1440))]
SYMP = [(2, F(1,2)), (3, F(-17,12)), (4, F(51,16))]
SYMQ = [(2, F(-1,2)), (3, F(11,12)), (4, F(-23,16))]

def dec(fr):
    return Decimal(fr.numerator) / Decimal(fr.denominator)

def resid_e(n):
    N = Decimal(n)
    acc = sum((dec(c) / N**j for j, c in COEF), Decimal(0))
    return (D(n) / E - acc) * N**6

def resid_sym(n):
    N = Decimal(n)
    acc = Decimal(0)
    for (j, p), (_, q) in zip(SYMP, SYMQ):
        acc += (dec(p) * E + dec(q) / E) / N**j
    return (Dy(n) - acc) * N**5

def richardson(f, ns):
    """Assume f(n) = C + d/n + O(n^-2); eliminate d from consecutive decades."""
    vals = [(n, f(n)) for n in ns]
    out = []
    for (n1, v1), (n2, v2) in zip(vals, vals[1:]):
        r = Decimal(n2) / Decimal(n1)
        out.append((n2, (r * v2 - v1) / (r - 1)))
    return vals, out

def main():
    ns = [10**k for k in range(3, NMAX_POW + 1)]
    res = {"prec": PREC, "n_max": f"1e{NMAX_POW}"}

    raw, ext = richardson(resid_e, ns)
    res["D_over_e"] = {
        "target_3455_256": str(Decimal(3455)/Decimal(256)),
        "raw":        [{"n": f"1e{len(str(n))-1}", "v": str(+v)[:34]} for n, v in raw],
        "richardson": [{"n": f"1e{len(str(n))-1}", "v": str(+v)[:34]} for n, v in ext],
    }

    raw2, ext2 = richardson(resid_sym, ns[:-1])
    # predicted n^-5 coefficient of the symmetric expansion:
    #   (-9587/1440) e + (3157/1440)/e
    tgt = dec(F(-9587,1440))*E + dec(F(3157,1440))/E
    res["symmetric"] = {
        "target_-9587_1440_e_plus_3157_1440_over_e": str(+tgt)[:34],
        "raw":        [{"n": f"1e{len(str(n))-1}", "v": str(+v)[:34]} for n, v in raw2],
        "richardson": [{"n": f"1e{len(str(n))-1}", "v": str(+v)[:34]} for n, v in ext2],
    }
    print(json.dumps(res, indent=1))

if __name__ == "__main__":
    main()
