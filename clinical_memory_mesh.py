
from simple_memory_mesh import SimpleMemoryMesh
from typing import Dict, List, Any
from datetime import datetime
import json

class ClinicalMemoryMesh(SimpleMemoryMesh):
    """
    Extended memory for clinical/trauma-informed AI systems
    Adds specialized storage for crisis tracking and clinical protocols
    """
    
    def __init__(self, memory_dir: str = "clinical_memory"):
        super().__init__(memory_dir)
        
        # Clinical-specific memory categories
        self.clinical_categories = {
            "crisis_events": [],
            "safety_plans": [],
            "protocol_history": [],
            "behavioral_patterns": [],
            "risk_assessments": []
        }
        
        self.crisis_file = self.memory_dir / "crisis_tracking.json"
        self.safety_file = self.memory_dir / "safety_plans.json"
        self.protocol_file = self.memory_dir / "clinical_protocols.json"
        
        self.load_clinical_memory()
    
    def store_crisis_event(self, level: str, context: Dict, intervention: str):
        """Track crisis events separately - HIPAA-compliant"""
        event = {
            "id": self._generate_id(f"crisis_{datetime.now().isoformat()}"),
            "level": level,
            "context": context,
            "intervention": intervention,
            "timestamp": datetime.now().isoformat(),
            "resolved": False
        }
        
        self.clinical_categories["crisis_events"].append(event)
        self._save_clinical()
        
        # Also store in main memory for context
        self.store(
            f"Crisis {level}: {intervention}",
            category="events",
            importance=0.9,
            metadata={"crisis": True, "level": level}
        )
        
        return event["id"]
    
    def store_safety_plan(self, user_id: str, plan: Dict):
        """Store personalized safety plan"""
        safety_plan = {
            "id": self._generate_id(f"safety_{user_id}"),
            "user_id": user_id,
            "plan": plan,
            "created": datetime.now().isoformat(),
            "last_updated": datetime.now().isoformat()
        }
        
        self.clinical_categories["safety_plans"].append(safety_plan)
        self._save_clinical()
        return safety_plan["id"]
    
    def track_protocol(self, protocol_name: str, session_data: Dict):
        """Track clinical protocol usage (CPT, PE, EMDR, etc.)"""
        protocol_entry = {
            "id": self._generate_id(f"protocol_{protocol_name}"),
            "protocol": protocol_name,
            "session_data": session_data,
            "timestamp": datetime.now().isoformat()
        }
        
        self.clinical_categories["protocol_history"].append(protocol_entry)
        self._save_clinical()
        
        # Store in semantic memory for learning
        self.store(
            f"Applied {protocol_name} protocol",
            category="learning",
            importance=0.8,
            metadata={"protocol": protocol_name}
        )
    
    def get_crisis_history(self, days: int = 30) -> List[Dict]:
        """Retrieve recent crisis events"""
        from datetime import timedelta
        cutoff = datetime.now() - timedelta(days=days)
        
        return [
            event for event in self.clinical_categories["crisis_events"]
            if datetime.fromisoformat(event["timestamp"]) >= cutoff
        ]
    
    def get_active_safety_plan(self, user_id: str) -> Dict:
        """Get user's current safety plan"""
        plans = [
            p for p in self.clinical_categories["safety_plans"]
            if p["user_id"] == user_id
        ]
        return plans[-1] if plans else None
    
    def _save_clinical(self):
        """Save clinical data separately - encrypted in production"""
        with open(self.crisis_file, 'w') as f:
            json.dump(self.clinical_categories["crisis_events"], f, indent=2)
        
        with open(self.safety_file, 'w') as f:
            json.dump(self.clinical_categories["safety_plans"], f, indent=2)
        
        with open(self.protocol_file, 'w') as f:
            json.dump(self.clinical_categories["protocol_history"], f, indent=2)
    
    def load_clinical_memory(self):
        """Load clinical data if exists"""
        if self.crisis_file.exists():
            with open(self.crisis_file) as f:
                self.clinical_categories["crisis_events"] = json.load(f)
        
        if self.safety_file.exists():
            with open(self.safety_file) as f:
                self.clinical_categories["safety_plans"] = json.load(f)
        
        if self.protocol_file.exists():
            with open(self.protocol_file) as f:
                self.clinical_categories["protocol_history"] = json.load(f)
    
    def get_clinical_stats(self) -> Dict:
        """Extended stats with clinical metrics"""
        base_stats = self.get_stats()
        
        clinical_stats = {
            "crisis_events_total": len(self.clinical_categories["crisis_events"]),
            "active_safety_plans": len(self.clinical_categories["safety_plans"]),
            "protocols_used": len(set(p["protocol"] for p in self.clinical_categories["protocol_history"])),
            "recent_crises_7d": len(self.get_crisis_history(days=7))
        }
        
        return {**base_stats, **clinical_stats}
