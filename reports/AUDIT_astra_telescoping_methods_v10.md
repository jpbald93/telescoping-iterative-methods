# Telescoping methods V10 — adversarial audit (verification pass)

## Verdict (ACCEPT / MINOR REVISION / MAJOR REVISION / REJECT, one paragraph)

**MAJOR REVISION. All five V9 mathematical replacements are correct, including every entry of the parametric table.** Nevertheless, V10 is not yet a reliable verification paper: the supplied Lean development proves less than the manuscript says, the advertised independent verification drivers are absent from the supplied package, the printed symbolic derivation starts from incorrect identities, and the proof of all-n monotonicity has an unfilled gap. A new blanket rejection of geometric AGM upper bounds is false. The bibliography also contains one demonstrably wrong volume/page citation and an unverified Newman–Sofer entry whose stated pages contain different material. These findings concern substantive accuracy and reproducibility, not the correctness of the five corrected formulas. A provisional report was written after the first full read and supplemented during artifact inspection; this is the consolidated final report.

**Scope and citation convention.** I read all 472 lines of `telescoping_methods.tex`, inspected the extracted text of the accompanying PDF, read the complete generator and Lean sources, reran the generator and Lean gate, and performed independent exact/high-precision checks. Unless otherwise stated, line numbers below refer to that TeX file. Quotations spanning lines have whitespace flattened, not words changed. Actual theorem numbering in this file is 1–7: the parametric, Wallis, interval and quadratic-step results are Theorems 4–7, respectively. I identify them by name to avoid the numbering discrepancy in the assignment.

## Did the five V9 fixes land correctly?

### 1. Symmetric sequence: **PASS**

Lines 207–210 state

> `= \Bigl(\tfrac12 e - \tfrac12 e^{-1}\Bigr)\frac1{n^{2}} + \Bigl(-\tfrac{17}{12} e + \tfrac{11}{12} e^{-1}\Bigr)\frac1{n^{3}} + \Bigl(\tfrac{51}{16} e - \tfrac{23}{16} e^{-1}\Bigr)\frac1{n^{4}} + O(n^{-5}).`

All three coefficients are correct. Independently expanding the exponential by its coefficient recurrence and applying the shift gives

\[
D_n/e=\tfrac12 n^{-2}-\tfrac{17}{12}n^{-3}+\tfrac{51}{16}n^{-4}-\tfrac{9587}{1440}n^{-5}+\tfrac{3455}{256}n^{-6}+O(n^{-7}),
\]
\[
e(x_{n+1}^{-1}-x_n^{-1})=-\tfrac12n^{-2}+\tfrac{11}{12}n^{-3}-\tfrac{23}{16}n^{-4}+\tfrac{3157}{1440}n^{-5}+O(n^{-6}).
\]

Thus the leading coefficient is indeed `(e-e^{-1})/2 = 1.1752011936…`, not `e/2 = 1.3591409142…`. The sign/cancellation explanation at lines 197–200 is sound, and the e-part agrees term by term with the exponential-sequence expansion. The next coefficient at lines 219–221 is also correct: `−17.290814231707377265…`. The formal/provenance qualifications below do not invalidate this correction.

### 2. Parametric n^-2 coefficient: **PASS**

Lines 234–235 give the normalized coefficient `a^{2}b/2`. For fixed real a,b,

\[
\log x_n(a,b)=ab-\frac{a^2b}{2n}+\frac{a^3b}{3n^2}+O(n^{-3}),
\]
so
\[
x_n(a,b)/e^{ab}=1-\frac{a^2b}{2n}+\frac{a^3b/3+a^4b^2/8}{n^2}+O(n^{-3}).
\]
Differencing gives the printed leading coefficient. At a=b=1 it is 1/2 after normalization, hence e/2 before normalization. The consistency objection at lines 240–246 correctly rules out a finite coefficient proportional to a−b as a general formula. At a=0 or b=0 the sequence is constant and the genuine vanishing coefficient is appropriate; the manuscript need not promise a nonzero coefficient there.

