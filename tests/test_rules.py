"""
Tests for Tower of Hanoi game rules.

This module contains comprehensive tests for the game rules implementation
in hanoi.rules. The tests verify that the core game mechanics work correctly,
including state initialization, move validation, move application, and
completion checking.

Test Coverage:
- Initial state creation and validation
- Legal and illegal move detection
- Move application and state mutation
- Game completion verification
- Edge cases and error conditions
"""

import pytest
from hanoi.rules import initial_state, is_legal_move, apply_move, is_solved
from hanoi.types import Move

# =============================================================================
# INITIAL STATE TESTS
# =============================================================================

def test_initial_state():
    """
    Test that initial state has all disks on peg 0 with decreasing sizes.
    
    This test verifies that the initial_state function correctly creates
    a valid starting configuration for the Tower of Hanoi puzzle. It checks:
    1. All disks are placed on the first peg (peg A)
    2. Other pegs are empty
    3. Disks have correct IDs and sizes
    4. Disks are arranged in descending order (largest at bottom)
    """
    n = 5
    state = initial_state(n)
    peg_a, peg_b, peg_c = state
    
    # Verify all disks are on peg A and other pegs are empty
    assert len(peg_a) == n
    assert len(peg_b) == 0
    assert len(peg_c) == 0
    
    # Verify disk properties and ordering
    # Disks should have IDs 0 to n-1 and sizes n to 1 (descending)
    for i, disk in enumerate(peg_a):
        assert disk["id"] == i
        assert disk["size"] == n - i

# =============================================================================
# MOVE VALIDATION TESTS
# =============================================================================

def test_illegal_move_larger_on_smaller():
    """
    Test that illegal moves are rejected when trying to place larger disk on smaller.
    
    This test verifies the core Tower of Hanoi rule that a larger disk cannot
    be placed on top of a smaller disk. It creates a scenario where this rule
    would be violated and ensures the move is properly rejected.
    """
    state = initial_state(3)
    
    # Set up a scenario where we try to place a larger disk on a smaller one
    # First move: move the largest disk (size 3) from A to B
    illegal_move = Move(from_=0, to=1)
    state = apply_move(state, illegal_move)
    
    # Second move: try to move the medium disk (size 2) from A to B
    # This should fail because size 2 < size 3, but we're trying to place it on top
    illegal_move2 = Move(from_=0, to=1)
    
    # Verify the move is correctly identified as illegal
    assert not is_legal_move(state, illegal_move2)

def test_illegal_move_empty_source():
    """
    Test that moving from empty peg is illegal.
    
    This test verifies that the game correctly prevents moves from empty pegs,
    which would be invalid since there are no disks to move.
    """
    state = initial_state(3)
    
    # Try to move from empty peg B to peg C
    illegal_move = Move(from_=1, to=2)
    assert not is_legal_move(state, illegal_move)

def test_legal_move():
    """
    Test that legal moves are accepted.
    
    This test verifies that valid moves are correctly identified as legal.
    A move is legal if it follows the Tower of Hanoi rules:
    1. Source peg has at least one disk
    2. Destination peg is empty or has a larger top disk
    """
    state = initial_state(3)
    
    # Move top disk (smallest) from A to B - this should be legal
    legal_move = Move(from_=0, to=1)
    assert is_legal_move(state, legal_move)

# =============================================================================
# MOVE APPLICATION TESTS
# =============================================================================

def test_apply_move():
    """
    Test that applying a legal move mutates state correctly.
    
    This test verifies that when a legal move is applied, the game state
    is updated correctly. It checks that:
    1. The original state is not modified (immutability)
    2. The new state reflects the move correctly
    3. Disk counts on pegs are updated properly
    4. The moved disk appears in the correct location
    """
    state = initial_state(3)
    original_state = state
    
    # Apply a legal move: move top disk from A to B
    move = Move(from_=0, to=1)
    new_state = apply_move(state, move)
    
    # Verify state immutability (original state unchanged)
    assert new_state != original_state
    
    # Verify peg disk counts are correct after the move
    assert len(new_state[0]) == 2  # Peg A now has 2 disks
    assert len(new_state[1]) == 1  # Peg B now has 1 disk
    assert len(new_state[2]) == 0  # Peg C still empty
    
    # Verify the moved disk is the smallest one (size 1)
    assert new_state[1][0]["size"] == 1

def test_apply_illegal_move_raises_error():
    """
    Test that applying illegal move raises ValueError.
    
    This test verifies that the apply_move function properly validates
    moves before applying them and raises an appropriate error when
    an illegal move is attempted.
    """
    state = initial_state(3)
    
    # Try to move from empty peg B to peg C
    illegal_move = Move(from_=1, to=2)
    
    # Verify that applying an illegal move raises ValueError
    with pytest.raises(ValueError):
        apply_move(state, illegal_move)

# =============================================================================
# GAME COMPLETION TESTS
# =============================================================================

def test_is_solved():
    """
    Test that solved state is correctly identified.
    
    This test verifies that the is_solved function correctly identifies
    when the Tower of Hanoi puzzle has been completed. A solved state
    requires all disks to be on the target peg in the correct order.
    """
    n = 3
    
    # Verify initial state is not solved
    initial = initial_state(n)
    assert not is_solved(initial, n)
    
    # Create a manually constructed solved state
    # All disks on peg C in descending order (largest at bottom)
    solved_state = ([], [], [
        {"id": 0, "size": 3},  # Largest disk at bottom
        {"id": 1, "size": 2},  # Medium disk in middle
        {"id": 2, "size": 1}   # Smallest disk at top
    ])
    assert is_solved(solved_state, n)

def test_is_solved_wrong_order():
    """
    Test that state with wrong disk order is not solved.
    
    This test verifies that the is_solved function correctly rejects
    states where all disks are on the target peg but in the wrong order.
    The Tower of Hanoi rules require disks to be stacked in descending
    order (largest at bottom).
    """
    n = 3
    
    # Create state with disks in wrong order on target peg
    wrong_order_state = ([], [], [
        {"id": 0, "size": 1},  # Smallest disk at bottom (wrong)
        {"id": 1, "size": 3},  # Largest disk in middle (wrong)
        {"id": 2, "size": 2}   # Medium disk at top (wrong)
    ])
    assert not is_solved(wrong_order_state, n)

def test_is_solved_partial():
    """
    Test that partial solution is not solved.
    
    This test verifies that the is_solved function correctly identifies
    partial solutions as incomplete. A partial solution occurs when
    some but not all disks have been moved to the target peg.
    """
    n = 3
    
    # Create a partial solution state
    # Only some disks moved to target, others still on source/auxiliary
    partial_state = ([{"id": 0, "size": 3}], [{"id": 1, "size": 2}], [{"id": 2, "size": 1}])
    assert not is_solved(partial_state, n)
