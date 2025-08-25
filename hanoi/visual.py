"""
SVG visualization helpers for Tower of Hanoi board and recursion tree.
"""

from typing import Dict, List, Tuple
from .types import GameState, TraceEvent, Peg

def board_svg(state: GameState, width: int = 600, height: int = 300) -> str:
    """
    Generate SVG for the Tower of Hanoi board.
    
    Args:
        state: Current game state
        width: SVG width
        height: SVG height
        
    Returns:
        SVG string representing the board
    """
    peg_a, peg_b, peg_c = state
    peg_width = width // 3
    disk_height = 20
    max_disks = max(len(peg_a), len(peg_b), len(peg_c))
    
    svg = f'<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">'
    
    # Background
    svg += f'<rect width="{width}" height="{height}" fill="#f8f9fa" stroke="#dee2e6" stroke-width="2"/>'
    
    # Draw pegs
    for i, (peg, x_offset) in enumerate([(peg_a, 0), (peg_b, peg_width), (peg_c, 2 * peg_width)]):
        peg_x = x_offset + peg_width // 2
        peg_y = height - 50
        
        # Peg base
        svg += f'<rect x="{peg_x-5}" y="{peg_y}" width="10" height="50" fill="#6c757d"/>'
        
        # Draw disks
        for j, disk in enumerate(peg):
            disk_size = disk["size"]
            disk_width = max(20, disk_size * 15)
            disk_x = peg_x - disk_width // 2
            disk_y = peg_y - (j + 1) * disk_height
            
            # Disk color based on size
            hue = (disk_size * 30) % 360
            color = f"hsl({hue}, 70%, 60%)"
            
            svg += f'<rect x="{disk_x}" y="{disk_y}" width="{disk_width}" height="{disk_height-2}" fill="{color}" stroke="#495057" stroke-width="1"/>'
            svg += f'<text x="{peg_x}" y="{disk_y + disk_height//2 + 4}" text-anchor="middle" font-size="10" fill="white">{disk_size}</text>'
    
    # Peg labels
    labels = ["A", "B", "C"]
    for i, label in enumerate(labels):
        x = i * peg_width + peg_width // 2
        svg += f'<text x="{x}" y="{height-10}" text-anchor="middle" font-size="16" font-weight="bold" fill="#495057">{label}</text>'
    
    svg += '</svg>'
    return svg

def tree_layout(n: int, a: Peg, b: Peg, c: Peg) -> Tuple[Dict[str, Tuple[int, int, str]], List[Tuple[str, str]]]:
    """
    Generate layout for recursion tree nodes and edges.
    
    Args:
        n: Number of disks
        a: Source peg
        b: Destination peg
        c: Auxiliary peg
        
    Returns:
        Tuple of (nodes dict, edges list) where nodes is {id: (x, y, label)}
    """
    nodes = {}
    edges = []
    
    def layout_recursive(n: int, a: Peg, b: Peg, c: Peg, x: int, y: int, parent_id: str = None) -> int:
        if n == 0:
            return x
            
        node_id = f"n{n}:{a}->{b}|aux{c}"
        label = f"n={n}\n{a}→{b}"
        
        nodes[node_id] = (x, y, label)
        
        if parent_id:
            edges.append((parent_id, node_id))
        
        if n == 1:
            return x + 1
        
        # Left child (n-1 disks to auxiliary)
        left_x = layout_recursive(n-1, a, c, b, x, y + 1, node_id)
        
        # Right child (n-1 disks from auxiliary to destination)
        right_x = layout_recursive(n-1, c, b, a, left_x, y + 1, node_id)
        
        return right_x
    
    layout_recursive(n, a, b, c, 0, 0)
    return nodes, edges

def tree_svg(n: int, events: List[TraceEvent], t: int, a: Peg = 0, b: Peg = 2, c: Peg = 1, 
             width: int = 800, level_gap: int = 90) -> str:
    """
    Generate SVG for the recursion tree with active node highlighting.
    
    Args:
        n: Number of disks
        events: Trace events
        t: Current timestamp
        a: Source peg
        b: Destination peg
        c: Auxiliary peg
        width: SVG width
        level_gap: Vertical gap between levels
        
    Returns:
        SVG string representing the recursion tree
    """
    from .trace import active_node_at
    
    nodes, edges = tree_layout(n, a, b, c)
    active_node = active_node_at(events, t)
    
    # Calculate dimensions
    max_x = max(x for x, y, _ in nodes.values()) if nodes else 0
    max_y = max(y for x, y, _ in nodes.values()) if nodes else 0
    
    node_width = 80
    node_height = 60
    total_width = max(1, max_x + 1) * node_width
    total_height = max(1, max_y + 1) * level_gap
    
    svg = f'<svg width="{width}" height="{total_height}" xmlns="http://www.w3.org/2000/svg">'
    
    # Draw edges
    for from_id, to_id in edges:
        if from_id in nodes and to_id in nodes:
            from_x, from_y, _ = nodes[from_id]
            to_x, to_y, _ = nodes[to_id]
            
            # Convert to pixel coordinates
            from_px = from_x * node_width + node_width // 2
            from_py = from_y * level_gap + node_height // 2
            to_px = to_x * node_width + node_width // 2
            to_py = to_y * level_gap + node_height // 2
            
            svg += f'<line x1="{from_px}" y1="{from_py}" x2="{to_px}" y2="{to_py}" stroke="#6c757d" stroke-width="2"/>'
    
    # Draw nodes
    for node_id, (x, y, label) in nodes.items():
        px = x * node_width + node_width // 2
        py = y * level_gap + node_height // 2
        
        # Determine node color based on state
        if node_id == active_node:
            fill_color = "#007bff"  # Active - blue
            text_color = "white"
        else:
            # Check if node has been exited
            exited = any(e["type"] == "exit" and e["node_id"] == node_id and e["t"] <= t for e in events)
            if exited:
                fill_color = "#e9ecef"  # Exited - gray
                text_color = "#6c757d"
            else:
                fill_color = "#f8f9fa"  # Idle - light gray
                text_color = "#495057"
        
        # Node circle
        svg += f'<circle cx="{px}" cy="{py}" r="25" fill="{fill_color}" stroke="#495057" stroke-width="2"/>'
        
        # Node label
        lines = label.split('\n')
        for i, line in enumerate(lines):
            y_offset = (i - len(lines)//2) * 12
            svg += f'<text x="{px}" y="{py + y_offset + 4}" text-anchor="middle" font-size="10" fill="{text_color}">{line}</text>'
    
    svg += '</svg>'
    return svg
