⟨Split⟩ ← •Import "util.bqn"
mt ← ∘‿2⥊∾{•ParseFloat⌾(1⊸⊑)' 'Split𝕩}¨•FLines"../input/in_2023_07"
ranking ←⟨⟨5⟩,⟨1,4⟩,⟨2,3⟩,⟨1,1,3⟩,⟨1,2,2⟩,⟨1,1,1,2⟩⟩
ordering1 ← "23456789TJQKA"
ordering2 ← "J23456789TQKA"
Key ← {-⊑ranking⊐<∧/⁼⊐𝕩}
Enum ← ⥊(<⟨⟩)<⊸∾⌜´('J'=⊢)◶⟨⊢,1↓ordering2⟩¨
•Show +´(1+↕≠mt)×¨1⊑˘(⍋({⟨Key𝕩,ordering1⊐𝕩⟩}∘⊑)˘)⊸⊏mt
•Show +´(1+↕≠mt)×¨1⊑˘(⍋({⟨⌈´Key¨Enum𝕩,ordering2⊐𝕩⟩}∘⊑)˘)⊸⊏mt
