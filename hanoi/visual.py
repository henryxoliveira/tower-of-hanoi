"""
SVG visualization helpers for Tower of Hanoi board and recursion tree.

This module provides functions to generate SVG (Scalable Vector Graphics) visualizations
for the Tower of Hanoi puzzle. It creates two main types of visualizations:
1. Game Board: Shows the current state of the three pegs and disks
2. Recursion Tree: Visualizes the recursive algorithm's execution structure

The visualizations are designed to be:
- Interactive: Elements can be highlighted based on current state
- Educational: Clear representation of game state and algorithm flow
- Responsive: SVG format allows scaling without quality loss
- Accessible: High contrast colors and clear labels
"""

from typing import Dict, List, Tuple
from .types import GameState, TraceEvent, Peg

# =============================================================================
# GAME BOARD VISUALIZATION
# =============================================================================

def board_svg(state: GameState, width: int = 600, height: int = 300) -> str:
    """
    Generate SVG for the Tower of Hanoi board.
    
    This function creates a visual representation of the current game state,
    showing all three pegs and their disks. Each disk is colored based on
    its size and labeled with its size number for easy identification.
    
    The board layout:
    - Three equal-width columns for pegs A, B, and C
    - Each peg has a base and can hold multiple disks
    - Disks are stacked with largest at bottom, smallest at top
    - Disk colors vary by size using HSL color space
    - Peg labels (A, B, C) are shown at the bottom
    
    Args:
        state: Current game state (tuple of three peg states)
        width: Total width of the SVG in pixels (default: 600)
        height: Total height of the SVG in pixels (default: 300)
        
    Returns:
        SVG string that can be embedded in HTML or displayed in a web browser
        
    Example:
        >>> state = initial_state(3)
        >>> svg = board_svg(state)
        >>> svg.startswith('<svg')  # Returns valid SVG markup
        True
    """
    # Extract the three pegs from the game state
    peg_a, peg_b, peg_c = state
    
    # Calculate layout dimensions
    peg_width = width // 3  # Each peg gets 1/3 of the total width
    disk_height = 20  # Height of each disk in pixels
    max_disks = max(len(peg_a), len(peg_b), len(peg_c))  # For potential future scaling
    
    # Start building the SVG markup
    svg = f'<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">'
    
    # Add background rectangle for the board
    svg += f'<rect width="{width}" height="{height}" fill="#f8f9fa" stroke="#dee2e6" stroke-width="2"/>'
    
    # Draw each of the three pegs and their disks
    for i, (peg, x_offset) in enumerate([(peg_a, 0), (peg_b, peg_width), (peg_c, 2 * peg_width)]):
        # Calculate peg position (centered in its column)
        peg_x = x_offset + peg_width // 2
        peg_y = height - 50  # Peg base positioned near bottom
        
        # Draw the peg base (vertical rectangle)
        svg += f'<rect x="{peg_x-5}" y="{peg_y}" width="10" height="50" fill="#6c757d"/>'
        
        # Draw each disk on this peg
        for j, disk in enumerate(peg):
            disk_size = disk["size"]
            # Disk width scales with size (minimum 20px, +15px per size unit)
            disk_width = max(20, disk_size * 15)
            # Position disk centered on peg, stacked from bottom up
            disk_x = peg_x - disk_width // 2
            disk_y = peg_y - (j + 1) * disk_height
            
            # Generate color based on disk size using HSL color space
            # This creates visually distinct colors for different disk sizes
            hue = (disk_size * 30) % 360  # Cycle through hue values
            color = f"hsl({hue}, 70%, 60%)"
            
            # Draw the disk rectangle with border
            svg += f'<rect x="{disk_x}" y="{disk_y}" width="{disk_width}" height="{disk_height-2}" fill="{color}" stroke="#495057" stroke-width="1"/>'
            # Add size label on the disk
            svg += f'<text x="{peg_x}" y="{disk_y + disk_height//2 + 4}" text-anchor="middle" font-size="10" fill="white">{disk_size}</text>'
    
    # Add peg labels (A, B, C) at the bottom
    labels = ["A", "B", "C"]
    for i, label in enumerate(labels):
        x = i * peg_width + peg_width // 2
        svg += f'<text x="{x}" y="{height-10}" text-anchor="middle" font-size="16" font-weight="bold" fill="#495057">{label}</text>'
    
    svg += '</svg>'
    return svg

