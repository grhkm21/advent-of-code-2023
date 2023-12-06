⟨Split⟩ ← •Import "util.bqn"
mt ← •FLines"../input/in_2023_01"
names ← (⋈¨'0'+↕10)∾"zero"‿"one"‿"two"‿"three"‿"four"‿"five"‿"six"‿"seven"‿"eight"‿"nine"

SolveLine ← •ParseFloat∘∾○⊑⟜⌽('0'⊸≤∧≤⟜'9')⊸/
•Show +´SolveLine¨mt
•Show +´{SolveLine∾{⊑¨(1⊸⊑)¨⊸/𝕩}¨<˘⍉names{⟨'0'+10|⊑names⊐<𝕨,𝕨≡(≠𝕨)↑𝕩⟩}⌜↓𝕩}¨mt
