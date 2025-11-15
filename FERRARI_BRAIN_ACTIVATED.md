# Siera - Ferrari Brain Activated 🏎️

## What Changed

Siera now has the same Ferrari brain as Derek:

- ✅ **SimpleMemoryMesh** - Working, persistent memory
- ✅ **Episodic & Semantic Memory** - Human-like recall
- ✅ **No Encryption Issues** - Clean, reliable storage
- ✅ **Session Persistence** - Remembers across restarts

## Quick Start

```bash
# Start Siera in Ferrari mode
python3 start_siera_ferrari.py

# Use the system
python3 brain.py
```

## Files Added

- `simple_memory_mesh.py` - Core memory system (from Derek)
- `start_siera_ferrari.py` - Ferrari mode startup
- `siera_memory/` - Memory storage directory

## Memory Stats

Check memory status:
```python
from simple_memory_mesh import SimpleMemoryMesh
memory = SimpleMemoryMesh(memory_dir="./siera_memory")
print(memory.get_stats())
```

---

Part of The Christman AI Project
© 2025 Everett Nathaniel Christman