# =============================================================================
# RECURSION TREE LAYOUT
# =============================================================================

def tree_layout(n: int, a: Peg, b: Peg, c: Peg) -> Tuple[Dict[str, Tuple[int, int, str]], List[Tuple[str, str]]]:
    """
    Generate layout for recursion tree nodes and edges.
    
    This function creates a hierarchical layout for the recursion tree that
    represents the structure of recursive calls in the Tower of Hanoi algorithm.
    It uses a recursive approach to position nodes and edges in a tree structure
    that clearly shows the parent-child relationships between recursive calls.
    
    The layout algorithm:
    1. Positions each recursive call as a node in the tree
    2. Creates edges between parent and child recursive calls
    3. Uses a grid-based system for consistent spacing
    4. Labels nodes with disk count and move information
    
    Args:
        n: Number of disks (determines tree depth and structure)
        a: Source peg for the root recursive call
        b: Destination peg for the root recursive call
        c: Auxiliary peg for the root recursive call
        
    Returns:
        Tuple containing:
        - Dictionary mapping node IDs to (x, y, label) tuples
        - List of (parent_id, child_id) edge tuples
        
    Example:
        >>> nodes, edges = tree_layout(2, 0, 2, 1)
        >>> len(nodes)  # Number of recursive calls
        3
        >>> len(edges)  # Number of parent-child relationships
        2
    """
    nodes = {}
    edges = []
    
    def layout_recursive(n: int, a: Peg, b: Peg, c: Peg, x: int, y: int, parent_id: str = None) -> int:
        """
        Recursively layout the tree nodes and edges.
        
        This inner function traverses the recursion tree structure and
        assigns grid coordinates to each node. It returns the next
        available x-coordinate to ensure proper spacing.
        
        Args:
            n: Number of disks for this recursive call
            a, b, c: Peg assignments for this call
            x, y: Current grid coordinates
            parent_id: ID of the parent node (if any)
            
        Returns:
            Next available x-coordinate for sibling nodes
        """
        # Base case: no disks to move
        if n == 0:
            return x
            
        # Create unique node identifier and label
        node_id = f"n{n}:{a}->{b}|aux{c}"
        label = f"n={n}\n{a}→{b}"  # Show disk count and move direction
        
        # Store node information
        nodes[node_id] = (x, y, label)
        
        # Create edge to parent if this is a child node
        if parent_id:
            edges.append((parent_id, node_id))
        
        # Base case: single disk (leaf node)
        if n == 1:
            return x + 1
        
        # Recursive case: position child nodes
        # Left child: move n-1 disks from source to auxiliary
        left_x = layout_recursive(n-1, a, c, b, x, y + 1, node_id)
        
        # Right child: move n-1 disks from auxiliary to destination
        right_x = layout_recursive(n-1, c, b, a, left_x, y + 1, node_id)
        
        return right_x
    
    # Start the recursive layout from the root
    layout_recursive(n, a, b, c, 0, 0)
    return nodes, edges

# =============================================================================
# RECURSION TREE VISUALIZATION
# =============================================================================

