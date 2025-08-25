"""
Trace utilities for Tower of Hanoi recursion visualization.
"""

from typing import List, Optional
from .types import Peg, TraceEvent

def build_trace_events(n: int, a: Peg = 0, b: Peg = 2, c: Peg = 1) -> List[TraceEvent]:
    """
    Build the complete trace events list for a Tower of Hanoi solution.
    
    Args:
        n: Number of disks
        a: Source peg (default: 0)
        b: Destination peg (default: 2)
        c: Auxiliary peg (default: 1)
        
    Returns:
        List of trace events in chronological order
    """
    from .solvers import hanoi_recursive_traced
    
    # Get the traced solver and extract events
    _, events = hanoi_recursive_traced(n, a, b, c)
    return events

def active_node_at(events: List[TraceEvent], t: int) -> Optional[str]:
    """
    Find the currently active node at timestamp t.
    
    A node is active if it has been entered but not yet exited.
    
    Args:
        events: List of trace events
        t: Timestamp to check
        
    Returns:
        Node ID of the active node, or None if no node is active
    """
    active_nodes = []
    
    for event in events:
        if event["t"] > t:
            break
            
        if event["type"] == "enter":
            active_nodes.append(event["node_id"])
        elif event["type"] == "exit":
            if event["node_id"] in active_nodes:
                active_nodes.remove(event["node_id"])
    
    # Return the most recently entered node (deepest in call stack)
    return active_nodes[-1] if active_nodes else None
