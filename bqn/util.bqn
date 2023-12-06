⟨HashMap⟩ ← •Import "/Users/grhkm/git/bqn-libs/hashmap.bqn"
Split ⇐ (¬-˜⊢×·+`»⊸>)∘≠⊔⊢
SplitF ⇐ {((¯1+⊢×·+`»⊸<)¬𝕨⊸≡¨𝕩)⊔𝕩}
_cache ⇐ { F _𝕣:
  m←HashMap˜⟨⟩
  {m.Has 𝕩? m.Get 𝕩; 𝕩 (m.Set⊢⊢) F𝕩 }
}