### 3. Parametric n^-3 coefficient and Table 2: **PASS**

The displayed formula at lines 234–235 and 249–250 is correct:

\[
c_3=-a^2b(3a^2b+8a+6)/12.
\]

I checked **all six** table rows (lines 268–273), not just the two requested spot checks:

| (a,b) | c2 | c3 |
|---|---:|---:|
| (1,1) | 1/2 | −17/12 |
| (2,1) | 2 | −34/3 |
| (1,2) | 1 | −10/3 |
| (2,2) | 4 | −92/3 |
| (1/2,3) | 3/8 | −49/64 |
| (3,1/2) | 9/4 | −261/16 |

In particular `(2,1)` gives `−4(12+16+6)/12=−34/3`, and `(2,2)` gives `−8(24+16+6)/12=−92/3`. There is no recurrence of V9's wrong-table-entry failure. The normalization by e^(ab) is explicitly specified in the table heading, so this is not a missing exponential factor.

### 4. Wallis factor of pi: **PASS**

Line 287 states

> `\frac{\pi}{2} - W_N = \frac{\pi}{8N} - \frac{5\pi}{64N^{2}} + O(N^{-3}).`

Both coefficients are correct. The exact representation

\[
W_N=\frac{\pi\,\Gamma(N+1)^2}{2\Gamma(N+1/2)\Gamma(N+3/2)}
\]

also gives the next coefficient `11π/256 = 0.1349903093339364…` in the tail. Independent direct products at 200-digit precision give:

| N | π/2−W_N | two-term expression | N^3 times residual |
|---:|---:|---:|---:|
| 100 | 0.0039025814808154986058 | 0.0039024471243810712884 | 0.1343564344273174 |
| 400 | 0.0009802158301984554954 | 0.0009802137234589247458 | 0.1348313299679735 |
| 1600 | 0.0002453410852093670719 | 0.0002453410522624597442 | 0.1349505324144960 |
| 6400 | 0.0000613532399178821929 | 0.0000613532394029729709 | 0.1349803630966392 |

At N=100, `W_N=1.5668937453140811206255…`. The correction genuinely restores π, and the residual described as “near 0.135” is accurate. Calling finite observations a confirmation of an O-bound, or calling the expansion an explicit tail bound, is a separate evidential problem discussed below.

### 5. Replacement AGM inequalities: **PASS mathematically; formal coverage overstated**

The interval statement at line 313 follows directly from `b_n≤AGM≤a_n`. The quadratic-step statement at lines 318–322 and proof at lines 325–328 are correct. For `0<b≤a`, put s=√a and t=√b. Then s≥t>0, so `(s+t)^2≥4t^2=4b`, and

\[
\frac{a+b}{2}-\sqrt{ab}=\frac{(a-b)^2}{2(s+t)^2}\le\frac{(a-b)^2}{8b}.
\]

The inequality direction is right. If a>b, the numerator is positive and the denominator comparison is strict, giving strict inequality; at a=b both sides vanish. Thus the equality iff clause is also correct. The errors are the surrounding blanket assertion about geometric bounds (Should-fix 1) and the claim that the supplied Lean files formalise the full interval theorem and equality clause (Blocker 1), not these elementary mathematical arguments.

## Is the evidence-tier labelling honest?

**Partly, but not adequately in its present form.** The asymptotic headings at lines 129, 202, 230 and 283 are explicitly `[num]`. Lines 101–108 and 469–470 explicitly say these expansions are not formalised. There is no unqualified assertion that all asymptotic results are Lean theorems. The monotonicity heading at line 148 also correctly distinguishes its numerical statement from a Lean-checked base case.

However, the actual claimed Lean scope is **not limited to the AGM inequalities and D1,D2**. Lines 96–100 and 466–469 explicitly add the telescoping identity and increment sum; the latter paragraph also includes D1>D2. The sources prove finite telescoping, the small exact values/inequality, elementary one-step AGM nesting, and the quadratic inequality. They do **not** contain the infinite telescoping theorem, an iterated AGM limit/interval theorem, or the equality iff clause. This is a concrete mismatch, not speculation about the kernel.

