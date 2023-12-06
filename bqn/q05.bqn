# def follow(val):
#     path = []
#     for block in maps:
#         for i, rg in enumerate(block):
#             dest, src, length = list(map(int, rg.split()))
#             if src <= val < src + length:
#                 val = dest + (val - src)
#                 path.append(i)
#                 break
#         else:
#             path.append(None)
#     return val, path

⟨Split, SplitF⟩ ← •Import "util.bqn"
maps ← ⟨⟩SplitF•FLines"../input/in_2023_05"
orig ← •ParseFloat¨' 'Split⊑1↓':'Split⊑⊑maps
maps ↩ {(¯1+1⊏𝕩)⊸+⌾(2⊸⊏)𝕩}⌾⍉¨{1(⊏⎉1⍋⊸⊏⊢)∘‿3⥊∾(•ParseFloat¨)¨' 'Split¨1↓𝕩}¨1↓maps

Follow ← {
  val ← 𝕩
  {
    val_start ← val
    # Assumption: Intervals don't overlap (holds in given inputs)
    {
      dest‿src‿end ← 𝕩
      (src⊸≤∧end⊸≥) val_start ? val ↩ dest + (val - src) ; 0
    }˘𝕩
  }¨maps
  val
}

•Show ⌊´Follow¨orig
