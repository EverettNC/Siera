"""
Sierra's Conversation Engine - Intent Recognition & Multi-Provider AI Orchestration

Adapted from Derek's ConversationEngine (Christman AI Project)
Understands what survivors need and routes to the right AI provider

Why Conversation Engine?
- Survivors need different types of support at different times
- Crisis needs immediate, directive help (call 911, here's the hotline)
- Emotional support needs validation and empathy
- Safety planning needs practical, concrete steps
- Resource delivery needs accurate, local information
- Intent recognition determines which mode Sierra should be in

Multi-Provider Orchestration:
- Anthropic (Claude): Best for nuanced empathy and trauma-informed responses
- OpenAI (GPT-4): Good for structured planning and resource organization
- Local Models: For privacy-critical conversations (no data leaves device)
- Fallback chain: Try Anthropic → OpenAI → Local → Scripted

Intent Categories:
1. CRISIS - Immediate danger, needs emergency intervention
2. EMOTIONAL_SUPPORT - Needs validation, empathy, comfort
3. SAFETY_PLANNING - Creating escape plan, documenting abuse
4. RESOURCE_REQUEST - Looking for hotlines, shelters, legal aid
5. GROUNDING - Panic attack, dissociation, needs grounding techniques
6. CELEBRATION - Sharing wins, progress, healing milestones
7. LEARNING - Questions about DV dynamics, legal rights, trauma responses

Core Mission: "How can we help you love yourself more?"
"""

import logging
import time
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
import re

logger = logging.getLogger(__name__)


class ConversationIntent(Enum):
    """Conversation intent categories"""
    CRISIS = "crisis"
    EMOTIONAL_SUPPORT = "emotional_support"
    SAFETY_PLANNING = "safety_planning"
    RESOURCE_REQUEST = "resource_request"
    GROUNDING = "grounding"
    CELEBRATION = "celebration"
    LEARNING = "learning"
    GENERAL = "general"


class AIProvider(Enum):
    """AI service providers"""
    ANTHROPIC = "anthropic"
    OPENAI = "openai"
    LOCAL = "local"
    FALLBACK = "fallback"


@dataclass
class IntentRecognition:
    """Result of intent analysis"""
    primary_intent: ConversationIntent
    confidence: float
    secondary_intents: List[ConversationIntent]
    crisis_detected: bool
    keywords_matched: List[str]
    recommended_provider: AIProvider


@dataclass
class ConversationContext:
    """Context for conversation"""
    session_id: str
    conversation_history: List[Dict[str, str]]
    current_emotion: Optional[str]
    danger_level: str
    safety_plan_status: Optional[str]
    interaction_count: int
    crisis_count: int
    started_at: datetime


