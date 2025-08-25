"""
Tower of Hanoi - Core package for game logic, solvers, and visualization.
"""

from .types import Peg, Move, Disk, PegState, GameState, TraceEvent, TraceEventType
from .rules import initial_state, is_legal_move, apply_move, is_solved
from .solvers import hanoi_recursive, hanoi_recursive_traced
from .trace import build_trace_events, active_node_at
from .visual import board_svg, tree_svg, tree_layout

__all__ = [
    # Types
    'Peg', 'Move', 'Disk', 'PegState', 'GameState', 'TraceEvent', 'TraceEventType',
    # Rules
    'initial_state', 'is_legal_move', 'apply_move', 'is_solved',
    # Solvers
    'hanoi_recursive', 'hanoi_recursive_traced',
    # Trace
    'build_trace_events', 'active_node_at',
    # Visual
    'board_svg', 'tree_svg', 'tree_layout',
]
