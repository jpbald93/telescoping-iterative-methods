#!/usr/bin/env python3
"""All numerical values quoted in the V10 manuscript are produced here.

Rationale: V9 quoted six numerals inside the monotonicity proof that were
wrong (D_1 = 0.370 when D_1 = 1/4 exactly), and asserted asymptotic
coefficients that had not been recomputed.  Nothing in V10 is typed by hand.

Run:  python3 make_tables.py
"""
from mpmath import mp, mpf, sqrt, pi, exp
import sympy as sp

mp.dps = 60

# ----------------------------------------------------------------- symbolic
u, a, b = sp.symbols('u a b')          # u = 1/n


def norm_series(a_, b_, N=6):
    """Series in u of x_n(a,b)/exp(ab) where x_n = (1 + a/n)^(bn)."""
    lg = sum((-1) ** (k + 1) * (a_ * u) ** k / k for k in range(1, N + 2))
    w = sp.expand(sp.series(sp.expand(b_ * lg / u - a_ * b_), u, 0, N).removeO())
    ex = sum(w ** k / sp.factorial(k) for k in range(0, N + 1))
    return sp.expand(sp.series(sp.expand(ex), u, 0, N).removeO())


def shift(S, N=6):
    """n -> n+1, i.e. u -> u/(1+u)."""
    return sp.expand(sp.series(S.subs(u, u / (1 + u)), u, 0, N).removeO())


def coeffs_e():
    """Theorem: D_n/e coefficients for x_n = (1+1/n)^n."""
    X = norm_series(1, 1)
    D = sp.expand(sp.series(shift(X) - X, u, 0, 6).removeO())
    return {k: sp.nsimplify(D.coeff(u, k)) for k in (2, 3, 4, 5)}


def coeffs_sym():
    """Theorem: coefficients of y_{n+1}-y_n for y_n = x_n + 1/x_n."""
    E = sp.E
    X = sp.expand(E * norm_series(1, 1))
    Y = sp.expand(sp.series(X + 1 / X, u, 0, 6).removeO())
    D = sp.expand(sp.series(shift(Y) - Y, u, 0, 6).removeO())
    out = {}
    # Treat e as an indeterminate t so the split into p*e + q/e is exact
    # rational arithmetic.  (sympy's nsimplify will happily invent radicals
    # for a float-contaminated coefficient, which corrupted an earlier run.)
    t = sp.Symbol('t', positive=True)
    for k in (2, 3, 4):
        c = sp.expand(D.coeff(u, k).rewrite(sp.exp))
        c_t = sp.expand(c.subs(E, t))
        poly = sp.Poly(sp.expand(c_t * t), t)
        p = sp.Rational(poly.coeff_monomial(t ** 2))
        q = sp.Rational(poly.coeff_monomial(1))
        assert sp.simplify(c - (p * E + q / E)) == 0, f"split failed at n^-{k}"
        out[k] = (p, q)
    return out


def coeffs_param():
    """Theorem: D_n(a,b)/exp(ab) coefficients, general (a,b)."""
    X = norm_series(a, b, 5)
    D = sp.expand(sp.series(shift(X, 5) - X, u, 0, 5).removeO())
    return {k: sp.factor(sp.simplify(sp.nsimplify(D.coeff(u, k)))) for k in (2, 3)}


# ---------------------------------------------------------------- numerical
def x(n):
    return (1 + mpf(1) / n) ** n


def D(n):
    return x(n + 1) - x(n)


def wallis(N):
    p = mpf(1)
    for k in range(1, N + 1):
        p *= (mpf(2 * k) ** 2) / ((2 * k - 1) * (2 * k + 1))
    return p


def agm_rows(a1, b1, N=6):
    A, B = mpf(a1), mpf(b1)
    G = mp.agm(mpf(a1), mpf(b1))
    out = []
    for n in range(1, N + 1):
        out.append((n, A, B, A - G, A - B))
        A, B = (A + B) / 2, sqrt(A * B)
    return out, G


