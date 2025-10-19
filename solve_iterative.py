def solve_iterative(n: int, src: Peg="A", aux: Peg="B", dst: Peg="C"):
    # total moves: 2^n - 1
    total = (1 << n) - 1
    order = [src, dst, aux] if n % 2 == 1 else [src, aux, dst]

    pegs = {"A": list(range(n, 0, -1)), "B": [], "C": []}
    yield pegs  # optional: first state

    def legal_between(p: Peg, q: Peg):
        if can_move(pegs, p, q):
            move(pegs, p, q); return (p, q)
        else:
            move(pegs, q, p); return (q, p)

    for step in range(1, total + 1):
        idx = step % 3
        a, b = (order[0], order[1]) if idx == 1 else (order[0], order[2]) if idx == 2 else (order[1], order[2])
        yield legal_between(a, b)
