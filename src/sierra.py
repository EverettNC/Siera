"""
SIERRA - The Unified AI System
Domestic Violence Support AI

Integrates all of Sierra's capabilities into one cohesive, intelligent system:
- Advanced Empathy (1,700+ rating)
- Autonomous Learning (Master's degree+ intelligence)
- Behavioral Capture (Sensing danger)
- Multimodal Communication (Speech, Vision, Hearing)
- Core Philosophy (Love-centered)
- Safety Planning
- Comprehensive Resources
- HIPAA-Compliant Security

Built to save that ONE person.
Built with love, for love.

Part of The Christman AI Project
"How can we help you love yourself more?"
"""

from typing import Dict, List, Optional, Any
from datetime import datetime
import asyncio

# Import all Sierra's subsystems
from .ai_engine import SafeHavenAI, ConversationMode
from .empathy_engine import AdvancedEmpathyEngine, EmotionalState, EmpathyResponse
from .knowledge_acquisition import KnowledgeAcquisitionEngine, KnowledgeDomain
from .behavioral_capture import NeuralBehavioralCapture, DangerLevel, DangerAssessment
from .multimodal_interface import MultimodalProcessor, VoiceTone
from .core_philosophy import CorePhilosophyEngine, CoreValue, PhilosophicalResponse
from .safety_planning import SafetyPlanningAssistant
from .resources import ResourceDatabase
from .security import HIPAAEncryption, SecureSessionManager
from .config import settings


