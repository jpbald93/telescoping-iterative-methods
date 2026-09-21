/-
Axiom-dependency audit. Every theorem must depend only on a subset of Lean's
three standard axioms: propext, Classical.choice, Quot.sound.
-/
import Telescoping.Basic

#print axioms Telescoping.telescope
#print axioms Telescoping.telescope_sum
#print axioms Telescoping.x_one
#print axioms Telescoping.x_two
#print axioms Telescoping.x_three
#print axioms Telescoping.D_one
#print axioms Telescoping.D_two
#print axioms Telescoping.D_one_gt_D_two
#print axioms Telescoping.ratio_one
#print axioms Telescoping.gm_le_am
#print axioms Telescoping.le_gmStep
#print axioms Telescoping.amStep_le
#print axioms Telescoping.step_mem
#print axioms Telescoping.quadratic_step
