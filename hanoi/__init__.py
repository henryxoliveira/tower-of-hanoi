"""
Tower of Hanoi - Core package for game logic, solvers, and visualization.

This package provides a complete implementation of the Tower of Hanoi puzzle,
including game rules, recursive solvers, visualization components, and debugging
tools. It's designed as a modular system where each module handles a specific
aspect of the puzzle.

Package Structure:
- types.py: Core data structures and type definitions
- rules.py: Game rules and state management
- solvers.py: Recursive algorithms for solving the puzzle
- trace.py: Debugging and execution tracing utilities
- visual.py: SVG-based visualization components
"""

# =============================================================================
# TYPE DEFINITIONS
# =============================================================================

# Import all core data types used throughout the package
# These provide type safety and clear interfaces between modules
from .types import Peg, Move, Disk, PegState, GameState, TraceEvent, TraceEventType

# =============================================================================
# GAME RULES AND LOGIC
# =============================================================================

# Import game rule functions that handle state management and move validation
# These functions implement the core Tower of Hanoi puzzle mechanics
from .rules import initial_state, is_legal_move, apply_move, is_solved

# =============================================================================
# SOLVING ALGORITHMS
# =============================================================================

# Import recursive solvers that generate optimal move sequences
# These implement the classic recursive algorithm for Tower of Hanoi
from .solvers import hanoi_recursive, hanoi_recursive_traced

# =============================================================================
# DEBUGGING AND TRACING
# =============================================================================

# Import tracing utilities for debugging and visualization
# These help understand the recursive algorithm's execution flow
from .trace import build_trace_events, active_node_at

# =============================================================================
# VISUALIZATION COMPONENTS
# =============================================================================

# Import SVG-based visualization functions for game board and recursion tree
# These create interactive visual representations of the game state and algorithm
from .visual import board_svg, tree_svg, tree_layout

# =============================================================================
# PUBLIC API DEFINITION
# =============================================================================

# Define the complete public API for the hanoi package
# This ensures that only intended functions and types are exposed to users
# and provides a clear interface for the entire package
__all__ = [
    # Core data types for game state and moves
    'Peg', 'Move', 'Disk', 'PegState', 'GameState', 'TraceEvent', 'TraceEventType',
    
    # Game rule functions for state management and validation
    'initial_state', 'is_legal_move', 'apply_move', 'is_solved',
    
    # Recursive solving algorithms
    'hanoi_recursive', 'hanoi_recursive_traced',
    
    # Debugging and execution tracing utilities
    'build_trace_events', 'active_node_at',
    
    # Visualization components for web interface
    'board_svg', 'tree_svg', 'tree_layout',
]
