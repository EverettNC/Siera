#!/usr/bin/env python3
"""
🏎️ Siera Ferrari Mode - Full Brain Activation
Siera with advanced memory and reasoning
"""

print("🏎️ STARTING SIERA IN FERRARI MODE...")
print("=" * 60)

try:
    from brain import *
    print("\n✅ Siera brain loaded")
    
    # Check if memory system exists
    try:
        from simple_memory_mesh import SimpleMemoryMesh
        memory = SimpleMemoryMesh(memory_dir="./siera_memory")
        stats = memory.get_stats()
        print(f"\n🧠 Memory Status:")
        print(f"   Episodic: {stats.get('episodic_memory_count', 0)}")
        print(f"   Working: {stats.get('working_memory_count', 0)}")
        print(f"   Total: {stats.get('episodic_memory_count', 0) + stats.get('working_memory_count', 0)}")
        print("\n✅ Memory system operational!")
    except Exception as e:
        print(f"\n⚠️  Memory system needs initialization: {e}")
    
    print("\n✅ Siera is ready with Ferrari brain!")
    print("\nTest with:")
    print("   python3 brain.py")
    
except Exception as e:
    print(f"\n❌ Error loading Siera: {e}")
    import traceback
    traceback.print_exc()
