"""
Sierra's Cortex Executive - Central Coordination Layer

Adapted from Derek's Brain Architecture (Christman AI Project)
The executive layer that coordinates all Sierra subsystems

Architecture Layers (6-tier):
1. Cortex (Executive) - THIS MODULE - Decision-making, priority routing
2. Memory - Conversation history, survivor context, trauma patterns
3. Reasoning - Danger assessment, empathy analysis, safety planning
4. Communication - Voice Cortex, text output, multimodal interface
5. Perception - Audio danger detection, speech recognition, vision (future)
6. Actions - Safety plans, resource delivery, crisis intervention

Core Mission: "How can we help you love yourself more?"
Safety First: Domestic violence survivors need coordinated, predictable support
"""

import logging
import time
import threading
import queue
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass
from datetime import datetime
from enum import Enum

logger = logging.getLogger(__name__)


class CortexPriority(Enum):
    """Processing priority levels"""
    CRISIS = 1       # Immediate danger - interrupt everything
    URGENT = 2       # Safety-related, time-sensitive
    HIGH = 3         # Important but not emergency
    NORMAL = 4       # Standard conversation
    LOW = 5          # Background processing, maintenance


class CortexMode(Enum):
    """Operating modes"""
    CRISIS = "crisis"                    # Active danger - crisis intervention
    SAFETY_PLANNING = "safety_planning"  # Creating safety plan
    EMOTIONAL_SUPPORT = "emotional"      # Empathy, validation, comfort
    RESOURCE_DELIVERY = "resources"      # Providing hotlines, shelters, legal
    LEARNING = "learning"                # Building knowledge
    MAINTENANCE = "maintenance"          # Background tasks


@dataclass
class CortexRequest:
    """Request to the cortex"""
    request_id: str
    priority: CortexPriority
    mode: CortexMode
    content: Dict[str, Any]
    callback: Optional[Callable] = None
    timestamp: float = 0.0

    def __post_init__(self):
        if self.timestamp == 0.0:
            self.timestamp = time.time()

    def __lt__(self, other):
        """Compare by priority, then timestamp"""
        if self.priority.value != other.priority.value:
            return self.priority.value < other.priority.value
        return self.timestamp < other.timestamp


@dataclass
class CortexResponse:
    """Response from the cortex"""
    request_id: str
    success: bool
    data: Dict[str, Any]
    processing_time: float
    modules_involved: List[str]
    timestamp: float = 0.0

    def __post_init__(self):
        if self.timestamp == 0.0:
            self.timestamp = time.time()


