"""
Trace utilities for Tower of Hanoi recursion visualization.

This module provides utilities for tracking and analyzing the execution of
recursive Tower of Hanoi algorithms. It generates trace events that record
when recursive functions are entered and exited, as well as when moves are
made. These events are used by the visualization module to create interactive
recursion trees that show the algorithm's execution flow.

The tracing system helps users understand:
- How the recursive algorithm works
- Which recursive calls are currently active
- The relationship between moves and recursive calls
- The depth and structure of the recursion tree
"""

from typing import List, Optional
from .types import Peg, TraceEvent

# =============================================================================
# TRACE EVENT GENERATION
# =============================================================================

def build_trace_events(n: int, a: Peg = 0, b: Peg = 2, c: Peg = 1) -> List[TraceEvent]:
    """
    Build the complete trace events list for a Tower of Hanoi solution.
    
    This function generates a complete timeline of events that occur during
    the execution of the recursive Tower of Hanoi algorithm. Each event
    represents a specific moment in the algorithm's execution:
    - "enter" events: When a recursive function call begins
    - "move" events: When a disk is actually moved
    - "exit" events: When a recursive function call completes
    
    The events are ordered by their logical timestamp (t), which represents
    the sequence in which they occur during execution.
    
    Args:
        n: Number of disks to solve for
        a: Source peg (default: 0, peg A)
        b: Destination peg (default: 2, peg C)
        c: Auxiliary peg (default: 1, peg B)
        
    Returns:
        List of TraceEvent objects in chronological order, representing
        the complete execution trace of the recursive algorithm
        
    Example:
        >>> events = build_trace_events(2)
        >>> len(events)  # Multiple events per recursive call
        9
        >>> events[0]["type"]  # First event is usually an "enter"
        'enter'
    """
    # Import here to avoid circular imports
    from .solvers import hanoi_recursive_traced
    
    # Use the traced solver to generate both moves and trace events
    # We only need the events for visualization, so we discard the moves
    _, events = hanoi_recursive_traced(n, a, b, c)
    return events

# =============================================================================
# TRACE ANALYSIS
# =============================================================================

def active_node_at(events: List[TraceEvent], t: int) -> Optional[str]:
    """
    Find the currently active node at timestamp t.
    
    This function analyzes the trace events to determine which recursive
    function call is currently active at a given timestamp. A node is
    considered "active" if it has been entered but not yet exited.
    
    The function maintains a stack of active nodes by:
    1. Adding nodes to the stack when "enter" events are encountered
    2. Removing nodes from the stack when "exit" events are encountered
    3. Returning the most recently entered node (deepest in call stack)
    
    This is used by the visualization to highlight the current execution
    path in the recursion tree.
    
    Args:
        events: Complete list of trace events in chronological order
        t: Timestamp to check for active nodes
        
    Returns:
        Node ID of the currently active recursive call, or None if no
        recursive calls are active at the given timestamp
        
    Example:
        >>> events = build_trace_events(2)
        >>> active_node_at(events, 3)  # Check which node is active at timestamp 3
        'n1:0->2|aux1'
    """
    # Track currently active nodes using a stack-like approach
    active_nodes = []
    
    # Process all events up to the target timestamp
    for event in events:
        # Stop processing once we exceed the target timestamp
        if event["t"] > t:
            break
            
        # Add node to active stack when entering a recursive call
        if event["type"] == "enter":
            active_nodes.append(event["node_id"])
        # Remove node from active stack when exiting a recursive call
        elif event["type"] == "exit":
            if event["node_id"] in active_nodes:
                active_nodes.remove(event["node_id"])
    
    # Return the most recently entered node (deepest in the call stack)
    # This represents the currently executing recursive function
    return active_nodes[-1] if active_nodes else None