I ran `bash gate.sh` in the supplied Lean directory. It returned **`PASS (14 theorems, standard axioms only)`**. This validates the gate's successful result for those formal statements; it does not turn related prose consequences into formal theorems. I did not independently rerun the advertised negative tests.

The numerical rhetoric also exceeds the declared weaker tier. Lines 105–107 say a next-coefficient recovery is “a check possible only if every preceding coefficient is correct”; lines 144–145 repeat “That agreement is possible only if the four displayed coefficients are exactly correct.” Finite precision and finitely many arguments cannot imply that logical necessity. For example, perturbing the n^-2 coefficient by 10^-60 changes a normalized n^6 residual at n=10^9 by only 10^-24, beneath a fifteen-digit check. Numerical agreement is strong evidence, not proof of exactness or an O-bound. An exact symbolic identity plus an analytic remainder argument would supply the missing proof.

The AI-use declaration (lines 375–381) is appropriately specific about drafting, computations, formalisation, direction, and author responsibility. I found no basis to allege concealed AI use. Its blanket sentence “Every mathematical statement was checked as described” (lines 378–380), however, inherits the documented verification-scope and missing-artifact problems. Revise that sentence rather than claiming the disclosure itself is inadequate.

## Blockers

### 1. The advertised formal theorems do not match the actual Lean statements

**Exact claim, lines 466–469:**

> `statements are: the telescoping identity \eqref{eq:telescope} and the increment sum $\sum_{k<n}(x_{k+1}-x_k) = x_n - x_1$; the exact values $D_1 = 1/4$, $D_2 = 13/108$ and the inequality $D_1 > D_2$; and the two AGM inequalities, Theorems~\ref{thm:agm-interval} and~\ref{thm:agm-step}.`

**Actual source:**
- `lean/Telescoping/Basic.lean`, lines 38–54, proves `x n = x 0 + ∑ k ∈ Finset.range n, (x (k + 1) - x k)` and its rearrangement. These are finite, zero-based identities. Neither theorem mentions a limit, summability, or an infinite sum.
- Lines 140–142 prove `b ≤ gmStep a b ∧ gmStep a b ≤ amStep a b ∧ amStep a b ≤ a`. This is one-step interval nesting, not the theorem about `a_n−AGM(a_1,b_1)` for every n. The file contains no definition of an AGM sequence/limit to which such a theorem could refer.
- Lines 150–151 state the quadratic inequality, with no equality-characterisation theorem elsewhere in the complete source.

**Required correction:** Formalise the missing conclusions, or explicitly label them as elementary consequences proved in text of the precise Lean lemmas. The interval theorem's current `[Lean]` label, the universal finitary/algebraic claims in the abstract, and Appendix D must agree with the objects actually checked. Keep the valid formal work; narrow its advertised scope.

### 2. Claimed complete computational record is incomplete, and its description is inaccurate

**Exact claim, lines 382–386:**

> `The generating program (Appendix~\ref{app:code}), the verification program (Appendix~\ref{app:num}), and the Lean~4 development (Appendix~\ref{app:lean}) are the complete computational record; running them regenerates every numeral and re-checks every kernel-verified statement.`

**Exact claim, lines 451–454:**

> `Increasing the working precision from $400$ to $2000$ digits leaves the results unchanged, so the residual is limited by truncation in $n$, not by rounding. The driver is \texttt{verify.py} / \texttt{deep.py} in the accompanying package.`

Neither named driver is present in V10 or anywhere in the supplied `inbox/telescoping-iterative-methods` tree. Appendix C describes them but does not reproduce them. The available `make_tables.py` sets `mp.dps = 60` (line 13); it performs symbolic coefficient derivation, small-n differences, Wallis products and AGM rows, not the advertised 200/400/2000-digit residual experiment. Its output is reproducible: my rerun agrees exactly with `tables_output.txt`. But that output does not contain the six-row parametric coefficient table or its six independent numerical checks; its only printed parameter specialization is a=b=1 (`make_tables.py`, lines 105–110).