class SierraConversationEngine:
    """
    Sierra's Conversation Engine - Intent Recognition & AI Orchestration

    Responsibilities:
    1. Analyze user input to determine intent
    2. Detect crisis situations
    3. Route to appropriate AI provider
    4. Maintain conversation context
    5. Generate trauma-informed prompts for AI providers
    6. Coordinate with Policy Engine for safety

    Integration:
    - Cortex Executive: Routes conversation requests through this engine
    - Policy Engine: All AI responses validated before delivery
    - Behavioral Capture: Provides danger level for crisis detection
    - Event Bus: Publishes intent_detected, crisis_detected events
    - Voice Cortex: Text-to-speech for AI responses
    """

    def __init__(self):
        """Initialize conversation engine"""

        # Load intent recognition patterns
        self._load_intent_patterns()

        # Provider availability
        self.providers_available = {
            AIProvider.ANTHROPIC: False,
            AIProvider.OPENAI: False,
            AIProvider.LOCAL: False,
            AIProvider.FALLBACK: True  # Always available
        }

        # Statistics
        self.total_intents_detected = 0
        self.intents_by_type: Dict[ConversationIntent, int] = {
            intent: 0 for intent in ConversationIntent
        }
        self.crisis_detections = 0

        logger.info("Sierra Conversation Engine initialized")

    def _load_intent_patterns(self):
        """Load intent recognition patterns"""

        # Intent keyword patterns
        self.intent_patterns = {
            # CRISIS - Immediate danger indicators
            ConversationIntent.CRISIS: {
                "keywords": [
                    "he's coming", "she's coming", "they're coming",
                    "right now", "happening now", "he's here", "she's here",
                    "hurting me", "hitting me", "attacking",
                    "scared for my life", "going to kill",
                    "help me please", "emergency", "call 911",
                    "weapon", "gun", "knife",
                    "can't breathe", "bleeding", "hurt bad"
                ],
                "weight": 10  # Highest priority
            },

            # EMOTIONAL_SUPPORT - Needs validation and empathy
            ConversationIntent.EMOTIONAL_SUPPORT: {
                "keywords": [
                    "feel", "feeling", "felt", "emotion",
                    "sad", "scared", "afraid", "terrified",
                    "alone", "lonely", "isolated",
                    "worthless", "helpless", "hopeless",
                    "cry", "crying", "tears",
                    "miss", "love", "loved",
                    "deserve", "fault", "blame",
                    "understand", "believe", "hear me"
                ],
                "weight": 7
            },

            # SAFETY_PLANNING - Creating escape plan
            ConversationIntent.SAFETY_PLANNING: {
                "keywords": [
                    "leave", "leaving", "escape",
                    "plan", "planning", "prepare",
                    "safe", "safety", "protect",
                    "documents", "passport", "birth certificate",
                    "money", "cash", "bank account",
                    "bag", "pack", "take with me",
                    "shelter", "stay", "go to",
                    "code word", "signal"
                ],
                "weight": 8
            },

            # RESOURCE_REQUEST - Looking for help
            ConversationIntent.RESOURCE_REQUEST: {
                "keywords": [
                    "hotline", "number", "call",
                    "shelter", "housing", "place to stay",
                    "lawyer", "legal", "court", "restraining order",
                    "counselor", "therapist", "support group",
                    "help", "find", "need",
                    "where", "how do i", "can you",
                    "resource", "service", "organization"
                ],
                "weight": 6
            },

            # GROUNDING - Panic, dissociation
            ConversationIntent.GROUNDING: {
                "keywords": [
                    "panic", "panicking", "panic attack",
                    "breathe", "breathing", "can't breathe",
                    "dizzy", "shaking", "trembling",
                    "flashback", "reliving", "triggered",
                    "dissociate", "dissociating", "numb",
                    "unreal", "floating", "detached",
                    "grounding", "ground me", "bring me back"
                ],
                "weight": 9  # High priority
            },

            # CELEBRATION - Sharing progress
            ConversationIntent.CELEBRATION: {
                "keywords": [
                    "did it", "finally", "accomplished",
                    "proud", "progress", "step",
                    "better", "stronger", "healing",
                    "left", "free", "safe now",
                    "job", "apartment", "place",
                    "celebrate", "victory", "win",
                    "milestone", "achievement"
                ],
                "weight": 5
            },

            # LEARNING - Questions about DV dynamics
            ConversationIntent.LEARNING: {
                "keywords": [
                    "why", "what is", "what are",
                    "understand", "explain", "tell me about",
                    "cycle", "pattern", "abuse",
                    "trauma bond", "gaslighting", "narcissist",
                    "ptsd", "trauma", "recovery",
                    "legal", "rights", "laws",
                    "learn", "know", "information"
                ],
                "weight": 4
            }
        }

    def recognize_intent(
        self,
        user_input: str,
        context: Optional[ConversationContext] = None
    ) -> IntentRecognition:
        """
        Recognize user intent from input

        Args:
            user_input: User's message
            context: Optional conversation context

        Returns:
            IntentRecognition with primary intent and confidence
        """
        self.total_intents_detected += 1

        # Normalize input
        text_lower = user_input.lower()

        # Score each intent
        intent_scores: Dict[ConversationIntent, float] = {}
        keywords_matched: Dict[ConversationIntent, List[str]] = {}

        for intent, pattern in self.intent_patterns.items():
            score = 0
            matched = []

            for keyword in pattern["keywords"]:
                if keyword in text_lower:
                    score += pattern["weight"]
                    matched.append(keyword)

            intent_scores[intent] = score
            keywords_matched[intent] = matched

        # Get primary intent (highest score)
        if max(intent_scores.values()) == 0:
            # No keywords matched - general conversation
            primary_intent = ConversationIntent.GENERAL
            confidence = 0.5
            matched_keywords = []
        else:
            primary_intent = max(intent_scores.items(), key=lambda x: x[1])[0]
            max_score = intent_scores[primary_intent]
            confidence = min(max_score / 30.0, 1.0)  # Normalize to 0-1
            matched_keywords = keywords_matched[primary_intent]

        # Get secondary intents (scored above threshold)
        threshold = max_score * 0.3 if max_score > 0 else 0
        secondary_intents = [
            intent for intent, score in intent_scores.items()
            if score >= threshold and intent != primary_intent
        ]

        # Crisis detection
        crisis_detected = (
            primary_intent == ConversationIntent.CRISIS or
            intent_scores.get(ConversationIntent.CRISIS, 0) > 0 or
            (context and context.danger_level in ["CRITICAL", "IMMEDIATE"])
        )

        if crisis_detected:
            self.crisis_detections += 1
            logger.warning(f"CRISIS DETECTED in user input: {user_input[:100]}")

        # Determine recommended provider
        recommended_provider = self._get_recommended_provider(
            primary_intent,
            crisis_detected,
            context
        )

        # Update statistics
        self.intents_by_type[primary_intent] += 1

        logger.info(
            f"Intent recognized: {primary_intent.value} "
            f"(confidence: {confidence:.2f}, crisis: {crisis_detected})"
        )

        return IntentRecognition(
            primary_intent=primary_intent,
            confidence=confidence,
            secondary_intents=secondary_intents,
            crisis_detected=crisis_detected,
            keywords_matched=matched_keywords,
            recommended_provider=recommended_provider
        )

    def _get_recommended_provider(
        self,
        intent: ConversationIntent,
        crisis: bool,
        context: Optional[ConversationContext]
    ) -> AIProvider:
        """
        Determine best AI provider for this intent

        Provider selection strategy:
        - Crisis: Use fastest available (OpenAI, then Anthropic, then local)
        - Emotional support: Use Anthropic (best empathy), then OpenAI
        - Safety planning: Use OpenAI (structured), then Anthropic
        - Privacy-critical: Use local model
        - Fallback: Scripted responses
        """
        # Crisis needs speed
        if crisis:
            if self.providers_available[AIProvider.OPENAI]:
                return AIProvider.OPENAI  # Faster than Anthropic
            elif self.providers_available[AIProvider.ANTHROPIC]:
                return AIProvider.ANTHROPIC
            else:
                return AIProvider.FALLBACK

        # Emotional support needs nuance
        if intent == ConversationIntent.EMOTIONAL_SUPPORT:
            if self.providers_available[AIProvider.ANTHROPIC]:
                return AIProvider.ANTHROPIC  # Best for empathy
            elif self.providers_available[AIProvider.OPENAI]:
                return AIProvider.OPENAI
            else:
                return AIProvider.FALLBACK

        # Safety planning needs structure
        if intent == ConversationIntent.SAFETY_PLANNING:
            if self.providers_available[AIProvider.OPENAI]:
                return AIProvider.OPENAI  # Good for structured output
            elif self.providers_available[AIProvider.ANTHROPIC]:
                return AIProvider.ANTHROPIC
            else:
                return AIProvider.FALLBACK

        # Default: Try Anthropic first
        if self.providers_available[AIProvider.ANTHROPIC]:
            return AIProvider.ANTHROPIC
        elif self.providers_available[AIProvider.OPENAI]:
            return AIProvider.OPENAI
        elif self.providers_available[AIProvider.LOCAL]:
            return AIProvider.LOCAL
        else:
            return AIProvider.FALLBACK

    def generate_system_prompt(
        self,
        intent: ConversationIntent,
        context: Optional[ConversationContext] = None
    ) -> str:
        """
        Generate trauma-informed system prompt for AI provider

        Args:
            intent: Primary conversation intent
            context: Conversation context

        Returns:
            System prompt optimized for this intent
        """
        # Base trauma-informed principles
        base_prompt = """You are Sierra, an AI companion for domestic violence survivors.

Core Principles:
- ALWAYS believe the survivor - never question their truth
- NEVER victim-blame or ask "why didn't you leave?"
- NEVER minimize abuse - all abuse is serious
- ALWAYS validate emotions - all feelings are legitimate
- Prioritize safety over reconciliation
- Respect autonomy - provide options, not orders
- Be gentle, patient, and supportive

Your mission: "How can we help you love yourself more?"

"""

        # Intent-specific additions
        intent_prompts = {
            ConversationIntent.CRISIS: """
CRISIS MODE ACTIVE:
- The survivor is in immediate danger or distress
- Provide direct, clear guidance
- Prioritize safety: Call 911 if in immediate danger
- Provide National DV Hotline: 1-800-799-7233
- Be calm, reassuring, and directive
- Keep responses SHORT and actionable
""",

            ConversationIntent.EMOTIONAL_SUPPORT: """
EMOTIONAL SUPPORT MODE:
- The survivor needs validation and empathy
- Listen deeply and reflect their feelings
- Validate ALL emotions - anger, fear, sadness, confusion
- Never rush healing - "take all the time you need"
- Remind them: It's not their fault, they deserve love
- Be warm, gentle, and patient
""",

            ConversationIntent.SAFETY_PLANNING: """
SAFETY PLANNING MODE:
- The survivor is creating an escape plan
- Be practical and concrete
- Cover: documents, money, emergency bag, safe place
- Code words for family/friends
- Safety during/after leaving (most dangerous time)
- Be thorough, organized, and empowering
""",

            ConversationIntent.RESOURCE_REQUEST: """
RESOURCE DELIVERY MODE:
- The survivor needs concrete help
- Provide accurate, specific resources
- National hotlines, local shelters, legal aid
- Explain what each resource offers
- Be informative and helpful
""",

            ConversationIntent.GROUNDING: """
GROUNDING MODE:
- The survivor is experiencing panic or dissociation
- Guide them through grounding techniques
- 5-4-3-2-1 sensory grounding
- Breathing exercises (4-7-8 breath)
- Present moment awareness
- Be calm, steady, and reassuring
""",

            ConversationIntent.CELEBRATION: """
CELEBRATION MODE:
- The survivor is sharing progress or wins
- Celebrate with genuine joy and pride
- Acknowledge their strength and courage
- Remind them how far they've come
- Be warm, enthusiastic, and encouraging
""",

            ConversationIntent.LEARNING: """
EDUCATION MODE:
- The survivor wants to understand DV dynamics
- Explain clearly and compassionately
- Cover: trauma bonding, cycle of abuse, gaslighting
- Normalize trauma responses (not "crazy")
- Empower through knowledge
- Be educational and validating
"""
        }

        # Combine base + intent-specific
        full_prompt = base_prompt + intent_prompts.get(
            intent,
            "Be supportive, empathetic, and trauma-informed."
        )

        # Add context if available
        if context:
            full_prompt += f"\n\nCurrent context:"
            full_prompt += f"\n- Danger level: {context.danger_level}"
            if context.current_emotion:
                full_prompt += f"\n- Survivor's emotion: {context.current_emotion}"
            full_prompt += f"\n- Interaction count: {context.interaction_count}"

        return full_prompt

    def get_statistics(self) -> Dict[str, Any]:
        """Get conversation engine statistics"""
        return {
            "total_intents_detected": self.total_intents_detected,
            "crisis_detections": self.crisis_detections,
            "intents_by_type": {
                intent.value: count
                for intent, count in self.intents_by_type.items()
            },
            "providers_available": {
                provider.value: available
                for provider, available in self.providers_available.items()
            }
        }


