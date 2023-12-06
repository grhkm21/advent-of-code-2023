⟨Split⟩ ← •Import "util.bqn"
mt ← {' 'Split 1⊑':'Split𝕩}¨•FLines"../input/in_2023_06"
Solve ← {t‿d←𝕩⋄≠(d⊸<(⊢×(t-⊢)))⊸/↕1+t}
part1 ← ×´Solve¨<˘⍉2‿∘⥊∾•ParseFloat¨¨ mt
part2 ← Solve(•ParseFloat∾)¨mt

•Out •Repr part1
•Out •Repr part2
