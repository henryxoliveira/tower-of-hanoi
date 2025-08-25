"""
Tests for Tower of Hanoi trace utilities.
"""

import pytest
from hanoi.trace import build_trace_events, active_node_at

def test_build_trace_events_well_nested():
    """Test that build_trace_events returns well-nested enter/exit events."""
    n = 3
    events = build_trace_events(n)
    
    # Check that events are well-nested
    stack = []
    for event in events:
        if event["type"] == "enter":
            stack.append(event["node_id"])
        elif event["type"] == "exit":
            assert stack, "Exit event without matching enter"
            assert stack[-1] == event["node_id"], "Exit event doesn't match last enter"
            stack.pop()
    
    assert not stack, "Unmatched enter events"

def test_build_trace_events_move_count():
    """Test that number of move events equals 2^n - 1."""
    for n in range(1, 6):  # Test n=1 to n=5
        events = build_trace_events(n)
        move_events = [e for e in events if e["type"] == "move"]
        expected_moves = 2**n - 1
        assert len(move_events) == expected_moves, f"n={n}: expected {expected_moves} moves, got {len(move_events)}"

def test_build_trace_events_structure():
    """Test that trace events have correct structure."""
    n = 3
    events = build_trace_events(n)
    
    for event in events:
        # Check required fields
        assert "type" in event
        assert "t" in event
        assert event["type"] in ["enter", "move", "exit"]
        assert isinstance(event["t"], int)
        
        # Check node_id is present for all events
        assert "node_id" in event
        
        # Check move field is present only for move events
        if event["type"] == "move":
            assert "move" in event
            assert event["move"] is not None
        else:
            assert "move" not in event or event["move"] is None

def test_active_node_at_initial():
    """Test active_node_at at timestamp 0."""
    n = 3
    events = build_trace_events(n)
    
    active = active_node_at(events, 0)
    # At t=0, the root node should be active
    assert active == "n3:0->2|aux1"

def test_active_node_at_midway():
    """Test active_node_at at a midway timestamp."""
    n = 3
    events = build_trace_events(n)
    
    # Find a timestamp where we're in the middle of execution
    mid_t = len(events) // 2
    active = active_node_at(events, mid_t)
    
    # Should return a valid node_id or None
    if active is not None:
        assert "n" in active and "->" in active and "aux" in active

def test_active_node_at_end():
    """Test active_node_at at the end of execution."""
    n = 3
    events = build_trace_events(n)
    
    # At the very end, no node should be active
    end_t = events[-1]["t"]
    active = active_node_at(events, end_t)
    assert active is None

def test_active_node_at_specific_timestamps():
    """Test active_node_at at specific known timestamps."""
    n = 2  # Simpler case for easier testing
    events = build_trace_events(n)
    
    # Find the first move event
    first_move_t = None
    for event in events:
        if event["type"] == "move":
            first_move_t = event["t"]
            break
    
    if first_move_t is not None:
        active = active_node_at(events, first_move_t)
        # Should be active at the time of the move
        assert active is not None

def test_active_node_at_empty_events():
    """Test active_node_at with empty events list."""
    active = active_node_at([], 0)
    assert active is None

def test_active_node_at_future_timestamp():
    """Test active_node_at with timestamp beyond events."""
    n = 3
    events = build_trace_events(n)
    
    # Use a timestamp beyond the last event
    future_t = events[-1]["t"] + 100
    active = active_node_at(events, future_t)
    assert active is None