class SierraCortexExecutive:
    """
    Sierra's Cortex Executive - Central Coordinator

    Responsibilities:
    1. Route requests to appropriate subsystems
    2. Enforce priority-based processing (crisis first)
    3. Coordinate module interactions
    4. Maintain global state and context
    5. Enforce cardinal rules (Policy Engine integration)
    6. Emergency override when danger detected

    Singleton Pattern: Only ONE cortex coordinates Sierra

    Integration Points:
    - Voice Cortex: Singleton voice output
    - Audio Safety System: Danger detection + speech recognition
    - Behavioral Capture: Comprehensive danger assessment
    - Empathy Engine: Emotional analysis and validation
    - Safety Planning: Escape plan creation
    - Resources: Hotline/shelter delivery
    - AI Engine: LLM-powered conversation
    - Knowledge Acquisition: Domain expertise
    - Core Philosophy: Values and sacred truths
    """

    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        """Singleton: Only ONE cortex exists"""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        """Initialize cortex (only once)"""
        if self._initialized:
            return

        self._initialized = True

        # Request queue (priority queue)
        self.request_queue: queue.PriorityQueue = queue.PriorityQueue()

        # Current state
        self.current_mode = CortexMode.EMOTIONAL_SUPPORT
        self.is_processing = False
        self.current_request: Optional[CortexRequest] = None

        # Module registry
        self.modules: Dict[str, Any] = {}
        self.module_health: Dict[str, bool] = {}

        # Global context (survivor state)
        self.survivor_context = {
            "crisis_active": False,
            "danger_level": "SAFE",
            "current_emotion": None,
            "safety_plan_status": None,
            "session_start": time.time(),
            "total_interactions": 0
        }

        # Statistics
        self.total_requests = 0
        self.crisis_interventions = 0
        self.mode_switches = 0

        # Processing thread
        self.processing_active = True
        self.processor_thread = threading.Thread(target=self._process_queue, daemon=True)
        self.processor_thread.start()

        logger.info("Sierra Cortex Executive initialized")
        logger.info("  Mode: EMOTIONAL_SUPPORT (default)")
        logger.info("  Priority system: CRISIS → URGENT → HIGH → NORMAL → LOW")

    def register_module(self, name: str, module: Any) -> bool:
        """
        Register a subsystem module

        Args:
            name: Module identifier (e.g., "voice_cortex", "empathy_engine")
            module: Module instance

        Returns:
            True if registered successfully
        """
        try:
            self.modules[name] = module
            self.module_health[name] = True
            logger.info(f"Cortex: Registered module '{name}'")
            return True
        except Exception as e:
            logger.error(f"Cortex: Failed to register module '{name}': {e}")
            return False

    def submit_request(
        self,
        request_id: str,
        priority: CortexPriority,
        mode: CortexMode,
        content: Dict[str, Any],
        callback: Optional[Callable] = None
    ) -> bool:
        """
        Submit request to cortex

        Args:
            request_id: Unique identifier
            priority: Processing priority
            mode: Operating mode for this request
            content: Request data
            callback: Optional callback when complete

        Returns:
            True if queued successfully
        """
        try:
            request = CortexRequest(
                request_id=request_id,
                priority=priority,
                mode=mode,
                content=content,
                callback=callback
            )

            # CRISIS priority → interrupt current processing
            if priority == CortexPriority.CRISIS:
                if self.is_processing and self.current_request:
                    if self.current_request.priority != CortexPriority.CRISIS:
                        self._interrupt_current()
                        self.crisis_interventions += 1

                # Update global context
                self.survivor_context["crisis_active"] = True

            # Add to queue
            self.request_queue.put(request)
            self.total_requests += 1

            return True

        except Exception as e:
            logger.error(f"Cortex: Failed to submit request: {e}")
            return False

    def _process_queue(self):
        """Background thread - processes request queue"""
        while self.processing_active:
            try:
                # Get next request (blocks until available)
                request = self.request_queue.get(timeout=0.5)

                # Process it
                self._process_request(request)

                # Mark as done
                self.request_queue.task_done()

            except queue.Empty:
                continue
            except Exception as e:
                logger.error(f"Cortex: Queue processing error: {e}", exc_info=True)

    def _process_request(self, request: CortexRequest):
        """Process a cortex request"""
        start_time = time.time()

        try:
            self.is_processing = True
            self.current_request = request

            # Switch mode if needed
            if request.mode != self.current_mode:
                self._switch_mode(request.mode)

            # Route to appropriate handler
            handler = self._get_handler(request.mode)
            response_data = handler(request)

            # Create response
            processing_time = time.time() - start_time
            response = CortexResponse(
                request_id=request.request_id,
                success=True,
                data=response_data,
                processing_time=processing_time,
                modules_involved=response_data.get("modules_used", [])
            )

            # Callback if provided
            if request.callback:
                request.callback(response)

            # Update context
            self.survivor_context["total_interactions"] += 1

            logger.info(
                f"Cortex: Processed {request.request_id} "
                f"({request.mode.value}) in {processing_time:.3f}s"
            )

        except Exception as e:
            logger.error(f"Cortex: Request processing error: {e}", exc_info=True)
        finally:
            self.is_processing = False
            self.current_request = None

    def _get_handler(self, mode: CortexMode) -> Callable:
        """Get handler function for mode"""
        handlers = {
            CortexMode.CRISIS: self._handle_crisis,
            CortexMode.SAFETY_PLANNING: self._handle_safety_planning,
            CortexMode.EMOTIONAL_SUPPORT: self._handle_emotional_support,
            CortexMode.RESOURCE_DELIVERY: self._handle_resources,
            CortexMode.LEARNING: self._handle_learning,
            CortexMode.MAINTENANCE: self._handle_maintenance
        }
        return handlers.get(mode, self._handle_emotional_support)

    def _handle_crisis(self, request: CortexRequest) -> Dict[str, Any]:
        """Handle crisis-level request"""
        modules_used = []

        # 1. Assess danger (Behavioral Capture)
        if "behavioral_capture" in self.modules:
            danger = self.modules["behavioral_capture"].assess_danger(
                request.content.get("text", ""),
                request.content.get("context", {})
            )
            self.survivor_context["danger_level"] = danger["level"]
            modules_used.append("behavioral_capture")

        # 2. Voice crisis intervention (Voice Cortex)
        if "voice_cortex" in self.modules:
            crisis_message = (
                "I'm very concerned about your safety right now. "
                "If you're in immediate danger, call 911. "
                "The National Domestic Violence Hotline is 1-800-799-7233."
            )
            self.modules["voice_cortex"].speak_crisis(crisis_message)
            modules_used.append("voice_cortex")

        # 3. Provide emergency resources (Resources)
        resources = []
        if "resources" in self.modules:
            resources = self.modules["resources"].get_crisis_resources()
            modules_used.append("resources")

        # 4. Empathy response (Empathy Engine)
        empathy_response = None
        if "empathy_engine" in self.modules:
            empathy_response = self.modules["empathy_engine"].generate_response(
                request.content.get("text", ""),
                emotion="fear"
            )
            modules_used.append("empathy_engine")

        return {
            "mode": "crisis",
            "crisis_message": crisis_message,
            "resources": resources,
            "empathy": empathy_response,
            "modules_used": modules_used
        }

    def _handle_safety_planning(self, request: CortexRequest) -> Dict[str, Any]:
        """Handle safety planning request"""
        modules_used = []

        # 1. Create or update safety plan (Safety Planning)
        plan = None
        if "safety_planning" in self.modules:
            plan = self.modules["safety_planning"].create_plan(
                request.content.get("user_info", {})
            )
            modules_used.append("safety_planning")

        # 2. Provide resources for plan (Resources)
        resources = []
        if "resources" in self.modules:
            resources = self.modules["resources"].get_safety_resources()
            modules_used.append("resources")

        # 3. Supportive voice output (Voice Cortex)
        if "voice_cortex" in self.modules:
            self.modules["voice_cortex"].speak(
                "Let's work together on a safety plan. You deserve to feel safe.",
                priority=2  # HIGH priority
            )
            modules_used.append("voice_cortex")

        return {
            "mode": "safety_planning",
            "plan": plan,
            "resources": resources,
            "modules_used": modules_used
        }

    def _handle_emotional_support(self, request: CortexRequest) -> Dict[str, Any]:
        """Handle emotional support request"""
        modules_used = []

        # 1. Analyze emotion (Empathy Engine)
        empathy_response = None
        if "empathy_engine" in self.modules:
            text = request.content.get("text", "")
            empathy_response = self.modules["empathy_engine"].generate_response(text)
            self.survivor_context["current_emotion"] = empathy_response.get("detected_emotion")
            modules_used.append("empathy_engine")

        # 2. Generate AI response (AI Engine)
        ai_response = None
        if "ai_engine" in self.modules:
            ai_response = self.modules["ai_engine"].generate_response(
                request.content.get("text", ""),
                mode="emotional_support"
            )
            modules_used.append("ai_engine")

        # 3. Voice output (Voice Cortex)
        if "voice_cortex" in self.modules and ai_response:
            self.modules["voice_cortex"].speak_gentle(ai_response)
            modules_used.append("voice_cortex")

        # 4. Background danger check (Behavioral Capture - passive)
        if "behavioral_capture" in self.modules:
            danger = self.modules["behavioral_capture"].passive_assessment(
                request.content.get("text", "")
            )
            if danger.get("level") != "SAFE":
                # Escalate to crisis if danger detected
                self.submit_request(
                    request_id=f"crisis_{time.time()}",
                    priority=CortexPriority.CRISIS,
                    mode=CortexMode.CRISIS,
                    content=request.content
                )
            modules_used.append("behavioral_capture")

        return {
            "mode": "emotional_support",
            "empathy": empathy_response,
            "ai_response": ai_response,
            "modules_used": modules_used
        }

    def _handle_resources(self, request: CortexRequest) -> Dict[str, Any]:
        """Handle resource delivery request"""
        modules_used = []

        # 1. Get resources (Resources)
        resources = []
        if "resources" in self.modules:
            resource_type = request.content.get("type", "all")
            resources = self.modules["resources"].search_resources(
                query=request.content.get("query", ""),
                resource_type=resource_type
            )
            modules_used.append("resources")

        # 2. Voice delivery (Voice Cortex)
        if "voice_cortex" in self.modules and resources:
            summary = f"I found {len(resources)} resources that might help you."
            self.modules["voice_cortex"].speak(summary)
            modules_used.append("voice_cortex")

        return {
            "mode": "resources",
            "resources": resources,
            "modules_used": modules_used
        }

    def _handle_learning(self, request: CortexRequest) -> Dict[str, Any]:
        """Handle learning/knowledge request"""
        modules_used = []

        # 1. Query knowledge (Knowledge Acquisition)
        answer = None
        if "knowledge_acquisition" in self.modules:
            answer = self.modules["knowledge_acquisition"].query(
                request.content.get("question", "")
            )
            modules_used.append("knowledge_acquisition")

        return {
            "mode": "learning",
            "answer": answer,
            "modules_used": modules_used
        }

    def _handle_maintenance(self, request: CortexRequest) -> Dict[str, Any]:
        """Handle background maintenance tasks"""
        modules_used = []

        # Health checks, cleanup, etc.
        health_status = self._check_module_health()

        return {
            "mode": "maintenance",
            "health_status": health_status,
            "modules_used": modules_used
        }

    def _switch_mode(self, new_mode: CortexMode):
        """Switch operating mode"""
        old_mode = self.current_mode
        self.current_mode = new_mode
        self.mode_switches += 1

        logger.info(f"Cortex: Mode switch {old_mode.value} → {new_mode.value}")

    def _interrupt_current(self):
        """Interrupt current processing for crisis"""
        logger.warning("Cortex: INTERRUPTING for crisis")
        self.is_processing = False

    def _check_module_health(self) -> Dict[str, bool]:
        """Check health of all registered modules"""
        health = {}
        for name, module in self.modules.items():
            try:
                # Check if module has health check method
                if hasattr(module, "health_check"):
                    health[name] = module.health_check()
                else:
                    # Assume healthy if exists
                    health[name] = True
            except Exception:
                health[name] = False

        self.module_health = health
        return health

    def get_status(self) -> Dict:
        """Get current cortex status"""
        return {
            "current_mode": self.current_mode.value,
            "is_processing": self.is_processing,
            "queue_size": self.request_queue.qsize(),
            "total_requests": self.total_requests,
            "crisis_interventions": self.crisis_interventions,
            "mode_switches": self.mode_switches,
            "registered_modules": list(self.modules.keys()),
            "module_health": self.module_health,
            "survivor_context": self.survivor_context,
            "session_duration": time.time() - self.survivor_context["session_start"]
        }

    def shutdown(self):
        """Clean shutdown"""
        logger.info("Cortex: Shutting down...")
        self.processing_active = False

        # Clear queue
        while not self.request_queue.empty():
            try:
                self.request_queue.get_nowait()
            except queue.Empty:
                break

        # Wait for processor thread
        if self.processor_thread:
            self.processor_thread.join(timeout=2.0)

        logger.info("Cortex: Shutdown complete")


