"""
Tower of Hanoi solvers - recursive and iterative algorithms.

This module implements various algorithms for solving the Tower of Hanoi puzzle.
The primary implementation uses the classic recursive approach, which is both
optimal (uses minimum number of moves) and educational (demonstrates recursion).

The recursive algorithm follows the divide-and-conquer strategy:
1. Move n-1 disks from source to auxiliary peg
2. Move the largest disk from source to destination
3. Move n-1 disks from auxiliary to destination

This approach guarantees the optimal solution of 2^n - 1 moves for n disks.
"""

from typing import Generator, List, Tuple
from .types import Peg, Move, TraceEvent

# =============================================================================
# RECURSIVE SOLVER
# =============================================================================

def hanoi_recursive(n: int, a: Peg = 0, b: Peg = 2, c: Peg = 1) -> Generator[Move, None, None]:
    """
    Standard recursive Tower of Hanoi solver.
    
    This is the classic recursive algorithm for solving the Tower of Hanoi puzzle.
    It uses a generator to yield moves one at a time, making it memory-efficient
    for large numbers of disks. The algorithm is optimal, requiring exactly
    2^n - 1 moves to solve a puzzle with n disks.
    
    The recursive strategy works by:
    1. Recursively moving n-1 disks from source to auxiliary peg
    2. Moving the largest disk from source to destination
    3. Recursively moving n-1 disks from auxiliary to destination
    
    Args:
        n: Number of disks to move (must be positive)
        a: Source peg (default: 0, peg A)
        b: Destination peg (default: 2, peg C)
        c: Auxiliary peg (default: 1, peg B)
        
    Yields:
        Move objects representing each step in the solution
        
    Example:
        >>> moves = list(hanoi_recursive(3))
        >>> len(moves)  # Should be 2^3 - 1 = 7 moves
        7
        >>> moves[0]  # First move: smallest disk from A to C
        {'from_': 0, 'to': 2}
    """
    # Base case: if only one disk, move it directly from source to destination
    if n == 1:
        yield Move(from_=a, to=b)
    else:
        # Recursive case: use the three-step strategy
        # Step 1: Move n-1 disks from source (a) to auxiliary (c) using destination (b) as temp
        yield from hanoi_recursive(n-1, a, c, b)
        
        # Step 2: Move the largest disk from source (a) to destination (b)
        yield Move(from_=a, to=b)
        
        # Step 3: Move n-1 disks from auxiliary (c) to destination (b) using source (a) as temp
        yield from hanoi_recursive(n-1, c, b, a)

# =============================================================================
# TRACED RECURSIVE SOLVER
# =============================================================================

def hanoi_recursive_traced(n: int, a: Peg = 0, b: Peg = 2, c: Peg = 1) -> Tuple[Generator[Move, None, None], List[TraceEvent]]:
    """
    Recursive solver with trace events for visualization.
    
    This enhanced version of the recursive solver generates trace events that
    can be used to visualize the recursive algorithm's execution. Each recursive
    call generates "enter" and "exit" events, while each move generates a "move"
    event. This allows the visualization to show the recursion tree structure
    and highlight the current execution path.
    
    The trace events are used by the visualization module to create an
    interactive recursion tree that shows how the algorithm progresses.
    
    Args:
        n: Number of disks to move (must be positive)
        a: Source peg (default: 0, peg A)
        b: Destination peg (default: 2, peg C)
        c: Auxiliary peg (default: 1, peg B)
        
    Returns:
        Tuple containing:
        - Generator yielding Move objects (same as hanoi_recursive)
        - List of TraceEvent objects for visualization
        
    Example:
        >>> moves, events = hanoi_recursive_traced(2)
        >>> len(events)  # Multiple events per recursive call
        9  # 3 recursive calls × 3 events each (enter, move, exit)
    """
    # Initialize trace event storage and timestamp counter
    events = []
    t = 0
    
    def traced_recursive(n: int, a: Peg, b: Peg, c: Peg) -> Generator[Move, None, None]:
        """
        Inner recursive function that generates both moves and trace events.
        
        This nested function maintains access to the events list and timestamp
        counter from the outer scope, allowing it to record the execution flow.
        """
        nonlocal t
        
        # Create a unique identifier for this recursive call
        # Format: "n{disks}:{source}->{dest}|aux{auxiliary}"
        node_id = f"n{n}:{a}->{b}|aux{c}"
        
        # Record the start of this recursive call
        events.append(TraceEvent(type="enter", node_id=node_id, t=t))
        t += 1
        
        if n == 1:
            # Base case: move single disk and record the move event
            move = Move(from_=a, to=b)
            events.append(TraceEvent(type="move", node_id=node_id, move=move, t=t))
            t += 1
            yield move
        else:
            # Recursive case: follow the three-step strategy with event recording
            
            # Step 1: Move n-1 disks from source to auxiliary
            yield from traced_recursive(n-1, a, c, b)
            
            # Step 2: Move largest disk from source to destination
            move = Move(from_=a, to=b)
            events.append(TraceEvent(type="move", node_id=node_id, move=move, t=t))
            t += 1
            yield move
            
            # Step 3: Move n-1 disks from auxiliary to destination
            yield from traced_recursive(n-1, c, b, a)
        
        # Record the end of this recursive call
        events.append(TraceEvent(type="exit", node_id=node_id, t=t))
        t += 1
    
    # Start the traced recursive algorithm and return both moves and events
    return traced_recursive(n, a, b, c), events

# =============================================================================
# FUTURE ITERATIVE SOLVERS
# =============================================================================

# TODO: Implement iterative solver using explicit stack
def hanoi_iterative_stack(n: int, a: Peg = 0, b: Peg = 2, c: Peg = 1) -> Generator[Move, None, None]:
    """
    Iterative Tower of Hanoi solver using explicit stack.
    
    This function will implement an iterative version of the Tower of Hanoi
    solver using an explicit stack to simulate the recursive calls. This
    approach avoids the overhead of function calls and can be more efficient
    for very large numbers of disks.
    
    The iterative approach will:
    1. Use a stack to store pending recursive calls
    2. Process the stack until all moves are generated
    3. Yield moves in the same order as the recursive version
    
    TODO: Implement this function
    
    Args:
        n: Number of disks to move
        a: Source peg
        b: Destination peg
        c: Auxiliary peg
        
    Yields:
        Move objects representing each step in the solution
    """
    raise NotImplementedError("Iterative stack solver not yet implemented")

# TODO: Implement iterative solver using bitwise operations
def hanoi_iterative_bitwise(n: int, a: Peg = 0, b: Peg = 2, c: Peg = 1) -> Generator[Move, None, None]:
    """
    Iterative Tower of Hanoi solver using bitwise operations.
    
    This function will implement an iterative solver that uses bitwise operations
    to determine the optimal moves. This approach is based on the mathematical
    properties of the Tower of Hanoi puzzle and can be very efficient.
    
    The bitwise approach will:
    1. Use binary representation to determine move patterns
    2. Generate moves without explicit recursion simulation
    3. Provide insights into the mathematical structure of the puzzle
    
    TODO: Implement this function
    
    Args:
        n: Number of disks to move
        a: Source peg
        b: Destination peg
        c: Auxiliary peg
        
    Yields:
        Move objects representing each step in the solution
    """
    raise NotImplementedError("Iterative bitwise solver not yet implemented")
