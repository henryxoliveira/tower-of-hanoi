"""
Type definitions for Tower of Hanoi game.
"""

from typing import Literal, TypedDict, List, Generator, Optional, Tuple

Peg = Literal[0, 1, 2]

class Move(TypedDict):
    from_: Peg
    to: Peg

class Disk(TypedDict):
    id: int
    size: int  # 1 = smallest

PegState = List[Disk]
GameState = Tuple[PegState, PegState, PegState]  # (A, B, C)

TraceEventType = Literal["enter", "move", "exit"]

class TraceEvent(TypedDict, total=False):
    type: TraceEventType
    node_id: str
    move: Optional[Move]
    t: int  # logical timestamp
