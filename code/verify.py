#!/usr/bin/env python3
"""High-precision verification of the V10 asymptotic coefficients.

Uses only the Python standard library (decimal / fractions), because the node
has no pip.  decimal is arbitrary-precision and provides ln() and exp().

Strategy
--------
For each claimed expansion we compute the sequence EXACTLY (or to PREC digits),
subtract the claimed truncated expansion, multiply by the next power of n, and
check that the result converges to the NEXT predicted coefficient.  That tests
the claimed coefficients AND predicts the following one, which is a far
stronger check than agreeing to a few digits.
"""
from decimal import Decimal, getcontext
from fractions import Fraction
import sys, json

PREC = int(sys.argv[1]) if len(sys.argv) > 1 else 400
getcontext().prec = PREC

def E():
    return Decimal(1).exp()

def x(n):
    """(1 + 1/n)^n to full working precision."""
    one = Decimal(1)
    return (n * ((one + one / Decimal(n)).ln())).exp()

def D(n):
    return x(n + 1) - x(n)

def y(n):
    xv = x(n)
    return xv + 1 / xv

def Dy(n):
    return y(n + 1) - y(n)

def xp(n, a, b):
    """(1 + a/n)^(b n) with a, b Decimals."""
    one = Decimal(1)
    return (b * Decimal(n) * ((one + a / Decimal(n)).ln())).exp()

def Dp(n, a, b):
    return xp(n + 1, a, b) - xp(n, a, b)

def residual(val, n, coeffs, e_factor):
    """val - e_factor*sum(c_j / n^j); returns residual * n^(next power)."""
    N = Decimal(n)
    acc = Decimal(0)
    for j, c in coeffs:
        acc += Decimal(c.numerator) / Decimal(c.denominator) / N ** j
    r = val - e_factor * acc
    nxt = coeffs[-1][0] + 1
    return r / e_factor * N ** nxt

# ---- expansions
F = Fraction
EXP_E   = [(2, F(1,2)), (3, F(-17,12)), (4, F(51,16)), (5, F(-9587,1440))]
# next predicted coefficient of D_n/e  (order n^-6), from the symbolic run
NEXT_E  = F(3455,256)

SYM_P   = [(2, F(1,2)), (3, F(-17,12)), (4, F(51,16))]      # coeff of e
SYM_Q   = [(2, F(-1,2)), (3, F(11,12)), (4, F(-23,16))]     # coeff of 1/e

def run():
    out = {"precision": PREC, "tests": []}
    e = E()

    # ---- 1. D_n / e ----
    rows = []
    for n in (10**3, 10**4, 10**5, 10**6, 10**7):
        r = residual(D(n), n, EXP_E, e)
        rows.append({"n": n, "residual_x_n6": str(+r)[:40]})
    out["tests"].append({
        "name": "D_n/e = 1/2 n^-2 - 17/12 n^-3 + 51/16 n^-4 - 9587/1440 n^-5 + ...",
        "predicted_next_coeff": str(NEXT_E), "rows": rows})

    # ---- 2. symmetric y_n ----
    rows = []
    for n in (10**3, 10**4, 10**5, 10**6):
        N = Decimal(n); acc = Decimal(0)
        for (j, p), (_, q) in zip(SYM_P, SYM_Q):
            acc += (Decimal(p.numerator)/Decimal(p.denominator)*e
                    + Decimal(q.numerator)/Decimal(q.denominator)/e) / N**j
        r = (Dy(n) - acc) * N**5
        rows.append({"n": n, "residual_x_n5": str(+r)[:40]})
    out["tests"].append({
        "name": "y_{n+1}-y_n = (1/2)e+(-1/2)/e n^-2 + (-17/12)e+(11/12)/e n^-3 + (51/16)e+(-23/16)/e n^-4",
        "rows": rows})

    # ---- 3. parametric leading + n^-3 ----
    for (an, ad, bn_, bd) in [(1,1,1,1), (2,1,1,1), (1,1,2,1), (2,1,2,1), (1,2,3,1), (3,1,1,2)]:
        a = Decimal(an)/Decimal(ad); b = Decimal(bn_)/Decimal(bd)
        af = F(an, ad); bf = F(bn_, bd)
        c2 = af**2*bf/2
        c3 = -af**2*bf*(3*af**2*bf + 8*af + 6)/12
        eab = (a*b).exp()
        rows = []
        for n in (10**4, 10**5, 10**6):
            N = Decimal(n)
            acc = (Decimal(c2.numerator)/Decimal(c2.denominator)/N**2
                   + Decimal(c3.numerator)/Decimal(c3.denominator)/N**3)
            r = (Dp(n, a, b) - eab*acc)/eab * N**4
            rows.append({"n": n, "residual_x_n4": str(+r)[:34]})
        out["tests"].append({
            "name": f"D_n({af},{bf})/exp(ab): c2={c2}, c3={c3}",
            "c2": str(c2), "c3": str(c3), "rows": rows})

    print(json.dumps(out, indent=1))

if __name__ == "__main__":
    run()