# Global singleton instance
_cortex = None

def get_cortex() -> SierraCortexExecutive:
    """Get the singleton cortex instance"""
    global _cortex
    if _cortex is None:
        _cortex = SierraCortexExecutive()
    return _cortex


# Test execution
if __name__ == "__main__":
    print("="*70)
    print("SIERRA CORTEX EXECUTIVE TEST")
    print("="*70)
    print()

    # Initialize cortex
    cortex = get_cortex()

    # Register mock modules
    class MockVoiceCortex:
        def speak(self, text, priority=3):
            print(f"  [Voice] {text}")
        def speak_crisis(self, text):
            print(f"  [Voice CRISIS] {text}")
        def speak_gentle(self, text):
            print(f"  [Voice Gentle] {text}")

    class MockEmpathyEngine:
        def generate_response(self, text, emotion=None):
            return {
                "detected_emotion": "fear",
                "validation": "I hear your fear",
                "support": "You're not alone"
            }

    class MockBehavioralCapture:
        def assess_danger(self, text, context):
            return {"level": "HIGH", "confidence": 0.85}
        def passive_assessment(self, text):
            return {"level": "SAFE"}

    cortex.register_module("voice_cortex", MockVoiceCortex())
    cortex.register_module("empathy_engine", MockEmpathyEngine())
    cortex.register_module("behavioral_capture", MockBehavioralCapture())

    print("Registered modules:")
    for module_name in cortex.modules.keys():
        print(f"  ✓ {module_name}")
    print()

    # Test 1: Normal emotional support
    print("Test 1: Emotional support request")
    cortex.submit_request(
        request_id="test_1",
        priority=CortexPriority.NORMAL,
        mode=CortexMode.EMOTIONAL_SUPPORT,
        content={"text": "I'm feeling scared"}
    )
    time.sleep(1)

    # Test 2: Crisis intervention
    print("\nTest 2: Crisis request (should interrupt)")
    cortex.submit_request(
        request_id="test_2",
        priority=CortexPriority.CRISIS,
        mode=CortexMode.CRISIS,
        content={"text": "He's coming home angry", "context": {}}
    )
    time.sleep(2)

    # Test 3: Safety planning
    print("\nTest 3: Safety planning request")
    cortex.submit_request(
        request_id="test_3",
        priority=CortexPriority.HIGH,
        mode=CortexMode.SAFETY_PLANNING,
        content={"user_info": {"has_children": True}}
    )
    time.sleep(1)

    # Status
    print("\n" + "="*70)
    print("CORTEX STATUS")
    print("="*70)
    status = cortex.get_status()
    for key, value in status.items():
        print(f"  {key}: {value}")

    print("\n✅ Cortex Executive test complete")
    print("🧠 Sierra's brain is coordinating subsystems")
    print("💜 Infrastructure for safety and healing")

    # Cleanup
    cortex.shutdown()


# ==============================================================================
# © 2025 Everett Nathaniel Christman
# The Christman AI Project — Luma Cognify AI
# All rights reserved. Unauthorized use, replication, or derivative training
# of this material is prohibited.
#
# Core Directive: "How can we help you love yourself more?"
# Autonomy & Alignment Protocol v3.0
# ==============================================================================
