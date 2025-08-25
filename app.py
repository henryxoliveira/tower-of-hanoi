"""
Tower of Hanoi - Streamlit App
Interactive game with solver and recursion tree visualization.
"""

import streamlit as st
import time
from typing import List

from hanoi import (
    initial_state, is_legal_move, apply_move, is_solved,
    hanoi_recursive, build_trace_events, active_node_at,
    board_svg, tree_svg
)
from hanoi.types import GameState, Move, TraceEvent

# Page configuration
st.set_page_config(
    page_title="Tower of Hanoi",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

def initialize_session_state():
    """Initialize session state variables."""
    if "n" not in st.session_state:
        st.session_state.n = 3
    if "state" not in st.session_state:
        st.session_state.state = initial_state(st.session_state.n)
    if "moves" not in st.session_state:
        st.session_state.moves = list(hanoi_recursive(st.session_state.n))
    if "i" not in st.session_state:
        st.session_state.i = 0
    if "events" not in st.session_state:
        st.session_state.events = build_trace_events(st.session_state.n)
    if "t" not in st.session_state:
        st.session_state.t = 0
    if "is_playing" not in st.session_state:
        st.session_state.is_playing = False
    if "speed_ms" not in st.session_state:
        st.session_state.speed_ms = 500

def reset_game():
    """Reset the game to initial state."""
    st.session_state.state = initial_state(st.session_state.n)
    st.session_state.moves = list(hanoi_recursive(st.session_state.n))
    st.session_state.i = 0
    st.session_state.events = build_trace_events(st.session_state.n)
    st.session_state.t = 0
    st.session_state.is_playing = False

def step_game():
    """Advance the game by one move."""
    if st.session_state.i < len(st.session_state.moves):
        move = st.session_state.moves[st.session_state.i]
        if is_legal_move(st.session_state.state, move):
            st.session_state.state = apply_move(st.session_state.state, move)
            st.session_state.i += 1
            
            # Advance trace to next event
            while (st.session_state.t < len(st.session_state.events) and 
                   st.session_state.events[st.session_state.t]["type"] != "move"):
                st.session_state.t += 1
            if st.session_state.t < len(st.session_state.events):
                st.session_state.t += 1

def auto_play():
    """Auto-play the game."""
    if st.session_state.is_playing and st.session_state.i < len(st.session_state.moves):
        step_game()
        time.sleep(st.session_state.speed_ms / 1000)
        st.experimental_rerun()

# Initialize session state
initialize_session_state()

# Main app
st.title("🏛️ Tower of Hanoi")
st.markdown("Interactive puzzle with recursive solver and visualization")

# Sidebar controls
with st.sidebar:
    st.header("Controls")
    
    # Disk count slider
    new_n = st.slider("Number of Disks", 3, 10, st.session_state.n)
    if new_n != st.session_state.n:
        st.session_state.n = new_n
        reset_game()
    
    st.markdown("---")
    
    # Game controls
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔄 Reset"):
            reset_game()
            st.experimental_rerun()
    
    with col2:
        if st.button("⏭️ Step"):
            step_game()
            st.experimental_rerun()
    
    # Auto-play controls
    if st.button("▶️ Play" if not st.session_state.is_playing else "⏸️ Pause"):
        st.session_state.is_playing = not st.session_state.is_playing
        st.experimental_rerun()
    
    # Speed control
    st.session_state.speed_ms = st.slider("Speed (ms)", 100, 2000, st.session_state.speed_ms, 100)
    
    st.markdown("---")
    
    # Game info
    st.subheader("Game Info")
    st.metric("Moves", f"{st.session_state.i}/{len(st.session_state.moves)}")
    
    solved = is_solved(st.session_state.state, st.session_state.n)
    if solved:
        st.success("✅ Solved!")
    else:
        st.info("🔄 In Progress")
    
    # Progress bar
    if len(st.session_state.moves) > 0:
        progress = st.session_state.i / len(st.session_state.moves)
        st.progress(progress)

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Game Board")
    board_html = board_svg(st.session_state.state)
    st.markdown(board_html, unsafe_allow_html=True)

with col2:
    st.subheader("Recursion Tree")
    tree_html = tree_svg(
        st.session_state.n, 
        st.session_state.events, 
        st.session_state.t
    )
    st.markdown(tree_html, unsafe_allow_html=True)

# Auto-play logic
if st.session_state.is_playing:
    auto_play()

# Footer
st.markdown("---")
st.markdown("""
**How to play:** Move all disks from peg A to peg C, one at a time, without placing a larger disk on top of a smaller one.

**Features:**
- Interactive game board
- Recursive solver visualization
- Step-by-step execution
- Auto-play with adjustable speed
""")
