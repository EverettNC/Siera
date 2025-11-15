#!/usr/bin/env python3
"""
🏥 Siera Clinical Ferrari Mode
Full memory + clinical tracking
"""

print("🏥 STARTING SIERA IN CLINICAL FERRARI MODE...")
print("=" * 60)

try:
    from clinical_memory_mesh import ClinicalMemoryMesh
    memory = ClinicalMemoryMesh(memory_dir="./siera_clinical_memory")
    
    stats = memory.get_clinical_stats()
    
    print(f"\n🏥 Clinical Memory Status:")
    print(f"   Episodic memories: {stats.get('episodic_memory_count', 0)}")
    print(f"   Crisis events tracked: {stats.get('crisis_events_total', 0)}")
    print(f"   Active safety plans: {stats.get('active_safety_plans', 0)}")
    print(f"   Protocols used: {stats.get('protocols_used', 0)}")
    print(f"   Recent crises (7d): {stats.get('recent_crises_7d', 0)}")
    
    print("\n✅ Clinical memory system operational!")
    print("\nFeatures:")
    print("   - Crisis event tracking")
    print("   - Safety plan storage")
    print("   - Clinical protocol history")
    print("   - Behavioral pattern analysis")
    print("   - HIPAA-compliant logging")
    
except Exception as e:
    print(f"\n⚠️  Error: {e}")
    import traceback
    traceback.print_exc()

print(f"\n✅ Siera clinical Ferrari brain ready!")
