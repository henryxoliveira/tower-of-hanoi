# hanoi.py

from typing import List, Tuple, Literal, Dict, Generator

Peg = Literal["A", "B", "C"]
Move = Tuple[Peg, Peg]

def can_move(pegs: Dict[Peg, List[int]], src: Peg, dst: Peg) -> bool:
    if not pegs[src]:
        return False
    if not pegs[dst]:
        return True
    return pegs[src][-1] < pegs[dst][-1]

def move(pegs: Dict[Peg, List[int]], src: Peg, dst: Peg) -> None:
    if not can_move(pegs, src, dst):
        raise ValueError(f"Illegal move {src}->{dst}: {pegs[src]} -> {pegs[dst]}")
    pegs[dst].append(pegs[src].pop())

def solve_recursive(n: int, src: Peg, aux: Peg, dst: Peg) -> Generator[Move, None, None]:
    """Yield optimal moves to solve n disks from src to dst using aux."""
    if n == 1:
        yield (src, dst)
    else:
        yield from solve_recursive(n - 1, src, dst, aux)
        yield (src, dst)
        yield from solve_recursive(n - 1, aux, src, dst)

def run(n: int, verbose: bool = True) -> Dict[Peg, List[int]]:
    if n <= 0:
        raise ValueError("n must be positive")
    pegs: Dict[Peg, List[int]] = {"A": list(range(n, 0, -1)), "B": [], "C": []}
    if verbose:
        print("Start:", pegs)
    moves_made = 0
    for (s, d) in solve_recursive(n, "A", "B", "C"):
        move(pegs, s, d)
        moves_made += 1
        if verbose:
            print(f"Move {moves_made:>3}: {s} -> {d} | {pegs}")
    if verbose:
        optimal = (1 << n) - 1
        print(f"Solved in {moves_made} moves (optimal {optimal}).")
    # quick sanity check
    assert pegs["C"] == list(range(n, 0, -1))
    return pegs

if __name__ == "__main__":
    import sys
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    run(n, verbose=True)