Moreover lines 436–438 claim “exact rational arithmetic for $D_n$ via \texttt{fractions}”. The generator imports mpmath and sympy, not fractions (lines 10–13), and computes D(n) in mpmath (lines 69–74). Its exact symbolic coefficients are legitimate; this is a description/provenance error, not evidence of wrong displayed coefficients.

**Required correction:** Supply the named drivers, commands, precision settings and outputs, and either emit all table rows from code or narrow the all-numerals claim. A reviewer independently recovering the advertised limits does not substantiate that the author's claimed independent computation was included or run.

### 3. Appendix A's derivation starts from false equalities

**Exact text, lines 424–425:**

> `Writing $u = 1/n$ and $L(u) = u^{-1}\ln(1+u) = 1 - \tfrac{u}{2} + \tfrac{u^2}{3} - \cdots$, we have $x_n = \exp(nL(u)) = e\exp(e_1 u + e_2 u^2 + \cdots)$`

With this definition the correct expression is `x_n=exp(L(u))`, not `exp(nL(u))`. The printed middle expression grows roughly like e^n and cannot equal either adjacent expression.

**Exact text, line 428:** `\ln x_n(a,b) = bnL(a u)`.

The correct expression is `ab L(au)`, defining L(0)=1 continuously if needed; alternatively use `b log(1+au)/u`, which works directly at a=0. The generator uses the correct latter expression (`make_tables.py`, lines 21–22), explaining why the coefficients survived the incorrect written derivation.

**Required correction:** Fix both identities and give a Taylor/remainder justification. These are easy repairs, but they occur precisely where the manuscript directs readers for its mathematical derivation.

### 4. The all-n monotonicity proof is incomplete

**Exact text, lines 159–164:**

> `Monotonicity for all $n$ follows from strict concavity of $t\mapsto t\ln(1+1/t)$ together with the ratio $D_n/D_{n+1} = 1 + 2/n + O(n^{-2}) > 1$ from \eqref{eq:e-expansion} for large $n$, and direct evaluation on the finite remaining range; we state the result at the \textsf{[num]} tier because the large-$n$ half rests on the (computationally, not kernel-, verified) expansion.`

There is no specified threshold, no remainder constant yielding one, and no record of checking a complete remaining range. The included code prints six differences and ratios. Even a valid qualitative asymptotic establishes only eventual monotonicity; it cannot identify a finite range that a given computation has exhausted. Concavity of log x(t) by itself does not establish concavity of x(t), because exponentiation does not preserve concavity.

The statement is true and has a short analytic repair. Let `g(t)=t log(1+1/t)` and `f(t)=exp(g(t))`. For t≥1,

\[
0<g'(t)=\log(1+1/t)-\frac1{t+1}<\frac1{t(t+1)},\qquad g''(t)=-\frac1{t(t+1)^2}.
\]

Consequently `(g')² < 1/[t²(t+1)²] ≤ −g''`, hence `f''=f((g')²+g'')<0`. Strict concavity of **f**, now actually proved, gives decreasing increments for every integer n≥1. Replace the computational argument with this proof or an appropriate verified citation. The existing label honestly limits the formal base case but does not repair the claimed universal proof.

## Should-fix

### 1. Correct the new false generalisation about geometric AGM bounds

**Exact text, lines 305–307:**

> `The convergence is quadratic, so a geometric bound of the form $C\cdot 4^{-N}$ cannot describe it: such a bound is simultaneously violated for small $N$ and enormously slack for large $N$.`

Quadratic convergence makes a geometric upper bound non-sharp; it does not make it false for arbitrary C. A concrete counterexample to this blanket statement is `(a_1,b_1)=(1,1/2)`. Writing δ_n=a_n−b_n, the manuscript's own correct step inequality gives `δ_{n+1}≤δ_n²/4≤δ_n/8`, since b_n≥1/2 and δ_n≤1/2. Therefore

