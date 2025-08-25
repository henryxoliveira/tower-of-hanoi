"""
Tests for Tower of Hanoi game rules.
"""

import pytest
from hanoi.rules import initial_state, is_legal_move, apply_move, is_solved
from hanoi.types import Move

def test_initial_state():
    """Test that initial state has all disks on peg 0 with decreasing sizes."""
    n = 5
    state = initial_state(n)
    peg_a, peg_b, peg_c = state
    
    # All disks should be on peg A
    assert len(peg_a) == n
    assert len(peg_b) == 0
    assert len(peg_c) == 0
    
    # Disks should have decreasing sizes from bottom
    for i, disk in enumerate(peg_a):
        assert disk["id"] == i
        assert disk["size"] == n - i

def test_illegal_move_larger_on_smaller():
    """Test that illegal moves are rejected."""
    state = initial_state(3)
    
    # Try to move larger disk onto smaller disk
    illegal_move = Move(from_=0, to=1)
    # First move disk 0->1 (size 3 to empty)
    state = apply_move(state, illegal_move)
    # Then try to move disk 0->1 (size 2 onto size 3) - should fail
    illegal_move2 = Move(from_=0, to=1)
    
    assert not is_legal_move(state, illegal_move2)

def test_illegal_move_empty_source():
    """Test that moving from empty peg is illegal."""
    state = initial_state(3)
    
    # Try to move from empty peg B
    illegal_move = Move(from_=1, to=2)
    assert not is_legal_move(state, illegal_move)

def test_legal_move():
    """Test that legal moves are accepted."""
    state = initial_state(3)
    
    # Move top disk from A to B
    legal_move = Move(from_=0, to=1)
    assert is_legal_move(state, legal_move)

def test_apply_move():
    """Test that applying a legal move mutates state correctly."""
    state = initial_state(3)
    original_state = state
    
    # Move top disk from A to B
    move = Move(from_=0, to=1)
    new_state = apply_move(state, move)
    
    # State should be different
    assert new_state != original_state
    
    # Peg A should have one less disk
    assert len(new_state[0]) == 2
    assert len(new_state[1]) == 1
    assert len(new_state[2]) == 0
    
    # The moved disk should be on peg B
    assert new_state[1][0]["size"] == 1

def test_apply_illegal_move_raises_error():
    """Test that applying illegal move raises ValueError."""
    state = initial_state(3)
    
    # Try to move from empty peg
    illegal_move = Move(from_=1, to=2)
    
    with pytest.raises(ValueError):
        apply_move(state, illegal_move)

def test_is_solved():
    """Test that solved state is correctly identified."""
    n = 3
    
    # Initial state is not solved
    initial = initial_state(n)
    assert not is_solved(initial, n)
    
    # Create solved state manually
    solved_state = ([], [], [
        {"id": 0, "size": 3},
        {"id": 1, "size": 2},
        {"id": 2, "size": 1}
    ])
    assert is_solved(solved_state, n)

def test_is_solved_wrong_order():
    """Test that state with wrong disk order is not solved."""
    n = 3
    
    # State with disks in wrong order
    wrong_order_state = ([], [], [
        {"id": 0, "size": 1},
        {"id": 1, "size": 3},
        {"id": 2, "size": 2}
    ])
    assert not is_solved(wrong_order_state, n)

def test_is_solved_partial():
    """Test that partial solution is not solved."""
    n = 3
    
    # State with only some disks moved
    partial_state = ([{"id": 0, "size": 3}], [{"id": 1, "size": 2}], [{"id": 2, "size": 1}])
    assert not is_solved(partial_state, n)
