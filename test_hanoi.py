from hanoi import run

def test_small_sizes():
    for n in range(1, 6):
        pegs = run(n, verbose=False)
        assert pegs["C"] == list(range(n, 0, -1))
