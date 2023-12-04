⟨Split⟩ ← •Import "util.bqn"
mt ← {•ParseFloat¨¨ ' 'Split¨'|'Split 1⊑':'Split𝕩}¨•FLines"in"

# TODO: Replace this with a Fold
Iter ← {
  tot‿cnts‿matches←𝕩
  (c0‿c1)‿(m0‿m1)←1⊸((⊑↑)⋈↓)¨⟨cnts, matches⟩
  (tot+c0)‿(c1+(≠c1)↑m0⥊c0)‿m1
}

part1 ← +´⌊2⋆1-˜(+´∊˜´)¨mt
part2 ← ⊑Iter⍟(≠mt) 0∾(≠⊸⥊⟜1⊸⋈(+´∊˜´)¨mt)
