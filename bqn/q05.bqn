⟨Split, SplitF⟩ ← •Import "util.bqn"
maps ← ⟨⟩SplitF•FLines"../input/in_2023_05"
orig ← •ParseFloat¨' 'Split⊑1↓':'Split⊑⊑maps
maps ↩ {(¯1+1⊏𝕩)⊸+⌾(2⊸⊏)𝕩}⌾⍉¨{1(⊏⎉1⍋⊸⊏⊢)∘‿3⥊∾(•ParseFloat¨)¨' 'Split¨1↓𝕩}¨1↓maps

Follow ← {
  val ← 𝕩
  path ← ⟨⟩
  {
    val_start ← val
    added ← 0
    {
      idx‿dest‿src‿end ← 𝕩
      (¬added) ∧ (src⊸≤∧end⊸≥) val_start ?
        # val ∊ [src, end] -> map val
        val ↩ dest + (val - src)
        path ↩ path ∾ idx
        added ↩ 1
      ; 0
    }¨(↕≠𝕩)∾¨(<˘𝕩)
    # If not added, then append ≠𝕩 to path
    path ↩ path ∾ (¬added) ⥊ ≠𝕩
  }¨maps
  val⋈path
}

G ← {
  max ← 10 ⋆ 100
  BS ← {
    start‿end ← 𝕩
    mid ← ⌊(start + end) ÷ 2
    val_start‿path_start ← Follow start
    val_end‿path_end ← Follow end
    {
      (path_start ≡ path_end) ? val_start ;
      (end = start + 1) ? (val_start ⌊ val_end) ;
      (BS ⟨start, mid⟩) ⌊ BS ⟨mid, end⟩
    }
  }
  BS 𝕩
}
•Show ⌊´⊏⎉1∘‿2⥊∾Follow¨orig
•Show ⌊´G¨{(¯1+⊑𝕩)⊸+⌾(1⊸⊑)𝕩}¨<˘∘‿2⥊orig
