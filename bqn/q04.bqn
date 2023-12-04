input ← >•FLines"../input/in_2023_04"
ScoreLine ← {
  tmp ← 2↓(∨`':'⊸=¨)⊸/𝕩
  right‿left ← •ParseFloat¨¨(0<≠)¨⊸/¨" |"⊸((⊢-˜¬×·+`»⊸<)∘∊˜⊔⊢)¨⊏⟜tmp⌾∾⊔⊏⍉∾(∧`'|'⊸≠¨)⊸((1‿2⥊∾)¨)tmp
  right ↩ (∊⟜left)⊸/right
  (⌊2⋆-⟜1)⊸⋈≠right
}

Iter ← {
  tot‿cnts‿matches←𝕩
  (c0‿c1)‿(m0‿m1)←1⊸((⊑↑)⋈↓)¨⟨cnts, matches⟩
  (tot+c0)‿(c1+(≠c1)↑m0⥊c0)‿m1
}

mt1‿mt2 ← <˘⍉ScoreLine˘input
part1 ← +´mt1
part2 ← ⊑Iter⍟(≠mt2) 0∾(≠⊸⥊⟜1⊸⋈ mt2)

•Out •Repr part1
•Out •Repr part2
