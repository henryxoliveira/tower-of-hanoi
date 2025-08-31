"""
Tower of Hanoi - Streamlit App
Interactive game with solver and recursion tree visualization.

This is the main application entry point that provides a web-based interface
for the Tower of Hanoi puzzle. It combines game logic, visualization, and
interactive controls to create an educational and engaging experience.

Key Features:
- Interactive game board with real-time visualization
- Recursive solver with step-by-step execution
- Recursion tree visualization showing algorithm flow
- Auto-play functionality with adjustable speed
- Session state management for persistent game state
"""

import streamlit as st
import time
from typing import List

# Import core game logic and visualization functions from the hanoi package
from hanoi import (
    initial_state, is_legal_move, apply_move, is_solved,
    hanoi_recursive, build_trace_events, active_node_at,
    board_svg, tree_svg
)
from hanoi.types import GameState, Move, TraceEvent

# =============================================================================
# PAGE CONFIGURATION
# =============================================================================

# Configure the Streamlit page with appropriate title, icon, and layout
# Wide layout provides more space for the game board and recursion tree
st.set_page_config(
    page_title="Tower of Hanoi",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =============================================================================
# SESSION STATE MANAGEMENT
# =============================================================================

def initialize_session_state():
    """
    Initialize all session state variables for the game.
    
    Session state persists across user interactions and page refreshes,
    allowing the game to maintain its current state. This function sets up
    all necessary variables with their default values.
    """
    if "n" not in st.session_state:
        st.session_state.n = 3  # Number of disks (default: 3)
    if "state" not in st.session_state:
        st.session_state.state = initial_state(st.session_state.n)  # Current game state
    if "moves" not in st.session_state:
        st.session_state.moves = list(hanoi_recursive(st.session_state.n))  # Pre-computed solution
    if "i" not in st.session_state:
        st.session_state.i = 0  # Current move index
    if "events" not in st.session_state:
        st.session_state.events = build_trace_events(st.session_state.n)  # Recursion trace events
    if "t" not in st.session_state:
        st.session_state.t = 0  # Current trace event index
    if "is_playing" not in st.session_state:
        st.session_state.is_playing = False  # Auto-play status
    if "speed_ms" not in st.session_state:
        st.session_state.speed_ms = 500  # Auto-play speed in milliseconds

def reset_game():
    """
    Reset the game to its initial state.
    
    This function reinitializes all game-related variables, effectively
    starting a fresh game with the current number of disks. It's called
    when the user changes the disk count or manually resets the game.
    """
    st.session_state.state = initial_state(st.session_state.n)
    st.session_state.moves = list(hanoi_recursive(st.session_state.n))
    st.session_state.i = 0
    st.session_state.events = build_trace_events(st.session_state.n)
    st.session_state.t = 0
    st.session_state.is_playing = False

# =============================================================================
# GAME LOGIC FUNCTIONS
# =============================================================================

def step_game():
    """
    Advance the game by one move.
    
    This function executes the next move in the solution sequence and
    updates both the game state and the recursion tree visualization.
    It also advances the trace to the next relevant event for proper
    tree highlighting.
    """
    if st.session_state.i < len(st.session_state.moves):
        move = st.session_state.moves[st.session_state.i]
        if is_legal_move(st.session_state.state, move):
            # Apply the move to update the game state
            st.session_state.state = apply_move(st.session_state.state, move)
            st.session_state.i += 1
            
            # Advance trace to next move event for tree visualization
            # Skip non-move events (enter/exit) to highlight the actual move
            while (st.session_state.t < len(st.session_state.events) and 
                   st.session_state.events[st.session_state.t]["type"] != "move"):
                st.session_state.t += 1
            if st.session_state.t < len(st.session_state.events):
                st.session_state.t += 1

def auto_play():
    """
    Auto-play the game at the specified speed.
    
    This function is called during auto-play mode to automatically
    advance the game. It uses time.sleep to control the speed and
    triggers a page rerun to update the UI.
    """
    if st.session_state.is_playing and st.session_state.i < len(st.session_state.moves):
        step_game()
        time.sleep(st.session_state.speed_ms / 1000)  # Convert ms to seconds
        st.experimental_rerun()

# =============================================================================
# APPLICATION INITIALIZATION
# =============================================================================

# Initialize session state when the app starts
initialize_session_state()

# =============================================================================
# MAIN USER INTERFACE
# =============================================================================

# Page header with title and description
st.title("🏛️ Tower of Hanoi")
st.markdown("Interactive puzzle with recursive solver and visualization")

# =============================================================================
# SIDEBAR CONTROLS
# =============================================================================

with st.sidebar:
    st.header("Controls")
    
    # Disk count configuration
    # Allows users to change the puzzle difficulty (3-10 disks)
    # Automatically resets the game when changed
    new_n = st.slider("Number of Disks", 3, 10, st.session_state.n)
    if new_n != st.session_state.n:
        st.session_state.n = new_n
        reset_game()
    
    st.markdown("---")
    
    # Manual game controls
    # Two-column layout for reset and step buttons
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔄 Reset"):
            reset_game()
            st.experimental_rerun()
    
    with col2:
        if st.button("⏭️ Step"):
            step_game()
            st.experimental_rerun()
    
    # Auto-play toggle
    # Button text changes based on current play state
    if st.button("▶️ Play" if not st.session_state.is_playing else "⏸️ Pause"):
        st.session_state.is_playing = not st.session_state.is_playing
        st.experimental_rerun()
    
    # Speed control for auto-play
    # Range from 100ms (fast) to 2000ms (slow) with 100ms increments
    st.session_state.speed_ms = st.slider("Speed (ms)", 100, 2000, st.session_state.speed_ms, 100)
    
    st.markdown("---")
    
    # Game status information
    st.subheader("Game Info")
    st.metric("Moves", f"{st.session_state.i}/{len(st.session_state.moves)}")
    
    # Display solved status with appropriate styling
    solved = is_solved(st.session_state.state, st.session_state.n)
    if solved:
        st.success("✅ Solved!")
    else:
        st.info("🔄 In Progress")
    
    # Visual progress bar showing completion percentage
    if len(st.session_state.moves) > 0:
        progress = st.session_state.i / len(st.session_state.moves)
        st.progress(progress)

# =============================================================================
# MAIN CONTENT AREA
# =============================================================================

# Two-column layout: game board (2/3 width) and recursion tree (1/3 width)
col1, col2 = st.columns([2, 1])

with col1:
    # Game board visualization
    # Shows the current state of all three pegs and disks
    st.subheader("Game Board")
    board_html = board_svg(st.session_state.state)
    st.markdown(board_html, unsafe_allow_html=True)

with col2:
    # Recursion tree visualization
    # Shows the recursive algorithm structure with current execution highlighted
    st.subheader("Recursion Tree")
    tree_html = tree_svg(
        st.session_state.n, 
        st.session_state.events, 
        st.session_state.t
    )
    st.markdown(tree_html, unsafe_allow_html=True)

# =============================================================================
# AUTO-PLAY EXECUTION
# =============================================================================

# Execute auto-play logic if enabled
if st.session_state.is_playing:
    auto_play()

# =============================================================================
# FOOTER AND HELP
# =============================================================================

# Footer with game instructions and feature list
st.markdown("---")
st.markdown("""
**How to play:** Move all disks from peg A to peg C, one at a time, without placing a larger disk on top of a smaller one.

**Features:**
- Interactive game board
- Recursive solver visualization
- Step-by-step execution
- Auto-play with adjustable speed
""")
