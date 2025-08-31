"""
Type definitions for Tower of Hanoi game.

This module defines the core data structures and type annotations used throughout
the Tower of Hanoi project. These types ensure type safety and provide clear
interfaces for the game logic, solvers, and visualization components.

The types are designed to be:
- Immutable where possible to prevent accidental state mutations
- Self-documenting through clear naming conventions
- Compatible with the recursive nature of Tower of Hanoi algorithms
"""

from typing import Literal, TypedDict, List, Generator, Optional, Tuple

# =============================================================================
# CORE GAME TYPES
# =============================================================================

# Represents the three pegs in the Tower of Hanoi puzzle
# Used throughout the codebase to identify source and destination pegs
# Values 0, 1, 2 correspond to pegs A, B, C respectively
Peg = Literal[0, 1, 2]

# Represents a single move in the Tower of Hanoi game
# Used by solvers to record moves and by visualization to animate the game
# The 'from_' field uses underscore to avoid Python keyword conflict
class Move(TypedDict):
    from_: Peg  # Source peg (where disk is moved from)
    to: Peg     # Destination peg (where disk is moved to)

# Represents a disk in the Tower of Hanoi puzzle
# Each disk has a unique ID and size, where size 1 is the smallest disk
# Used to track disk positions and validate move legality
class Disk(TypedDict):
    id: int   # Unique identifier for the disk
    size: int # Size of the disk (1 = smallest, larger numbers = bigger disks)

# =============================================================================
# GAME STATE TYPES
# =============================================================================

# Represents the current state of a single peg
# A list of disks where the first disk is at the bottom of the peg
# Used by the game engine to track disk positions and validate moves
PegState = List[Disk]

# Represents the complete state of the Tower of Hanoi game
# A tuple of three peg states representing pegs A, B, and C
# This is the primary data structure used by solvers and game logic
# The tuple format ensures immutability and enables easy state comparison
GameState = Tuple[PegState, PegState, PegState]  # (A, B, C)

# =============================================================================
# TRACING AND DEBUGGING TYPES
# =============================================================================

# Defines the types of events that can occur during algorithm execution
# Used by the trace module to log the recursive solving process
# - "enter": When entering a recursive function call
# - "move": When making a disk move
# - "exit": When exiting a recursive function call
TraceEventType = Literal["enter", "move", "exit"]

# Represents a single event in the algorithm execution trace
# Used for debugging, visualization, and understanding the solving process
# The 'total=False' allows optional fields to be omitted
class TraceEvent(TypedDict, total=False):
    type: TraceEventType    # Type of event (enter/move/exit)
    node_id: str           # Unique identifier for the recursive call node
    move: Optional[Move]   # The move made (only present for "move" events)
    t: int                 # Logical timestamp for ordering events
