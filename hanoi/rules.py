"""
Tower of Hanoi game rules and state management.

This module implements the core game mechanics and rules for the Tower of Hanoi
puzzle. It provides functions for creating initial game states, validating moves,
applying moves to game states, and checking if the puzzle has been solved.

The module enforces the classic Tower of Hanoi rules:
1. Only one disk can be moved at a time
2. A larger disk cannot be placed on top of a smaller disk
3. Only the top disk on any peg can be moved
4. The goal is to move all disks from the starting peg to the target peg
"""

from typing import List
from .types import Peg, Move, Disk, PegState, GameState

# =============================================================================
# GAME STATE MANAGEMENT
# =============================================================================

def initial_state(n: int) -> GameState:
    """
    Create initial game state with n disks on peg 0.
    
    This function sets up the starting configuration of the Tower of Hanoi puzzle,
    where all disks are stacked on the leftmost peg (peg A, index 0) in descending
    order of size (largest at bottom, smallest at top).
    
    Args:
        n: Number of disks to create (must be positive)
        
    Returns:
        GameState with all disks on peg 0, decreasing sizes from bottom to top
        
    Example:
        >>> initial_state(3)
        ([Disk(id=0, size=3), Disk(id=1, size=2), Disk(id=2, size=1)], [], [])
    """
    # Create disks with unique IDs and sizes (size 1 = smallest, size n = largest)
    # The largest disk (size n) gets ID 0, smallest disk (size 1) gets ID n-1
    disks = [Disk(id=i, size=n-i) for i in range(n)]
    
    # Return game state: all disks on peg A (index 0), pegs B and C empty
    return ([disk for disk in disks], [], [])  # (A, B, C)

# =============================================================================
# MOVE VALIDATION
# =============================================================================

def is_legal_move(state: GameState, move: Move) -> bool:
    """
    Check if a move is legal according to Tower of Hanoi rules.
    
    This function validates whether a proposed move follows the Tower of Hanoi
    rules. A move is legal if:
    1. The source peg has at least one disk
    2. The destination peg is either empty or has a larger top disk
    3. Only the top disk from the source peg is being moved
    
    Args:
        state: Current game state (tuple of three peg states)
        move: Move to validate (contains source and destination pegs)
        
    Returns:
        True if the move is legal according to Tower of Hanoi rules
        
    Example:
        >>> state = initial_state(3)
        >>> is_legal_move(state, Move(from_=0, to=1))  # Move top disk from A to B
        True
        >>> is_legal_move(state, Move(from_=1, to=0))  # B is empty, so illegal
        False
    """
    # Extract the source and destination pegs from the game state
    from_peg = state[move["from_"]]
    to_peg = state[move["to"]]
    
    # Rule 1: Source peg must have at least one disk to move
    if not from_peg:
        return False
    
    # Rule 2: Destination peg must be empty OR have a larger top disk
    # The top disk is the last element in the peg's disk list
    if to_peg and to_peg[-1]["size"] <= from_peg[-1]["size"]:
        return False
    
    return True

# =============================================================================
# MOVE APPLICATION
# =============================================================================

def apply_move(state: GameState, move: Move) -> GameState:
    """
    Apply a legal move to the game state.
    
    This function creates a new game state by applying the specified move.
    It first validates the move and then creates a new state by moving the
    top disk from the source peg to the destination peg. The original state
    is not modified (immutable operation).
    
    Args:
        state: Current game state to modify
        move: Move to apply (must be legal)
        
    Returns:
        New game state after applying the move
        
    Raises:
        ValueError: If the move is illegal according to Tower of Hanoi rules
        
    Example:
        >>> state = initial_state(3)
        >>> new_state = apply_move(state, Move(from_=0, to=1))
        >>> len(new_state[0])  # Peg A now has 2 disks
        2
        >>> len(new_state[1])  # Peg B now has 1 disk
        1
    """
    # Validate the move before applying it
    if not is_legal_move(state, move):
        raise ValueError(f"Illegal move: {move}")
    
    # Create a new state by copying the existing pegs
    # This ensures immutability - the original state is not modified
    new_state = list(state)
    
    # Remove the top disk from the source peg
    # The top disk is the last element in the peg's disk list
    disk = new_state[move["from_"]].pop()
    
    # Add the disk to the destination peg
    # The disk becomes the new top disk on the destination peg
    new_state[move["to"]].append(disk)
    
    # Return the new state as a tuple to maintain immutability
    return tuple(new_state)

# =============================================================================
# GAME COMPLETION CHECKING
# =============================================================================

def is_solved(state: GameState, n: int) -> bool:
    """
    Check if the game is solved (all disks on peg 2).
    
    This function determines whether the Tower of Hanoi puzzle has been
    successfully completed. The puzzle is solved when all n disks are
    moved to the rightmost peg (peg C, index 2) in the correct order
    (largest at bottom, smallest at top).
    
    Args:
        state: Current game state to check
        n: Number of disks that should be in the puzzle
        
    Returns:
        True if all n disks are on peg 2 in correct descending order
        
    Example:
        >>> # Create a solved state manually
        >>> solved_state = ([], [], [Disk(id=0, size=3), Disk(id=1, size=2), Disk(id=2, size=1)])
        >>> is_solved(solved_state, 3)
        True
    """
    # Unpack the three pegs from the game state
    peg_a, peg_b, peg_c = state
    
    # Check 1: All n disks must be on peg C (index 2)
    if len(peg_c) != n:
        return False
    
    # Check 2: Disks must be in correct order (decreasing size from bottom)
    # The largest disk (size n) should be at index 0, smallest (size 1) at index n-1
    for i in range(n):
        if peg_c[i]["size"] != n - i:
            return False
    
    return True
