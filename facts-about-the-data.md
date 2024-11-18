## What do we know about the data?

(Assuming all lines are read in)

1. The line before "Type" is the move name
2. every move has a Type, and it's the second line
3. every move has a Move Power, and it's the third line.
4. every move has a Move Time, and it's the fourth line.
5. every move has PP, and it's the fifth line.
6. every move has a Duration, and it's the sixth line.
   6a. some durations have concentration
7. every move has a Range, and it's the seventh line.
8. every move has a Description, and it's at least on the eighth line, but can stretch a number of lines.
9. some moves have a Higher Levels, which contains important information for damage calculation or other information

## Design choices

1. as long as damage type is displayed, then we don't need to worry about STAB
2. going to have to think about picking the higher of the two or more available movePowers in macro

Final Macros will look like this:

```
Low Kick
Power: STR/DEX
MoveTime: 1 action
PP: 5
Duration: Instantaneous
Range: Melee
Attack: [[1d20+{@{STR_Mod} , @{DEX_Mod}}kh1+@{ProfBonus}]]
Damage: [[1d10+{@{STR_Mod} , @{DEX_Mod}}kh1+@{STAB}]] Fighting
Description: Flinch on Nat 19+
Higher Levels: <paste> (if no @level5|10|17)
```

## Obsolete information

1. sprinkled in are some page numbers, they seem to be just before move names, but that's not been confirmed
