digits ← "0123456789"
input ← ∾⟜'.'˘>•FLines"../input/in_2023_03"
n‿m ← ≢input
dpos ← (∊⟜digits)∘⊑⟜input⊸/⥊(↕n)∾⌜↕m
syms ← (¬∊⟜(digits∾'.'))∘⊑⟜input⊸/⥊(↕n)∾⌜↕m
muls ← ('*'=⊑⟜input)⊸/⥊(↕n)∾⌜↕m
nums ← (0≠≠)¨⊸/(digits(¬∘∊˜/⊢)@+↕256)((⊢-˜¬×·+`»⊸<)∘∊˜⊔⊢)⥊input

mask1 ← ∨˝⍉dpos((1⊸≥)∘⌈´(|-))⌜syms
pack1 ← (∘‿2⊸⥊∾)¨(mask1⋈¨⊢)⌾∾nums
part1 ← +´(•ParseFloat 1⊏⍉)¨(⊑∘(∨˝)∘⊏⍉)¨⊸/pack1

# TODO: Try ≍
# TODO: Fix WA for 123 .*. 123

mask2 ← ⥊⊐⟜⟨1⟩˘⌾⍉ muls ((1⊸≥)∘⌈´(|-))⌜ dpos
pack2 ← (∘‿2⊸⥊∾)¨(mask2⋈¨⊢)⌾∾nums
part2 ← +´(×´(•ParseFloat 1⊏⍉)¨)¨(1⊸<≠)¨⊸/⊏⟜pack2⌾∾(1⊸↓⌾⌽)⊔(⊑∘(⌊˝)∘⊏⍉)¨pack2
(1⊸↓⌾⌽)⊔(⊑∘(⌊˝)∘⊏⍉)¨pack2
⊏⟜pack2⌾∾(1⊸↓⌾⌽)⊔(⊑∘(⌊˝)∘⊏⍉)¨pack2

•Out •Repr part1
•Out •Repr part2
