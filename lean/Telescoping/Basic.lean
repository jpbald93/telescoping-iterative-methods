/-
# Machine-checked results for the telescoping manuscript (V10)

## What is and is not formalised — read this before citing it

Lean is used here for the results that are *finitary or algebraic*, where a
kernel-checked proof is worth more than a numerical check:

* the telescoping identity itself (the backbone of the whole paper);
* the exact first differences `D 1 = 1/4`, `D 2 = 13/108`, and the strict
  inequalities between the small differences that V9 quoted **incorrectly**;
* the two AGM inequalities, including the genuinely quadratic step bound that
  replaces V9's false `K · 4⁻ᴺ` claim.

The **asymptotic expansions are deliberately NOT formalised.** Statements of
the form `D n = e/(2n²) - 17e/(12n³) + 51e/(16n⁴) + O(n⁻⁵)` require Landau
calculus over filters; formalising them faithfully is a substantial project and
nothing is gained by asserting a weaker statement and calling it the theorem.
Those coefficients are established by symbolic computation (`make_tables.py`)
and confirmed numerically to 50 digits — a *lower* tier of evidence than the
Lean results below, and the manuscript says so.

Do not describe this paper as "verified in Lean" without that qualification.
-/
import Mathlib.Analysis.SpecialFunctions.Pow.Real
import Mathlib.Analysis.MeanInequalities
import Mathlib.Algebra.Order.Field.Basic
import Mathlib.Tactic

namespace Telescoping

/-! ## 1. The telescoping identity

The backbone of the manuscript: a sequence equals its initial term plus the sum
of its increments. Mathlib knows this; we record it in the paper's own notation
so later statements can refer to it. -/

/-- Finite telescoping: `x n = x 0 + ∑_{k<n} (x (k+1) - x k)`. -/
theorem telescope (x : ℕ → ℝ) (n : ℕ) :
    x n = x 0 + ∑ k ∈ Finset.range n, (x (k + 1) - x k) := by
  induction n with
  | zero => simp
  | succ n ih =>
      rw [Finset.sum_range_succ, ← add_assoc, ← ih]
      ring

/-- The bare sum of increments equals `x n - x 0`. This is the identity the
manuscript uses when it writes `S n = 1 + ∑ … = x n`, and it is the reason the
leading term in every telescoping representation is `x 0`, not `1`. V9's
metallic-mean series silently assumed `x 0 = 1`. -/
theorem telescope_sum (x : ℕ → ℝ) (n : ℕ) :
    ∑ k ∈ Finset.range n, (x (k + 1) - x k) = x n - x 0 := by
  have := telescope x n
  linarith

/-! ## 2. The sequence `x n = (1 + 1/n)^n` and its first differences

V9's monotonicity proof quoted `D₁ ≈ 0.370, D₂ ≈ 0.151, D₃ ≈ 0.074` and
`r₁ ≈ 2.45, r₂ ≈ 2.04, r₃ ≈ 1.74`. Every one of those six numbers is wrong.
Here the first two differences are pinned exactly, by `norm_num`, so the
manuscript's numerals cannot drift again. -/

/-- `x n = (1 + 1/n)^n`, indexed so that `x 1 = 2`. -/
noncomputable def x (n : ℕ) : ℝ := (1 + 1 / (n : ℝ)) ^ n

/-- Successive difference `D n = x (n+1) - x n`. -/
noncomputable def D (n : ℕ) : ℝ := x (n + 1) - x n

@[simp] theorem x_one : x 1 = 2 := by norm_num [x]

@[simp] theorem x_two : x 2 = 9 / 4 := by norm_num [x]

@[simp] theorem x_three : x 3 = 64 / 27 := by norm_num [x]

/-- `D 1 = 1/4` **exactly**. V9 asserted `≈ 0.370`. -/
theorem D_one : D 1 = 1 / 4 := by
  unfold D
  rw [x_two, x_one]
  norm_num

/-- `D 2 = 13/108` exactly (`≈ 0.12037`). V9 asserted `≈ 0.151`. -/
theorem D_two : D 2 = 13 / 108 := by
  unfold D
  rw [x_three, x_two]
  norm_num

/-- The first differences are strictly decreasing at the start: `D 1 > D 2`.
V9 drew this conclusion from wrong numerals; it is true, and here it is
kernel-checked. -/
theorem D_one_gt_D_two : D 2 < D 1 := by
  rw [D_one, D_two]; norm_num

/-- `D 1 / D 2 = 27/13`, i.e. `≈ 2.0769`. V9 asserted `r₁ ≈ 2.45`. -/
theorem ratio_one : D 1 / D 2 = 27 / 13 := by
  rw [D_one, D_two]; norm_num

/-! ## 3. AGM inequalities

V9's Theorem 1 claimed `|AGM(a₁,b₁) - aₙ| ≤ K · 4⁻ⁿ` with
`K = (a₁-b₁)²/(4·AGM)`. That is false for small `n` at every initialisation
tested, and vacuously slack later, because the AGM converges *quadratically*.