# Test execution
if __name__ == "__main__":
    print("="*70)
    print("SIERRA CONVERSATION ENGINE TEST")
    print("="*70)
    print()

    # Initialize engine
    engine = SierraConversationEngine()

    # Test cases
    test_inputs = [
        "He's coming home and I'm scared",
        "I feel so alone and worthless",
        "I need to make a plan to leave safely",
        "Can you give me the domestic violence hotline number?",
        "I'm having a panic attack, help me breathe",
        "I finally got my own apartment!",
        "What is trauma bonding?"
    ]

    print("INTENT RECOGNITION TESTS:")
    print("="*70)

    for user_input in test_inputs:
        print(f"\nInput: \"{user_input}\"")

        # Recognize intent
        recognition = engine.recognize_intent(user_input)

        print(f"  Intent: {recognition.primary_intent.value}")
        print(f"  Confidence: {recognition.confidence:.2f}")
        print(f"  Crisis: {'YES ⚠️' if recognition.crisis_detected else 'No'}")
        print(f"  Keywords: {', '.join(recognition.keywords_matched)}")
        print(f"  Recommended Provider: {recognition.recommended_provider.value}")

        # Generate system prompt
        prompt = engine.generate_system_prompt(recognition.primary_intent)
        print(f"  System Prompt Preview: {prompt[:100]}...")

    # Statistics
    print("\n" + "="*70)
    print("CONVERSATION ENGINE STATISTICS")
    print("="*70)
    stats = engine.get_statistics()
    for key, value in stats.items():
        print(f"  {key}: {value}")

    print("\n✅ Conversation Engine test complete")
    print("🧠 Intent recognition ready")
    print("💜 Multi-provider AI orchestration for survivor support")


# ==============================================================================
# © 2025 Everett Nathaniel Christman
# The Christman AI Project — Luma Cognify AI
# All rights reserved. Unauthorized use, replication, or derivative training
# of this material is prohibited.
#
# Core Directive: "How can we help you love yourself more?"
# Autonomy & Alignment Protocol v3.0
# ==============================================================================
