# 🏛️ Tower of Hanoi - Interactive Puzzle with Recursion Visualization

A clean Streamlit application for playing the classic Tower of Hanoi puzzle, with an auto-solver and interactive recursion tree visualization.

## 🎮 Demo

*[Demo GIF will be added here]*

## 🚀 How to Run

### Prerequisites
- Python 3.11+
- pip

### Installation & Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd tower-of-hanoi
   ```

2. **Create virtual environment**
   ```bash
   python -m venv .venv
   ```

3. **Activate virtual environment**
   ```bash
   # On Windows:
   .venv\Scripts\activate
   
   # On macOS/Linux:
   source .venv/bin/activate
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Run tests**
   ```bash
   pytest -q
   ```

6. **Launch the app**
   ```bash
   streamlit run app.py
   ```

The app will open in your browser at `http://localhost:8501`

## 📁 Project Structure

```
tower-of-hanoi/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── .gitignore           # Git ignore patterns
│
├── hanoi/               # Core package
│   ├── __init__.py      # Package exports
│   ├── types.py         # Type definitions
│   ├── rules.py         # Game logic and rules
│   ├── solvers.py       # Recursive and iterative solvers
│   ├── trace.py         # Recursion tracing utilities
│   └── visual.py        # SVG visualization helpers
│
└── tests/               # Test suite
    ├── __init__.py
    ├── test_rules.py    # Game rules tests
    ├── test_solvers.py  # Solver algorithm tests
    └── test_trace.py    # Trace utilities tests
```

## 🧮 Algorithms

### Recursive Solver
The classic recursive solution follows the divide-and-conquer approach:

1. **Base case**: Move 1 disk directly from source to destination
2. **Recursive case**: 
   - Move n-1 disks from source to auxiliary peg
   - Move the largest disk from source to destination
   - Move n-1 disks from auxiliary to destination

**Time Complexity**: O(2^n)  
**Space Complexity**: O(n) (call stack depth)

### Move Generation
- **Total moves**: 2^n - 1 (optimal solution)
- **Move validation**: Ensures only top disk moves and no larger disk on smaller
- **State tracking**: Immutable game state with functional updates

## 🌳 Recursion Tree Visualization

The app provides an interactive visualization of the recursive call tree:

- **Nodes**: Represent recursive function calls with parameters
- **Edges**: Show parent-child relationships in the call tree
- **Colors**: 
  - 🔵 Blue: Currently active node
  - ⚪ Gray: Completed nodes
  - 🔘 Light gray: Pending nodes
- **Real-time updates**: Tree highlights the current execution point

## 🧪 Tests

Comprehensive test coverage for all core functionality:

```bash
# Run all tests
pytest

# Run specific test files
pytest tests/test_rules.py
pytest tests/test_solvers.py
pytest tests/test_trace.py

# Run with verbose output
pytest -v

# Run with coverage (if pytest-cov installed)
pytest --cov=hanoi
```

### Test Coverage
- ✅ **Game Rules**: Initial state, move validation, state updates
- ✅ **Solver Algorithms**: Move count verification, solution correctness
- ✅ **Trace Utilities**: Event generation, active node detection
- ✅ **Edge Cases**: Illegal moves, boundary conditions

## 🎯 Features

### Core Game
- **Interactive board**: Visual representation of pegs and disks
- **Move validation**: Prevents illegal moves
- **Progress tracking**: Move counter and completion status
- **Configurable difficulty**: 3-10 disks

### Solver & Visualization
- **Auto-solver**: Recursive algorithm with step-by-step execution
- **Speed control**: Adjustable animation speed (100-2000ms)
- **Recursion tree**: Real-time visualization of call stack
- **Play/Pause**: Control execution flow

### User Experience
- **Responsive design**: Works on desktop and mobile
- **Intuitive controls**: Clear buttons and sliders
- **Visual feedback**: Color-coded disks and status indicators
- **Educational**: Perfect for learning recursion concepts

## 🛣️ Roadmap

### Phase 1: Core Features ✅
- [x] Basic game implementation
- [x] Recursive solver
- [x] Recursion tree visualization
- [x] Streamlit UI
- [x] Test coverage

### Phase 2: Enhanced Interactivity 🚧
- [ ] **Drag & Drop**: Click and drag disks between pegs
- [ ] **Keyboard Controls**: 1/2/3 to select pegs, Enter to move
- [ ] **Manual Mode**: Allow user to solve puzzle manually
- [ ] **Undo/Redo**: Step backwards through moves

### Phase 3: Advanced Solvers 🚧
- [ ] **Iterative Stack Solver**: Non-recursive implementation
- [ ] **Bitwise Solver**: Efficient bit manipulation approach
- [ ] **Multiple Algorithms**: Choose between different solving strategies
- [ ] **Performance Comparison**: Benchmark different approaches

### Phase 4: Enhanced Visualization 🚧
- [ ] **Pan/Zoom**: Navigate large recursion trees
- [ ] **Animation**: Smooth disk movement animations
- [ ] **Theming**: Light/dark mode support
- [ ] **Export**: Save solutions as images or videos

### Phase 5: Developer Experience 🚧
- [ ] **Code Quality**: Black, Ruff, MyPy configuration
- [ ] **Pre-commit Hooks**: Automated code formatting
- [ ] **CI/CD**: GitHub Actions for testing
- [ ] **Documentation**: API docs and tutorials

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Setup
```bash
# Install development dependencies
pip install -r requirements.txt

# Install pre-commit hooks (when available)
pre-commit install

# Run linting
black hanoi/ tests/ app.py
ruff check hanoi/ tests/ app.py
mypy hanoi/ app.py
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Streamlit**: For the amazing web app framework
- **Classic Algorithm**: Tower of Hanoi as a fundamental recursion example
- **Open Source Community**: For inspiration and best practices

---

**Built with ❤️ for learning and teaching recursion concepts**
