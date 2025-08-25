"""
Tower of Hanoi solvers - recursive and iterative algorithms.
"""

from typing import Generator, List, Tuple
from .types import Peg, Move, TraceEvent

def hanoi_recursive(n: int, a: Peg = 0, b: Peg = 2, c: Peg = 1) -> Generator[Move, None, None]:
    """
    Standard recursive Tower of Hanoi solver.
    
    Args:
        n: Number of disks to move
        a: Source peg (default: 0)
        b: Destination peg (default: 2)
        c: Auxiliary peg (default: 1)
        
    Yields:
        Moves to solve the puzzle
    """
    if n == 1:
        yield Move(from_=a, to=b)
    else:
        # Move n-1 disks from source to auxiliary
        yield from hanoi_recursive(n-1, a, c, b)
        # Move largest disk from source to destination
        yield Move(from_=a, to=b)
        # Move n-1 disks from auxiliary to destination
        yield from hanoi_recursive(n-1, c, b, a)

def hanoi_recursive_traced(n: int, a: Peg = 0, b: Peg = 2, c: Peg = 1) -> Tuple[Generator[Move, None, None], List[TraceEvent]]:
    """
    Recursive solver with trace events for visualization.
    
    Args:
        n: Number of disks to move
        a: Source peg (default: 0)
        b: Destination peg (default: 2)
        c: Auxiliary peg (default: 1)
        
    Returns:
        Tuple of (move generator, trace events list)
    """
    events = []
    t = 0
    
    def traced_recursive(n: int, a: Peg, b: Peg, c: Peg) -> Generator[Move, None, None]:
        nonlocal t
        node_id = f"n{n}:{a}->{b}|aux{c}"
        
        # Enter event
        events.append(TraceEvent(type="enter", node_id=node_id, t=t))
        t += 1
        
        if n == 1:
            move = Move(from_=a, to=b)
            events.append(TraceEvent(type="move", node_id=node_id, move=move, t=t))
            t += 1
            yield move
        else:
            # Move n-1 disks from source to auxiliary
            yield from traced_recursive(n-1, a, c, b)
            # Move largest disk from source to destination
            move = Move(from_=a, to=b)
            events.append(TraceEvent(type="move", node_id=node_id, move=move, t=t))
            t += 1
            yield move
            # Move n-1 disks from auxiliary to destination
            yield from traced_recursive(n-1, c, b, a)
        
        # Exit event
        events.append(TraceEvent(type="exit", node_id=node_id, t=t))
        t += 1
    
    return traced_recursive(n, a, b, c), events

# TODO: Implement iterative solver using stack
def hanoi_iterative_stack(n: int, a: Peg = 0, b: Peg = 2, c: Peg = 1) -> Generator[Move, None, None]:
    """
    Iterative Tower of Hanoi solver using explicit stack.
    
    TODO: Implement this function
    """
    raise NotImplementedError("Iterative stack solver not yet implemented")

# TODO: Implement iterative solver using bitwise operations
def hanoi_iterative_bitwise(n: int, a: Peg = 0, b: Peg = 2, c: Peg = 1) -> Generator[Move, None, None]:
    """
    Iterative Tower of Hanoi solver using bitwise operations.
    
    TODO: Implement this function
    """
    raise NotImplementedError("Iterative bitwise solver not yet implemented")
