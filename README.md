ETF Belgrade — Intelligent Systems

First homework: Search algorithms

The base of the project (including GUI) was provided by lecturers. The modules `algorithms.py` and `tree_node.py` are student’s work.

The assignment can be found [here](http://ri4es.etf.rs/materijali/projekat/2024_2025/dz1/IS_DZ1_2024.pdf).

# How to run

`python main.py <algorithm> <map> <timeout>`

- `<algorithm>`: the name of the algorithm
    - `ExampleAlgorithm` (default): random moves
    - `Blue`: *depth-first* search
    - `Red`: *breadth-first* search
    - `Black`: *branch-and-bound* search
    - `White`: *A\** search with *Manhattan* heuristics
- `<map>`: path to the file that contains the map (default: `example_map.txt`)
    - `_` denotes empty space
    - `S` denotes a spaceship
    - `G` denotes a goal
    - `O` denotes an obstacle
- `<timeout>`: maximum run time; `0` denotes unlimited time (default)