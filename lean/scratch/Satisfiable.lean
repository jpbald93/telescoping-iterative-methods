import Telescoping

/-! Satisfiability certificates (outside the library; not imported by it).
For every theorem with hypotheses: a Lean-checked example showing those hypotheses can all be met
simultaneously by concrete values. Theorems whose conclusion is `False` assert that their hypotheses
are jointly impossible; for those we certify that every hypothesis but the last is satisfiable,
so the impossibility is not caused by a trivially inconsistent subset. -/

set_option linter.unusedVariables false
set_option linter.unnecessarySeqFocus false
set_option linter.style.longLine false

-- hypotheses of Telescoping.telescope are satisfiable
example : ∃ (x : ℕ → ℝ) (n : ℕ), True :=
  ⟨fun _ => 0, 0, trivial⟩

-- hypotheses of Telescoping.telescope_sum are satisfiable
example : ∃ (x : ℕ → ℝ) (n : ℕ), True :=
  ⟨fun _ => 0, 0, trivial⟩

-- hypotheses of Telescoping.gm_le_am are satisfiable
example : ∃ (a b : ℝ) (ha : 0 ≤ a) (hb : 0 ≤ b), True :=
  ⟨1, 1, by norm_num, by norm_num, trivial⟩

-- hypotheses of Telescoping.le_gmStep are satisfiable
example : ∃ (a b : ℝ) (hb : 0 ≤ b) (hab : b ≤ a), True :=
  ⟨1, 1, by norm_num, le_rfl, trivial⟩

-- hypotheses of Telescoping.amStep_le are satisfiable
example : ∃ (a b : ℝ) (hab : b ≤ a), True :=
  ⟨1, 1, le_rfl, trivial⟩

-- hypotheses of Telescoping.step_mem are satisfiable
example : ∃ (a b : ℝ) (ha : 0 ≤ a) (hb : 0 ≤ b) (hab : b ≤ a), True :=
  ⟨1, 1, by norm_num, by norm_num, le_rfl, trivial⟩

-- hypotheses of Telescoping.quadratic_step are satisfiable
example : ∃ (a b : ℝ) (hb : 0 < b) (hab : b ≤ a), True :=
  ⟨1, 1, by norm_num, le_rfl, trivial⟩
