⟨Split⟩ ← •Import "util.bqn"
mt ← {' 'Split 1⊑':'Split𝕩}¨•FLines"../input/in_2023_06"
Solve ← {t‿d←𝕩⋄≠(d⊸<(⊢×(t-⊢)))⊸/↕1+t}
×´Solve¨<˘⍉2‿∘⥊∾•ParseFloat¨¨ mt
Solve(•ParseFloat∾)¨mt
