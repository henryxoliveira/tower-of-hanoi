"""
Tests for Tower of Hanoi solvers.
"""

import pytest
from hanoi.solvers import hanoi_recursive
from hanoi.rules import initial_state, apply_move, is_solved

def test_hanoi_recursive_move_count():
    """Test that recursive solver produces correct number of moves."""
    for n in range(1, 7):  # Test n=1 to n=6
        moves = list(hanoi_recursive(n))
        expected_moves = 2**n - 1
        assert len(moves) == expected_moves, f"n={n}: expected {expected_moves}, got {len(moves)}"

def test_hanoi_recursive_solves_puzzle():
    """Test that applying all moves from recursive solver solves the puzzle."""
    for n in range(1, 7):  # Test n=1 to n=6
        state = initial_state(n)
        moves = list(hanoi_recursive(n))
        
        # Apply all moves
        for move in moves:
            state = apply_move(state, move)
        
        # Check that puzzle is solved
        assert is_solved(state, n), f"Puzzle not solved for n={n}"

def test_hanoi_recursive_moves_are_legal():
    """Test that all moves from recursive solver are legal."""
    for n in range(1, 6):  # Test n=1 to n=5 (n=6 might be slow)
        state = initial_state(n)
        moves = list(hanoi_recursive(n))
        
        for i, move in enumerate(moves):
            # Check that move is legal
            from hanoi.rules import is_legal_move
            assert is_legal_move(state, move), f"Illegal move {i}: {move}"
            
            # Apply the move
            state = apply_move(state, move)

def test_hanoi_recursive_specific_sequence():
    """Test specific known sequence for n=3."""
    moves = list(hanoi_recursive(3))
    
    # Known optimal solution for n=3: 7 moves
    expected_moves = [
        {"from_": 0, "to": 2},  # Move disk 1 to C
        {"from_": 0, "to": 1},  # Move disk 2 to B
        {"from_": 2, "to": 1},  # Move disk 1 to B
        {"from_": 0, "to": 2},  # Move disk 3 to C
        {"from_": 1, "to": 0},  # Move disk 1 to A
        {"from_": 1, "to": 2},  # Move disk 2 to C
        {"from_": 0, "to": 2},  # Move disk 1 to C
    ]
    
    assert len(moves) == len(expected_moves)
    for actual, expected in zip(moves, expected_moves):
        assert actual["from_"] == expected["from_"]
        assert actual["to"] == expected["to"]

def test_hanoi_recursive_different_pegs():
    """Test recursive solver with different peg configurations."""
    # Test moving from peg 1 to peg 0 with auxiliary peg 2
    moves = list(hanoi_recursive(3, a=1, b=0, c=2))
    
    # Should still produce 7 moves
    assert len(moves) == 7
    
    # Apply moves to verify they work
    state = ([], [{"id": 0, "size": 3}, {"id": 1, "size": 2}, {"id": 2, "size": 1}], [])
    for move in moves:
        state = apply_move(state, move)
    
    # Check that all disks end up on peg 0
    assert len(state[0]) == 3
    assert len(state[1]) == 0
    assert len(state[2]) == 0