def main():
    print("=" * 68)
    print("THEOREM (e): D_n / e  coefficients in powers of 1/n")
    for k, c in coeffs_e().items():
        print(f"   n^-{k}: {c}")

    print()
    print("THEOREM (symmetric): y_{n+1}-y_n  =  p*e + q/e  per order")
    for k, (p, q) in coeffs_sym().items():
        print(f"   n^-{k}: ({p})*e + ({q})/e")

    print()
    print("THEOREM (parametric): D_n(a,b)/exp(ab) coefficients")
    for k, c in coeffs_param().items():
        print(f"   n^-{k}: {c}")
    c3 = coeffs_param()[3]
    print(f"   check at a=b=1: {sp.nsimplify(c3.subs({a: 1, b: 1}))}  (must be -17/12)")

    print()
    print("=" * 68)
    print("TABLE: first differences D_n  (exact rationals where shown)")
    print(f"{'n':>3}  {'D_n':<24} {'r_n = D_n/D_{n+1}':<20}")
    for n in range(1, 7):
        print(f"{n:>3}  {mp.nstr(D(n), 16):<24} {mp.nstr(D(n)/D(n+1), 12):<20}")
    print(f"   D_1 exactly = (3/2)^2 - 2 = 1/4 = {mp.nstr(D(1), 12)}")

    print()
    print("TABLE: Wallis tail  pi/2 - W_N  against pi/(8N) - 5pi/(64N^2)")
    for N in (100, 400, 1600, 6400):
        t = pi / 2 - wallis(N)
        one = pi / (8 * mpf(N))
        two = one - 5 * pi / (64 * mpf(N) ** 2)
        print(f"  N={N:>5}  tail={mp.nstr(t,10):<14} pi/(8N)={mp.nstr(one,10):<14} "
              f"two-term={mp.nstr(two,10):<14} resid*N^3={mp.nstr((t-two)*mpf(N)**3,8)}")

    print()
    print("TABLE: AGM, a_n - AGM  against  a_n - b_n")
    for (a1, b1) in [(1, mpf('0.5')), (2, 1), (1, mpf('0.9'))]:
        rows, G = agm_rows(a1, b1)
        print(f"  a1={a1}, b1={b1}  (AGM={mp.nstr(G,12)})")
        for n, A, B, eG, ab in rows:
            if ab == 0:
                break
            print(f"     n={n}  a_n-AGM={mp.nstr(eG,8):<14} a_n-b_n={mp.nstr(ab,8):<14} "
                  f"ratio={mp.nstr(eG/ab,8)}")


if __name__ == "__main__":
    main()


def monotonicity_sign_check(tmax=200, steps=4000):
    """Confirm f'(t) - f'(t+1) > 0 on [1, tmax], where f(t)=(1+1/t)^t.

    Backs the all-n monotonicity claim of Section 2: D_n - D_{n+1} =
    integral_n^{n+1} (f'(t) - f'(t+1)) dt, so f' strictly decreasing gives
    strict monotonicity of the differences. f'(t) = f(t) g'(t) with
    g'(t) = ln(1+1/t) - 1/(t+1).
    """
    mp.dps = 50
    def fprime(t):
        t = mpf(t)
        f = (t * mp.log(1 + 1/t)).exp() if False else mp.e ** (t * mp.log(1 + 1/t))
        gp = mp.log(1 + 1/t) - 1/(t + 1)
        return f * gp
    worst = None
    for i in range(steps + 1):
        t = 1 + mpf(tmax - 1) * i / steps
        d = fprime(t) - fprime(t + 1)
        if worst is None or d < worst[1]:
            worst = (t, d)
    ok = worst[1] > 0
    print("monotonicity sign-check on [1,%d]: min(f'(t)-f'(t+1)) = %s at t=%.3f  -> %s"
          % (tmax, mp.nstr(worst[1], 4), float(worst[0]), "OK" if ok else "FAIL"))
    return ok