\[
0\le a_n-\mathrm{AGM}\le\tfrac12\,8^{-(n-1)}\le2\,4^{-n}\quad(n\ge1).
\]

Thus C=2 is a valid bound at every n. Say instead that the **particular V9 constant** fails for small n and that geometric bounds do not express the true quadratic rate. The phrase “linear-in-$N$ geometric bound” at line 329 is also misleading: 4^-N is exponential in N.

### 2. Do not promise explicit error bounds that are only unspecified asymptotics

**Exact abstract claims:** “explicit, checkable error control” (line 44) and “For the Wallis and AGM sequences we record sharp elementary tail bounds” (lines 49–50). Lines 77–78 and 356–358 similarly promise explicit truncation error from higher-order asymptotics.

For Wallis, the only theorem is an expansion with an unspecified O(N^-3) remainder, not an explicit inequality with a computable constant and validity threshold. The other non-AGM expansions likewise give no explicit remainder constants. The finite residual observations at lines 293–295 cannot establish a uniform O-bound. The abstract's “for each” also overstates the content: the Wallis section discusses tails, and the AGM section gives inequalities, not asymptotic expansions of their successive differences. Narrow these promises or add actual bounds. The AGM interval/step inequalities themselves are explicit and valid.

### 3. Repair the bibliography on verified evidence

