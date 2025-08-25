"""
Tower of Hanoi game rules and state management.
"""

from typing import List
from .types import Peg, Move, Disk, PegState, GameState

def initial_state(n: int) -> GameState:
    """
    Create initial game state with n disks on peg 0.
    
    Args:
        n: Number of disks
        
    Returns:
        GameState with all disks on peg 0, decreasing sizes from bottom
    """
    disks = [Disk(id=i, size=n-i) for i in range(n)]
    return ([disk for disk in disks], [], [])  # (A, B, C)

def is_legal_move(state: GameState, move: Move) -> bool:
    """
    Check if a move is legal according to Tower of Hanoi rules.
    
    Args:
        state: Current game state
        move: Move to check
        
    Returns:
        True if move is legal (top disk only, no larger on smaller)
    """
    from_peg = state[move["from_"]]
    to_peg = state[move["to"]]
    
    # Check if source peg has disks
    if not from_peg:
        return False
    
    # Check if destination peg is empty or has larger top disk
    if to_peg and to_peg[-1]["size"] <= from_peg[-1]["size"]:
        return False
    
    return True

def apply_move(state: GameState, move: Move) -> GameState:
    """
    Apply a legal move to the game state.
    
    Args:
        state: Current game state
        move: Move to apply
        
    Returns:
        New game state after applying the move
        
    Raises:
        ValueError: If move is illegal
    """
    if not is_legal_move(state, move):
        raise ValueError(f"Illegal move: {move}")
    
    # Create new state by copying pegs
    new_state = list(state)
    
    # Remove disk from source peg
    disk = new_state[move["from_"]].pop()
    
    # Add disk to destination peg
    new_state[move["to"]].append(disk)
    
    return tuple(new_state)

def is_solved(state: GameState, n: int) -> bool:
    """
    Check if the game is solved (all disks on peg 2).
    
    Args:
        state: Current game state
        n: Number of disks in the game
        
    Returns:
        True if all n disks are on peg 2 in correct order
    """
    peg_a, peg_b, peg_c = state
    
    # All disks must be on peg C (index 2)
    if len(peg_c) != n:
        return False
    
    # Check that disks are in correct order (decreasing size)
    for i in range(n):
        if peg_c[i]["size"] != n - i:
            return False
    
    return True
