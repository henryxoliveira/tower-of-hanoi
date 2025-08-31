"""
Tests for Tower of Hanoi trace utilities.

This module contains comprehensive tests for the tracing utilities in hanoi.trace.
The tests verify that the trace event generation and analysis functions work
correctly, ensuring that the recursive algorithm execution can be properly
tracked and visualized.

Test Coverage:
- Trace event structure and validation
- Event nesting and ordering
- Move event counting and timing
- Active node detection at various timestamps
- Edge cases and boundary conditions
"""

import pytest
from hanoi.trace import build_trace_events, active_node_at

# =============================================================================
# TRACE EVENT STRUCTURE TESTS
# =============================================================================

def test_build_trace_events_well_nested():
    """
    Test that build_trace_events returns well-nested enter/exit events.
    
    This test verifies that the trace events follow proper nesting structure,
    similar to function call stacks. Each "enter" event should have a
    corresponding "exit" event, and the nesting should be balanced.
    
    The test uses a stack-based approach to track enter/exit pairs and
    ensures that the recursive calls are properly structured.
    """
    n = 3
    events = build_trace_events(n)
    
    # Use a stack to track enter/exit event pairs
    stack = []
    for event in events:
        if event["type"] == "enter":
            # Push the node ID onto the stack when entering
            stack.append(event["node_id"])
        elif event["type"] == "exit":
            # Verify we have a matching enter event
            assert stack, "Exit event without matching enter"
            # Verify the exit matches the most recent enter
            assert stack[-1] == event["node_id"], "Exit event doesn't match last enter"
            # Pop the matching enter event
            stack.pop()
    
    # Verify all enter events have been matched with exits
    assert not stack, "Unmatched enter events"

def test_build_trace_events_move_count():
    """
    Test that number of move events equals 2^n - 1.
    
    This test verifies that the trace contains the correct number of move
    events. Since each move event corresponds to an actual disk movement,
    the number of move events should equal the optimal number of moves
    required to solve the puzzle (2^n - 1).
    
    The test covers multiple disk counts to ensure the relationship holds
    across different puzzle sizes.
    """
    for n in range(1, 6):  # Test n=1 to n=5
        events = build_trace_events(n)
        # Count only the move events (actual disk movements)
        move_events = [e for e in events if e["type"] == "move"]
        expected_moves = 2**n - 1  # Mathematical formula for optimal moves
        assert len(move_events) == expected_moves, f"n={n}: expected {expected_moves} moves, got {len(move_events)}"

def test_build_trace_events_structure():
    """
    Test that trace events have correct structure.
    
    This test verifies that all trace events have the required fields and
    that the field values are of the correct types. It ensures that:
    1. All events have required fields (type, t, node_id)
    2. Event types are valid (enter, move, exit)
    3. Timestamps are integers
    4. Move events have the move field, others don't
    5. Node IDs are present for all events
    """
    n = 3
    events = build_trace_events(n)
    
    for event in events:
        # Verify required fields are present
        assert "type" in event
        assert "t" in event
        assert event["type"] in ["enter", "move", "exit"]
        assert isinstance(event["t"], int)
        
        # Verify node_id is present for all events
        assert "node_id" in event
        
        # Verify move field is present only for move events
        if event["type"] == "move":
            assert "move" in event
            assert event["move"] is not None
        else:
            # Non-move events should not have a move field, or it should be None
            assert "move" not in event or event["move"] is None

# =============================================================================
# ACTIVE NODE DETECTION TESTS
# =============================================================================

def test_active_node_at_initial():
    """
    Test active_node_at at timestamp 0.
    
    This test verifies that at the very beginning of execution (timestamp 0),
    the root recursive call is active. This represents the initial state
    where the main recursive function has been entered but not yet exited.
    """
    n = 3
    events = build_trace_events(n)
    
    active = active_node_at(events, 0)
    # At t=0, the root node should be active (the main recursive call)
    assert active == "n3:0->2|aux1"

def test_active_node_at_midway():
    """
    Test active_node_at at a midway timestamp.
    
    This test verifies that the active node detection works correctly
    during the middle of execution. It checks that the function returns
    a valid node ID or None, and that the returned node ID follows
    the expected format.
    """
    n = 3
    events = build_trace_events(n)
    
    # Find a timestamp in the middle of execution
    mid_t = len(events) // 2
    active = active_node_at(events, mid_t)
    
    # Should return a valid node_id or None
    if active is not None:
        # Verify the node ID follows the expected format
        assert "n" in active and "->" in active and "aux" in active

def test_active_node_at_end():
    """
    Test active_node_at at the end of execution.
    
    This test verifies that at the very end of execution, no recursive
    calls are active. This represents the state after all recursive
    functions have completed and exited.
    """
    n = 3
    events = build_trace_events(n)
    
    # At the very end, no node should be active (all calls have exited)
    end_t = events[-1]["t"]
    active = active_node_at(events, end_t)
    assert active is None

def test_active_node_at_specific_timestamps():
    """
    Test active_node_at at specific known timestamps.
    
    This test verifies that the active node detection works correctly
    at specific points in the execution, particularly around move events.
    It ensures that when a move is being executed, the corresponding
    recursive call is marked as active.
    """
    n = 2  # Use simpler case for easier testing
    events = build_trace_events(n)
    
    # Find the first move event timestamp
    first_move_t = None
    for event in events:
        if event["type"] == "move":
            first_move_t = event["t"]
            break
    
    if first_move_t is not None:
        active = active_node_at(events, first_move_t)
        # Should be active at the time of the move
        assert active is not None

# =============================================================================
# EDGE CASE TESTS
# =============================================================================

def test_active_node_at_empty_events():
    """
    Test active_node_at with empty events list.
    
    This test verifies that the function handles the edge case of an
    empty events list gracefully. When there are no events, there
    can be no active nodes.
    """
    active = active_node_at([], 0)
    assert active is None

def test_active_node_at_future_timestamp():
    """
    Test active_node_at with timestamp beyond events.
    
    This test verifies that the function handles timestamps that are
    beyond the range of available events. When the timestamp is in
    the future relative to the events, no nodes should be active.
    """
    n = 3
    events = build_trace_events(n)
    
    # Use a timestamp beyond the last event
    future_t = events[-1]["t"] + 100
    active = active_node_at(events, future_t)
    assert active is None
