Strip ← ⌽(∨`' '⊸≠)⊸/∘(⌽(∨`' '⊸≠)⊸/)
Strip " This is a string! "

SplitAtChars ← (⊢-˜+`×¬)∘=⊔⊢

# Task 1: "3 blue" -> ⟨"3", "blue"⟩
ToInt ← •ParseFloat
Task1 ← ToInt⌾⊑' '⊸SplitAtChars
Task1 "3 blue"

# Task 2: "3 blue, 4 red" -> ⟨⟨3, "blue"⟩, ⟨4, "red"⟩⟩
Task2 ← (Task1∘Strip)¨','⊸SplitAtChars
Task2 "3 blue, 4 red"

# Task 3: "12 red, 1 green, 7 blue; 4 red, 4 blue; 12 red, 1 blue" -> ⟨⟨12, "red"⟩, ...⟩
Task3 ← ≍¨(∾(Task2¨(';'⊸SplitAtChars)))
Task3 "12 red, 1 green, 7 blue; 4 red, 4 blue; 12 red, 1 blue"

# Task 4: ⟨"red", 12⟩ 𝔽 Task3 "12 red, 1 green; 4 red, 4 blue; 12 red, 1 blue" -> ⟨⟩
#         ⟨"red", 12⟩ 𝔽 Task3 "12 red, 1 green; 4 red, 4 blue; 15 red, 1 blue" -> ⟨⟨15, "red"⟩⟩
Task4 ← {⟨1⊑𝕨, ⊑¨((⊑𝕨)⊸≡∘(⟨0,1⟩⊸⊑))¨⊸/𝕩⟩}
⟨"red", 12⟩ Task4 Task3 "12 red, 1 green; 4 red, 4 blue; 12 red, 1 blue"
⟨"red", 12⟩ Task4 Task3 "12 red, 1 green; 4 red, 4 blue; 15 red, 1 blue"

# Task 5: ⟨12, ⟨12, 4, 12⟩⟩ -> 1
# Task 5: ⟨12, ⟨12, 4, 15⟩⟩ -> 0
Task5 ← 0⊸=+´∘(1⊑⊑⊸<)
Task5 ⟨12, ⟨12, 4, 12⟩⟩
Task5 ⟨12, ⟨12, 4, 15⟩⟩

# Task 6: "12 red, 1 green, 7 blue; 4 red, 4 blue; 12 red, 1 blue" -> 1
#         "13 red, 1 green, 7 blue; 4 red, 4 blue; 12 red, 1 blue" -> 0
Task6 ← ∧´∘(⟨⟨"red",12⟩,⟨"green",13⟩,⟨"blue",14⟩⟩⊸(Task5∘Task4¨))∘<Task3
Task6 "12 red, 1 green, 7 blue; 4 red, 4 blue; 12 red, 1 blue"
Task6 "13 red, 1 green, 7 blue; 4 red, 4 blue; 12 red, 1 blue"

# Task 7: "Game 48" -> 48
Task7 ← ToInt 1⊸⊑∘(' '⊸SplitAtChars)
Task7 "Game 48"

# Task 8: "Game 48: 1 red, 1 green; 6 red, 3 blue, 2 green; 3 green, 6 red" -> 48
#         "Game 48: 1 red, 1 green; 6 red, 3 blue, 2 green; 3 green, 15 red" -> 0
Task8 ← {(Task7⊑𝕩)×Task6 1⊑𝕩}':'⊸SplitAtChars

# Task 9: "Game 48: 1 red, 1 green; 6 red, 3 blue, 2 green; 3 green, 6 red" -> 54
#         "Game 48: 1 red, 1 green; 6 red, 3 blue, 2 green; 3 green, 15 red" -> 135
Task9 ← ×´∘(⟨⟨"red",12⟩,⟨"green",13⟩,⟨"blue",14⟩⟩⊸((⌈´1⊸⊑)¨Task4¨))∘<Task3∘(1⊑':'⊸SplitAtChars)
Task9 "Game 48: 1 red, 1 green; 6 red, 3 blue, 2 green; 3 green, 6 red"
Task9 "Game 48: 1 red, 1 green; 6 red, 3 blue, 2 green; 3 green, 15 red"

data ← •file.Lines "../input/in_2023_02"
# data ← •file.Lines "in"

part1 ← +´Task8¨data

part2 ← +´Task9¨data

•Out •Repr part1
•Out •Repr part2