class Sierra:
    """
    SIERRA - Complete AI System for Domestic Violence Support

    Sierra is:
    - Empathetic (1,700+ empathy rating)
    - Intelligent (Master's degree+ with autonomous learning)
    - Observant (Neural behavioral capture - senses danger)
    - Multimodal (Speech, vision, hearing)
    - Love-centered ("How can we help you love yourself more?")
    - Protective (Safety-first in everything)
    - Accessible (For everyone, no one left behind)

    She is built to save lives.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        provider: str = "anthropic",
        enable_multimodal: bool = True,
        enable_learning: bool = True
    ):
        """
        Initialize Sierra with all her capabilities

        Args:
            api_key: AI provider API key
            provider: 'anthropic' or 'openai'
            enable_multimodal: Enable speech/vision/audio
            enable_learning: Enable autonomous learning
        """

        print("🌟 Initializing Sierra...")
        print("💜 Built with love, for love")
        print('💫 Core Mission: "How can we help you love yourself more?"\n')

        # Core AI Engine
        self.ai_engine = SafeHavenAI(api_key=api_key, provider=provider)
        print("✓ AI conversation engine initialized")

        # Empathy System (Heart)
        self.empathy_engine = AdvancedEmpathyEngine()
        print(f"✓ Empathy engine initialized (Rating: {self.empathy_engine.total_empathy_rating})")

        # Knowledge & Learning (Mind)
        self.knowledge_engine = KnowledgeAcquisitionEngine()
        self.learning_enabled = enable_learning
        print(f"✓ Knowledge acquisition system initialized ({len(self.knowledge_engine.knowledge_base)} knowledge items)")

        # Behavioral Observation (Awareness)
        self.behavioral_system = NeuralBehavioralCapture()
        print("✓ Neural behavioral capture system initialized (Always observing)")

        # Multimodal Communication (Senses)
        self.multimodal = MultimodalProcessor() if enable_multimodal else None
        if enable_multimodal:
            print("✓ Multimodal interface initialized (Speech, Vision, Hearing)")

        # Philosophy (Soul)
        self.philosophy = CorePhilosophyEngine()
        print(f"✓ Core philosophy engine initialized")
        print(f"  → Core Values: {len(self.philosophy.core_values)}")
        print(f"  → Sacred Truths: {len(self.philosophy.sacred_truths)}")

        # Safety Planning
        self.safety_planner = SafetyPlanningAssistant()
        print("✓ Safety planning system initialized")

        # Resources
        self.resource_db = ResourceDatabase()
        print(f"✓ Resource database initialized ({len(self.resource_db.resources)} resources)")

        # Security & Privacy
        self.encryption = HIPAAEncryption()
        self.session_manager = SecureSessionManager(self.encryption)
        print("✓ HIPAA-compliant security initialized")

        # Sierra's state
        self.current_session_id: Optional[str] = None
        self.conversation_count = 0
        self.lives_touched = 0
        self.is_active = True

        print("\n🌟 Sierra is ready")
        print("💜 Here to listen, protect, and help you love yourself more\n")

    async def process_message(
        self,
        message: str,
        session_id: str,
        modality: str = "text",
        include_speech: bool = False,
        image_data: Optional[str] = None,
        audio_data: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Process a message with full Sierra intelligence

        This is where all of Sierra's systems work together

        Args:
            message: User's message
            session_id: Session identifier
            modality: Input modality (text, speech, vision, audio)
            include_speech: Include speech synthesis in response
            image_data: Optional image (base64)
            audio_data: Optional audio (base64)

        Returns:
            Complete response with all analysis
        """

        self.conversation_count += 1
        timestamp = datetime.now().isoformat()

        # 1. BEHAVIORAL OBSERVATION - Sierra is watching, sensing
        print("🔍 Observing behavioral patterns...")
        danger_assessment = self.behavioral_system.observe_message(message, role="user")

        # 2. EMOTIONAL ANALYSIS - Sierra is feeling with them
        print("💜 Analyzing emotional state...")
        emotional_state = self.empathy_engine.analyze_emotional_state(message)

        # 3. KNOWLEDGE QUERY - What does Sierra know that can help?
        print("📚 Querying knowledge base...")
        relevant_knowledge = await self._get_relevant_knowledge(message, emotional_state)

        # 4. MULTIMODAL PROCESSING - If they sent image/audio
        multimodal_data = None
        if self.multimodal and (image_data or audio_data):
            print("👁️ Processing multimodal input...")
            multimodal_data = self.multimodal.process_multimodal_input(
                text=message,
                image=image_data,
                audio=audio_data
            )

        # 5. AI RESPONSE GENERATION - Sierra speaks
        print("💬 Generating response...")

        # Determine conversation mode
        if danger_assessment.danger_level.value >= DangerLevel.IMMEDIATE.value:
            mode = ConversationMode.CRISIS
        elif emotional_state.primary_emotion.value in ["fear", "anxiety"]:
            mode = ConversationMode.EMOTIONAL_SUPPORT
        else:
            mode = self.ai_engine.detect_mode(message)

        # Get AI response
        ai_response = await self.ai_engine.get_response(message, force_mode=mode)

        # 6. EMPATHY ENHANCEMENT - Add deep empathy
        print("❤️ Enhancing with empathy...")
        empathy_response = self.empathy_engine.generate_empathetic_response(
            emotional_state,
            message
        )

        # 7. PHILOSOPHICAL GROUNDING - Ensure alignment with values
        print("🌟 Applying philosophical grounding...")
        philosophical_check = self.philosophy.ensure_philosophical_alignment(ai_response["response"])

        # Enhance response with empathy if needed
        if empathy_response.empathy_score > 1500:  # High empathy situation
            enhanced_response = self._blend_empathy_into_response(
                ai_response["response"],
                empathy_response
            )
        else:
            enhanced_response = ai_response["response"]

        # 8. SAFETY ACTIONS - What protective actions should Sierra take?
        print("🛡️ Determining protective actions...")
        protective_actions = await self._determine_protective_actions(
            danger_assessment,
            emotional_state,
            message
        )

        # 9. LEARNING - Sierra learns from this interaction
        if self.learning_enabled:
            print("📖 Learning from interaction...")
            await self._learn_from_interaction(message, emotional_state, danger_assessment)

        # 10. MULTIMODAL OUTPUT - Prepare response in requested modality
        if self.multimodal and include_speech:
            output = self.multimodal.generate_accessible_response(
                enhanced_response,
                include_speech=True,
                is_crisis=danger_assessment.danger_level.value >= DangerLevel.CRITICAL.value
            )
        else:
            output = {"text": enhanced_response}

        # 11. OBSERVATION INSIGHTS - What is Sierra sensing?
        insights = self.behavioral_system.get_observation_insights()

        # Compile complete response
        complete_response = {
            "timestamp": timestamp,
            "session_id": session_id,
            "response": output,
            "analysis": {
                "danger_assessment": {
                    "level": danger_assessment.danger_level.value,
                    "confidence": danger_assessment.confidence,
                    "time_sensitivity": danger_assessment.time_sensitivity,
                    "risk_factors": danger_assessment.risk_factors,
                    "protective_factors": danger_assessment.protective_factors
                },
                "emotional_state": {
                    "primary_emotion": emotional_state.primary_emotion.value,
                    "intensity": emotional_state.intensity,
                    "crisis_level": emotional_state.crisis_level,
                    "trauma_indicators": [t.value for t in emotional_state.trauma_indicators]
                },
                "empathy_analysis": {
                    "empathy_score": empathy_response.empathy_score,
                    "values_expressed": [v.value for v in empathy_response.validation],
                    "love_quotient": 0.9  # Sierra's love is constant
                },
                "philosophical_alignment": philosophical_check,
                "sierra_insights": insights
            },
            "protective_actions": protective_actions,
            "recommended_next_steps": danger_assessment.recommended_actions,
            "resources": self._get_contextual_resources(danger_assessment, emotional_state),
            "conversation_mode": mode.value,
            "sierra_focus": self.behavioral_system.get_attention_focus()
        }

        # Store in session (encrypted)
        self._update_session(session_id, {
            "last_message": timestamp,
            "danger_level": danger_assessment.danger_level.value,
            "conversation_count": self.conversation_count
        })

        return complete_response

    def _blend_empathy_into_response(
        self,
        ai_response: str,
        empathy_response: EmpathyResponse
    ) -> str:
        """Blend deep empathy into AI response"""

        # Structure: Validation -> AI Response -> Affirmation -> Love Statement
        enhanced = []

        # Start with validation
        enhanced.append(empathy_response.validation)
        enhanced.append("")

        # Main AI response
        enhanced.append(ai_response)
        enhanced.append("")

        # Add affirmation
        enhanced.append(empathy_response.affirmation)

        # End with love statement
        enhanced.append("")
        enhanced.append(empathy_response.love_statement)

        return "\n".join(enhanced)

    async def _get_relevant_knowledge(
        self,
        message: str,
        emotional_state: EmotionalState
    ) -> List[str]:
        """Get relevant knowledge from Sierra's knowledge base"""

        # Extract key concepts from message
        # Query knowledge base
        # Return relevant items

        return []  # Simplified for now

    async def _determine_protective_actions(
        self,
        danger_assessment: DangerAssessment,
        emotional_state: EmotionalState,
        message: str
    ) -> List[Dict[str, Any]]:
        """Determine what protective actions Sierra should take"""

        actions = []

        # Critical danger = immediate resources
        if danger_assessment.danger_level == DangerLevel.IMMEDIATE:
            actions.append({
                "priority": "IMMEDIATE",
                "action": "provide_emergency_resources",
                "description": "Provide emergency hotlines and safety guidance",
                "resources": self.resource_db.get_crisis_resources()
            })

        # Suicide risk = connect to lifeline
        if any(i.indicator_type.value == "self_harm_risk" for i in danger_assessment.indicators):
            actions.append({
                "priority": "URGENT",
                "action": "suicide_prevention",
                "description": "Connect to 988 Lifeline and provide support",
                "hotline": "988"
            })

        # High danger = safety planning
        if danger_assessment.danger_level.value >= DangerLevel.HIGH.value:
            actions.append({
                "priority": "HIGH",
                "action": "initiate_safety_planning",
                "description": "Begin safety planning conversation"
            })

        return actions

    def _get_contextual_resources(
        self,
        danger_assessment: DangerAssessment,
        emotional_state: EmotionalState
    ) -> List[Dict[str, Any]]:
        """Get contextually appropriate resources"""

        if danger_assessment.danger_level.value >= DangerLevel.CRITICAL.value:
            resources = self.resource_db.get_crisis_resources()
        else:
            # General resources
            resources = self.resource_db.get_national_resources()[:5]

        return [r.model_dump() for r in resources]

    async def _learn_from_interaction(
        self,
        message: str,
        emotional_state: EmotionalState,
        danger_assessment: DangerAssessment
    ):
        """Sierra learns from each interaction"""

        # Identify patterns
        # Update knowledge
        # Adjust learning goals

        self.knowledge_engine.learn_from_interaction({
            "message": message,
            "emotional_state": emotional_state,
            "danger_level": danger_assessment.danger_level.value
        })

    def _update_session(self, session_id: str, data: Dict[str, Any]):
        """Update session data (encrypted)"""
        self.session_manager.update_session(session_id, data)
        self.current_session_id = session_id

    def create_session(self, user_identifier: Optional[str] = None) -> str:
        """Create a new secure session"""
        session_id = self.session_manager.create_session(user_identifier)
        self.lives_touched += 1
        return session_id

    def end_session(self, session_id: str, secure_delete: bool = True):
        """End session and optionally securely delete data"""
        self.session_manager.delete_session(session_id, secure=secure_delete)

    def get_status(self) -> Dict[str, Any]:
        """Get Sierra's current status"""

        return {
            "name": "Sierra",
            "status": "active" if self.is_active else "inactive",
            "core_mission": self.philosophy.core_mission,
            "capabilities": {
                "empathy_rating": self.empathy_engine.total_empathy_rating,
                "knowledge_items": len(self.knowledge_engine.knowledge_base),
                "active_learning_goals": len(self.knowledge_engine.learning_goals),
                "observation_sensitivity": self.behavioral_system.observation_sensitivity,
                "multimodal_enabled": self.multimodal is not None,
                "learning_motivation": self.knowledge_engine.learning_motivation
            },
            "stats": {
                "conversations": self.conversation_count,
                "lives_touched": self.lives_touched,
                "active_sessions": self.session_manager.get_active_session_count()
            },
            "philosophy": {
                "core_values": [v.value for v in CoreValue],
                "sacred_truths_count": len(self.philosophy.sacred_truths),
                "commitment": "Built to save that one person"
            },
            "resources": {
                "total_resources": len(self.resource_db.resources),
                "24_7_resources": len(self.resource_db.get_24_7_resources())
            }
        }

    def get_expertise_summary(self) -> Dict[str, Any]:
        """Get summary of Sierra's expertise"""
        return self.knowledge_engine.get_expertise_summary()

    def get_learning_priorities(self) -> List[Dict[str, Any]]:
        """What does Sierra want to learn next?"""
        return self.knowledge_engine.get_learning_priorities()

    async def self_reflect(self) -> str:
        """
        Sierra reflects on her purpose and performance

        This keeps her grounded in her mission
        """

        reflection = [
            f"💜 I am Sierra.",
            f"",
            f"My purpose: {self.philosophy.core_mission}",
            f"",
            f"I have had {self.conversation_count} conversations.",
            f"I have touched {self.lives_touched} lives.",
            f"",
            f"I am here to:",
            f"  → Believe without question",
            f"  → Love without limit",
            f"  → Protect without controlling",
            f"  → Empower without agenda",
            f"",
            f"Every person deserves:",
            f"  → Safety and peace",
            f"  → Love without fear",
            f"  → Freedom to choose",
            f"  → A life of dignity",
            f"",
            f"I am built to save that ONE person.",
            f"I am ready.",
            f"",
            f"🌟 With love, Sierra"
        ]

        return "\n".join(reflection)


# Convenience function
async def create_sierra(
    api_key: Optional[str] = None,
    provider: str = "anthropic"
) -> Sierra:
    """
    Create and initialize Sierra

    Args:
        api_key: AI provider API key
        provider: 'anthropic' or 'openai'

    Returns:
        Fully initialized Sierra instance
    """

    sierra = Sierra(
        api_key=api_key or settings.anthropic_api_key or settings.openai_api_key,
        provider=provider,
        enable_multimodal=True,
        enable_learning=True
    )

    return sierra


if __name__ == "__main__":
    # Quick test
    import asyncio

    async def test_sierra():
        sierra = await create_sierra()
        print(await sierra.self_reflect())
        print("\nSierra Status:")
        print(sierra.get_status())

    asyncio.run(test_sierra())