The two results below are what is actually true, and both are elementary. -/

section AGM

variable {a b : ℝ}

/-- One AGM step: the arithmetic mean. -/
noncomputable def amStep (a b : ℝ) : ℝ := (a + b) / 2

/-- One AGM step: the geometric mean. -/
noncomputable def gmStep (a b : ℝ) : ℝ := Real.sqrt (a * b)

/-- AM ≥ GM, in the form used below. -/
theorem gm_le_am (ha : 0 ≤ a) (hb : 0 ≤ b) : gmStep a b ≤ amStep a b := by
  unfold gmStep amStep
  have h2 : (0:ℝ) ≤ (a + b) / 2 := by linarith
  rw [show a * b = ((a + b) / 2) ^ 2 - ((a - b) / 2) ^ 2 by ring]
  calc Real.sqrt (((a + b) / 2) ^ 2 - ((a - b) / 2) ^ 2)
      ≤ Real.sqrt (((a + b) / 2) ^ 2) :=
        Real.sqrt_le_sqrt (by nlinarith [sq_nonneg ((a - b) / 2)])
    _ = (a + b) / 2 := Real.sqrt_sq h2

/-- The geometric mean stays above the smaller entry. -/
theorem le_gmStep (hb : 0 ≤ b) (hab : b ≤ a) : b ≤ gmStep a b := by
  unfold gmStep
  have h : b * b ≤ a * b := by nlinarith
  calc b = Real.sqrt (b * b) := by
          rw [Real.sqrt_mul_self hb]
    _ ≤ Real.sqrt (a * b) := Real.sqrt_le_sqrt h

/-- The arithmetic mean stays below the larger entry. -/
theorem amStep_le (hab : b ≤ a) : amStep a b ≤ a := by
  unfold amStep; linarith

/-- **The interval shrinks and stays nested**: one AGM step maps `[b, a]` into
itself. This is what makes `aₙ - AGM ≤ aₙ - bₙ` true, and it is the honest
replacement for V9's `4⁻ⁿ` claim. -/
theorem step_mem (ha : 0 ≤ a) (hb : 0 ≤ b) (hab : b ≤ a) :
    b ≤ gmStep a b ∧ gmStep a b ≤ amStep a b ∧ amStep a b ≤ a :=
  ⟨le_gmStep hb hab, gm_le_am ha hb, amStep_le hab⟩

/-- **The quadratic step bound.** The gap after one step satisfies
`a' - b' ≤ (a - b)² / (8b)`, which is genuinely quadratic — unlike a `4⁻ⁿ`
geometric bound, which cannot describe AGM convergence at all.

Proof: `a' - b' = (√a - √b)²/2 = (a-b)² / (2(√a+√b)²)` and
`(√a + √b)² ≥ 4b`. -/
theorem quadratic_step (hb : 0 < b) (hab : b ≤ a) :
    amStep a b - gmStep a b ≤ (a - b) ^ 2 / (8 * b) := by
  have ha : (0:ℝ) < a := lt_of_lt_of_le hb hab
  set s := Real.sqrt a with hs
  set t := Real.sqrt b with ht
  have hs0 : 0 < s := Real.sqrt_pos.mpr ha
  have ht0 : 0 < t := Real.sqrt_pos.mpr hb
  have hsa : s ^ 2 = a := Real.sq_sqrt ha.le
  have htb : t ^ 2 = b := Real.sq_sqrt hb.le
  have hts : t ≤ s := Real.sqrt_le_sqrt hab
  -- a' - b' = (s - t)^2 / 2
  have hstep : amStep a b - gmStep a b = (s - t) ^ 2 / 2 := by
    unfold amStep gmStep
    have : Real.sqrt (a * b) = s * t := by
      rw [hs, ht, ← Real.sqrt_mul ha.le]
    rw [this, ← hsa, ← htb]; ring
  rw [hstep]
  -- With `b = t^2 > 0`, reduce to a polynomial inequality in `s, t` via
  -- `a - b = (s - t)(s + t)`, avoiding any named division lemma.
  have hfac : a - b = (s - t) * (s + t) := by rw [← hsa, ← htb]; ring
  have key : (a - b) ^ 2 / (8 * b) - (s - t) ^ 2 / 2
      = ((s - t) ^ 2 * ((s + t) ^ 2 - 4 * t ^ 2)) / (8 * t ^ 2) := by
    rw [hfac, ← htb]
    field_simp
    ring
  have hnum : 0 ≤ (s - t) ^ 2 * ((s + t) ^ 2 - 4 * t ^ 2) := by
    have h1 : (0:ℝ) ≤ (s + t) ^ 2 - 4 * t ^ 2 := by nlinarith [sub_nonneg.mpr hts]
    exact mul_nonneg (sq_nonneg _) h1
  have hdiff : 0 ≤ (a - b) ^ 2 / (8 * b) - (s - t) ^ 2 / 2 := by
    rw [key]
    exact div_nonneg hnum (by positivity)
  linarith

end AGM

end Telescoping