def tree_svg(n: int, events: List[TraceEvent], t: int, a: Peg = 0, b: Peg = 2, c: Peg = 1, 
             width: int = 800, level_gap: int = 90) -> str:
    """
    Generate SVG for the recursion tree with active node highlighting.
    
    This function creates an interactive visualization of the recursion tree
    that shows the current execution state of the Tower of Hanoi algorithm.
    Nodes are colored differently based on their execution status:
    - Blue: Currently active (being executed)
    - Gray: Completed (exited)
    - Light gray: Not yet reached (idle)
    
    The visualization helps users understand:
    - The structure of recursive calls
    - Which calls are currently active
    - The execution flow of the algorithm
    - The relationship between moves and recursive calls
    
    Args:
        n: Number of disks (determines tree structure)
        events: Complete list of trace events from algorithm execution
        t: Current timestamp (determines which nodes are highlighted)
        a, b, c: Peg assignments for the root recursive call
        width: Total width of the SVG in pixels
        level_gap: Vertical spacing between tree levels in pixels
        
    Returns:
        SVG string representing the interactive recursion tree
        
    Example:
        >>> events = build_trace_events(2)
        >>> svg = tree_svg(2, events, 3, 0, 2, 1)
        >>> svg.startswith('<svg')  # Returns valid SVG markup
        True
    """
    # Import here to avoid circular imports
    from .trace import active_node_at
    
    # Generate the tree layout (node positions and edges)
    nodes, edges = tree_layout(n, a, b, c)
    
    # Determine which node is currently active at the given timestamp
    active_node = active_node_at(events, t)
    
    # Calculate overall dimensions for the SVG
    max_x = max(x for x, y, _ in nodes.values()) if nodes else 0
    max_y = max(y for x, y, _ in nodes.values()) if nodes else 0
    
    # Node and spacing dimensions
    node_width = 80  # Width allocated per node
    node_height = 60  # Height of each node
    total_width = max(1, max_x + 1) * node_width
    total_height = max(1, max_y + 1) * level_gap
    
    # Start building the SVG markup
    svg = f'<svg width="{width}" height="{total_height}" xmlns="http://www.w3.org/2000/svg">'
    
    # Draw edges (lines connecting parent and child nodes)
    for from_id, to_id in edges:
        if from_id in nodes and to_id in nodes:
            from_x, from_y, _ = nodes[from_id]
            to_x, to_y, _ = nodes[to_id]
            
            # Convert grid coordinates to pixel coordinates
            from_px = from_x * node_width + node_width // 2
            from_py = from_y * level_gap + node_height // 2
            to_px = to_x * node_width + node_width // 2
            to_py = to_y * level_gap + node_height // 2
            
            # Draw the edge line
            svg += f'<line x1="{from_px}" y1="{from_py}" x2="{to_px}" y2="{to_py}" stroke="#6c757d" stroke-width="2"/>'
    
    # Draw nodes (circles representing recursive calls)
    for node_id, (x, y, label) in nodes.items():
        # Convert grid coordinates to pixel coordinates
        px = x * node_width + node_width // 2
        py = y * level_gap + node_height // 2
        
        # Determine node color based on execution state
        if node_id == active_node:
            # Currently active node - highlight in blue
            fill_color = "#007bff"
            text_color = "white"
        else:
            # Check if this node has been completed (exited)
            exited = any(e["type"] == "exit" and e["node_id"] == node_id and e["t"] <= t for e in events)
            if exited:
                # Completed node - show in gray
                fill_color = "#e9ecef"
                text_color = "#6c757d"
            else:
                # Not yet reached - show in light gray
                fill_color = "#f8f9fa"
                text_color = "#495057"
        
        # Draw the node circle
        svg += f'<circle cx="{px}" cy="{py}" r="25" fill="{fill_color}" stroke="#495057" stroke-width="2"/>'
        
        # Add the node label (split across multiple lines if needed)
        lines = label.split('\n')
        for i, line in enumerate(lines):
            # Center the text vertically within the node
            y_offset = (i - len(lines)//2) * 12
            svg += f'<text x="{px}" y="{py + y_offset + 4}" text-anchor="middle" font-size="10" fill="{text_color}">{line}</text>'
    
    svg += '</svg>'
    return svg
