# pokemon-move-macros
A very hacky script that takes a pokemon move description from the Pokemon 5e handbook (now obsolete) and creates a move macro that is functional in Roll20.

# So, What it Do?
The original text can be found at `original-copy-pasta/pokemon-moves.txt`. 
And the initial-parse that was created from that text (using `scripts/initial-parse.py`) is found at `generated/initial-parse.json`.

That `initial-parse.json` is used in `create-move-info.py` to extract some more information about the move (if it's a saving throw, attack roll, higher level damage dice, ect...) and creates the `damage-parse.json` file

That new file, in turn, is used in `create-move-macro.py` to create an easy-to-read txt file (`final.txt`) which is formatted to be a copy-paste move macro that works in Roll20!