- **Chen–Paris, lines 404–406:** the manuscript gives `Appl. Math. Comput. 294 (2017), 24–36`. The exact-title Crossref record gives **293 (2017), 30–39**, DOI **10.1016/j.amc.2016.08.003**. This is a definite metadata error. The paper is relevant: its abstract expressly includes asymptotic expansions for the Wallis sequence. Sources: [Crossref record](https://api.crossref.org/works/10.1016%2Fj.amc.2016.08.003), [arXiv 1511.09217](https://arxiv.org/abs/1511.09217).
- **Newman–Sofer, lines 415–416:** the exact entry is `D.~J. Newman and T.~Sofer, ... A note on the sequence $(1+1/n)^n$, College Math. J. 21 (1990), no. 5, 415–417`. I could not authenticate it, and there is **positive contrary evidence for its stated location**: the issue contents assign pp. 415–419 to *Classroom Computer Capsules*, while the JSTOR issue lists *Bernoulli Trials and the Central Limit Theorem* on pp. 415–416. Verify a genuine source/DOI or remove the entry. This is not merely a claim based on a failed search, and I do not conclude that no such note could exist elsewhere. Sources: [issue contents](https://www.jstor.org/stable/i326549), [Utah journal bibliography, vol. 21 no. 5](https://ftp.math.utah.edu/pub/tex/bib/toc/collegemathj.html#21(5):November:1990), DOI for the capsules collection **10.1080/07468342.1990.11973347**.
- After whitespace flattening, the **only** citation command in the entire source is `\cite{ChenQi,ChenParis,QiMortici}` at line 298. Both Borwein entries, Brent, Salamin and Newman–Sofer are listed but not cited in the text. Add relevant citations where their results are used or describe them explicitly as further reading. The authentic AGM references are appropriate background, but currently are not integrated into the exposition.

I found no substantiated problem with the Chen–Qi or Qi–Mortici metadata or their relevance. The Borwein SIAM article and Salamin article are authentic and relevant. Brent's institutional record supports the manuscript's 323–347 pagination, although arXiv displays 323–348; I do **not** flag the manuscript's Brent pagination as an error. The classical-result disclaimer at lines 81–86 and the explicit Wallis disclaimer at lines 296–298 are consistent with the rest of the paper; calling coefficient lists contributions does not by itself establish an illicit priority claim.

### 4. Describe the residual experiment accurately, without overstating what it proves

Lines 142–145 say that subtracting the displayed terms and multiplying by n^6 recovers 3455/256 to fifteen digits at n=10^9. That is the limit for **D_n/e**, not unnormalised D_n; it also requires the Richardson extrapolation explained in Appendix C. Independently at 200 digits I obtain:

| Residual | Raw value | First Richardson value `2R(2n)−R(n)` | Exact next coefficient |
|---|---:|---:|---:|
| D_n/e, n=10^9 | 13.496093722987547590… | 13.496093749999999973… | 13.49609375 |
| symmetric, n=10^8 | −17.290813877157666167… | −17.290814231707373689… | −17.290814231707377265… |

The advertised precision is plausible **for the extrapolated quantities**: errors are about 2.69×10^-17 and 3.58×10^-15. Appendix C does disclose Richardson extrapolation, so I do not call the precision claims disproved. Make the local descriptions explicitly say “normalised, Richardson-extrapolated residual,” and replace the “possible only if ... exactly correct” language by “strong numerical evidence consistent with the exact symbolic coefficients.”

## Nits

1. **Finite-sum indexing.** Line 75 says “partial sums collapse to $x_{N}-x_1$.” If the sum is from n=1 through N, it is `x_{N+1}−x_1`; if the intended endpoint is N−1, specify it. Likewise line 467's `\sum_{k<n}` needs the lower limit k=1. The actual Lean finite sum is zero-based and ends at n−1, with result x_n−x_0. The infinite identity remains correct.
2. **AGM table caption counts the code's examples rather than the printed table.** Lines 335–336 say “for three initialisations,” but lines 343–348 contain only two, `(1,1/2)` and `(2,1)`. The generator also computes `(1,0.9)`, explaining the likely source of the mismatch. Change “three” to “two” or include that block.
3. **Precision floor in the generator's unused third AGM example.** `tables_output.txt` ends with `(1,0.9), n=6` having gap about 5.06×10^-60 and ratio 0.50769231 at 60-digit precision. That is a rounding-floor artifact, not a failure of the 1/2 limiting ratio and not an error in the manuscript's displayed rows. Stop before that floor or increase precision when emitting it as evidence. Checking only `ab == 0` (`make_tables.py`, lines 135–136) does not catch the near-floor case.

## What I checked and found sound

- All five requested V9 formula corrections, every displayed rational parametric coefficient, and the next e/symmetric coefficients check out independently.
- For the independent exact computation, I used rational arithmetic and the exponential-series recurrence `c_0=1`, `c_m=(1/m)∑_{j=1}^m jℓ_j c_{m−j}`, with `ℓ_j=b(−1)^j a^{j+1}/(j+1)`, then the exact shift coefficient identity `d_m=∑_{k=1}^{m−1}c_k(−1)^{m−k} binom(m−1,m−k)`. This was not a call to the manuscript's symbolic routine.
- The supplied generator runs successfully and reproduces its stored output exactly. Its first six differences and ratios agree with Table 1 at the printed precision. Both printed AGM initialisations and their displayed errors/ratios agree with high-precision AGM values; the factor-of-two scaling between the initialisations is correct.
- The actual Lean gate passes for its 14 audited statements. Exact D1=1/4, D2=13/108, D1>D2, finite telescoping and the one-step quadratic inequality are genuinely represented in the formal source. The criticism is scope correspondence, not evidence of a failed build or extra axioms.
- The telescoping infinite identity is mathematically valid without absolute convergence: its finite partial sums converge by telescoping. The ordinary AGM interval argument and quadratic-step proof, including the equality condition, are sound.
- The positivity restriction for the real parametric power is stated before use. For each fixed real a,b there is an appropriate starting index; the asymptotic formulas need no uniform-in-parameter interpretation. I found no serious undefined-notation issue beyond the finite-sum indexing noted above.
- The novel/contribution rhetoric is limited by explicit classical-result disclaimers; I did not find a substantiated claim to have discovered the telescoping identity, Wallis expansion, or AGM.
- The AI-use declaration names the substantial roles actually under discussion. Its verification assurance needs correction, but there is no evidential basis here for a claim of undisclosed AI involvement.

**Bottom line:** retain all five corrected mathematical replacements. Repair the derivation and monotonicity proof, narrow or complete the formal claims, supply the absent verification artifacts, remove the new geometric-bound overclaim, and correct the cited sources before acceptance.
