# Telescoping Representations of Classical Iterative Methods and Constants

Reproduction package for the note *Telescoping Representations of Classical
Iterative Methods and Constants* (Josh Bald). The paper uses the elementary
telescoping identity `L = x_1 + Σ (x_{n+1} − x_n)` as a frame for the
asymptotics of the successive differences of five classical sequences:
`(1+1/n)^n → e`, its symmetric companion `x_n + 1/x_n → e + 1/e`, the parametric
family `(1+a/n)^{bn} → e^{ab}`, the Wallis product, and the
arithmetic–geometric mean (AGM).

Everything the paper claims quantitatively is reproduced here, and the finitary
and algebraic statements are additionally checked by a Lean 4 development.

## Tiers of evidence

The paper labels every quantitative claim, and this repository is organised the
same way:

- **`[Lean]` — kernel-checked.** The finite telescoping identity, the exact
  first differences `D_1 = 1/4`, `D_2 = 13/108` and `D_1 > D_2`, and the two AGM
  one-step inequalities. These are the statements proved outright, in
  `lean/`.
- **`[num]` — high-precision computation, not a proof.** The asymptotic
  coefficient lists (Theorems on `D_n`, the symmetric sequence, the parametric
  family, and Wallis). These are confirmed to high precision and large `n` by
  the scripts in `code/`, which recover the *next* unclaimed coefficient — a
  check possible only if every preceding coefficient is correct, but still a
  finite, finite-precision check, not a proof. The asymptotic expansions are
  deliberately **not** formalised in Lean.

## Layout

```
paper/    telescoping_methods.tex   the manuscript (LaTeX)
          telescoping_methods.pdf   compiled, 10 pp
code/     make_tables.py            generates every table numeral; also the
                                    monotonicity sign-check cited in the paper
          verify.py                 fixed-n asymptotic-coefficient residuals
          deep.py                   Richardson extrapolation in n → next coeff
          tables_output.txt         captured output of make_tables.py
lean/     Telescoping/Basic.lean    the kernel-checked theorems
          Telescoping/Check.lean    #print axioms audit of each theorem
          gate.sh                   build + axiom + count gate
reports/  AUDIT_astra_...v10.md     independent adversarial audit
```

## Reproduce the numerics

Pure Python standard library plus SymPy/mpmath for `make_tables.py`; `verify.py`
and `deep.py` use only `decimal` and `fractions` (no third-party dependencies).

```bash
cd code
python3 make_tables.py          # every table numeral, in exact/arbitrary precision
python3 verify.py 200           # fixed-n residuals at 200-digit precision
python3 deep.py 9 200           # Richardson extrapolation to n = 1e9 (slower)
python3 -c "import make_tables as m; m.monotonicity_sign_check()"
```

`make_tables.py` prints the coefficient lists and the tables; `D_1 = 1/4` and
`D_2 = 13/108` are produced exactly with `fractions`. `deep.py 9 200` recovers
the next `D_n/e` coefficient `3455/256 = 13.49609375` to fifteen digits at
`n = 1e9`; increasing the precision argument well past 200 leaves the result
unchanged, confirming the residual is limited by truncation in `n`, not by
rounding.

## Reproduce the Lean check

Requires the Lean toolchain pinned in `lean/lean-toolchain`
(`leanprover/lean4:v4.33.1`) and its Mathlib dependency at the revision in
`lean/lake-manifest.json`.

```bash
cd lean
lake exe cache get      # fetch the prebuilt Mathlib cache (do not skip / silence)
./gate.sh
```

`gate.sh` requires a successful build, the absence of
`sorry`/`admit`/`axiom`/`native_decide`, and that every audited theorem depend
only on a subset of Lean's three standard axioms (`propext`,
`Classical.choice`, `Quot.sound`). It also pins the number of audited theorems,
so a silently deleted `#print axioms` line fails rather than passing quietly. A
successful run prints:

```
PASS (14 theorems, standard axioms only)
```

The gate is negative-tested: injecting a `sorry`-proved lemma, or deleting an
audit line, both make it fail.

## Build the paper

```bash
cd paper
pdflatex telescoping_methods.tex   # x3 for references
```

The manuscript's code appendix includes `code/make_tables.py` verbatim via
`\lstinputlisting`, so build from the `paper/` directory with the repository
layout intact.

## Reference

`reports/AUDIT_astra_telescoping_methods_v10.md` is an independent adversarial
audit (verification pass) of this version: it confirms the corrected
coefficients and the AGM proofs, and its findings — a corrected bibliography
entry, an Appendix-A identity fix, a completed monotonicity argument, narrowed
formal-scope wording, and the inclusion of the verification drivers — have all
been applied to the files here.
