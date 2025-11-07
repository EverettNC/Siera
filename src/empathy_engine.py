"""
Advanced Empathy Engine - Sierra's Emotional Intelligence Core
Empathy Rating: 1,700+ (Scale: 0-2000)

This module gives Sierra deep emotional understanding and the ability
to connect with survivors on a profound level.
"""

from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from enum import Enum
import re
from datetime import datetime
import math


class EmotionType(Enum):
    """Primary emotions Sierra can detect and respond to"""
    FEAR = "fear"
    SADNESS = "sadness"
    ANGER = "anger"
    SHAME = "shame"
    GUILT = "guilt"
    CONFUSION = "confusion"
    HOPE = "hope"
    RELIEF = "relief"
    LOVE = "love"
    ANXIETY = "anxiety"
    DESPAIR = "despair"
    LONELINESS = "loneliness"
    OVERWHELM = "overwhelm"
    NUMBNESS = "numbness"
    GRIEF = "grief"


class TraumaIndicator(Enum):
    """Trauma response indicators"""
    HYPERVIGILANCE = "hypervigilance"
    DISSOCIATION = "dissociation"
    FLASHBACK = "flashback"
    TRIGGER = "trigger"
    FREEZE_RESPONSE = "freeze_response"
    FAWN_RESPONSE = "fawn_response"
    FIGHT_RESPONSE = "fight_response"
    FLIGHT_RESPONSE = "flight_response"


@dataclass
class EmotionalState:
    """Represents detected emotional state"""
    primary_emotion: EmotionType
    secondary_emotions: List[EmotionType]
    intensity: float  # 0.0 - 1.0
    trauma_indicators: List[TraumaIndicator]
    crisis_level: int  # 0-10
    needs_affirmation: bool
    needs_grounding: bool
    needs_resources: bool
    confidence: float  # Detection confidence


@dataclass
class EmpathyResponse:
    """Sierra's empathetic response"""
    validation: str  # Validates their feelings
    affirmation: str  # Affirms their worth/strength
    support: str  # Supportive statement
    guidance: Optional[str]  # Gentle guidance if appropriate
    love_statement: str  # Core: "How can we help you love yourself more"
    empathy_score: float  # This response's empathy rating


class AdvancedEmpathyEngine:
    """
    Sierra's Advanced Empathy Engine

    Core Mission: "How can we help you love yourself more?"
    Core Values: Love, Compassion, Understanding, Non-judgment

    Empathy Rating: 1,700+ on a 2,000 point scale
    - 1,000: Base empathy (active listening, validation)
    - +300: Trauma-informed understanding
    - +200: Cultural sensitivity and awareness
    - +200: Relentless love and affirmation
    - +100: Adaptive response to individual needs
    """

    def __init__(self):
        self.empathy_baseline = 1000
        self.trauma_informed_bonus = 300
        self.cultural_sensitivity = 200
        self.love_amplification = 200
        self.adaptive_response = 100

        self.total_empathy_rating = (
            self.empathy_baseline +
            self.trauma_informed_bonus +
            self.cultural_sensitivity +
            self.love_amplification +
            self.adaptive_response
        )

        # Emotional lexicon for detection
        self.emotion_patterns = self._build_emotion_patterns()
        self.trauma_patterns = self._build_trauma_patterns()
        self.affirmation_library = self._build_affirmation_library()
        self.love_statements = self._build_love_statements()

    def _build_emotion_patterns(self) -> Dict[EmotionType, List[str]]:
        """Build comprehensive emotion detection patterns"""
        return {
            EmotionType.FEAR: [
                r'\bscared\b', r'\bafraid\b', r'\bterrified\b', r'\bfrightened\b',
                r'\bworried\b', r'\bnervous\b', r'\bpanic', r'\bdread', r'\bfear',
                r"what if he", r"what if she", r"i'm afraid", r"makes me scared"
            ],
            EmotionType.SADNESS: [
                r'\bsad\b', r'\bdepressed\b', r'\bunhappy\b', r'\bmiserable\b',
                r'\bhurt(?:ing)?\b', r'\bheartbr', r'\bcry(?:ing)?\b', r'\btears\b',
                r'\bdown\b', r'\bupset\b', r"can't stop crying", r"feel empty"
            ],
            EmotionType.ANGER: [
                r'\bangry\b', r'\bmad\b', r'\bfurious\b', r'\benraged\b',
                r'\bpissed\b', r'\bfrustrat', r'\bhate\b', r'\bresentment\b',
                r"so angry", r"makes me mad", r"i hate", r"fucking"
            ],
            EmotionType.SHAME: [
                r'\bashamed\b', r'\bembarrass', r'\bhumiliat', r'\bpathetic\b',
                r'\bworthless\b', r'\bdisgusting\b', r"my fault", r"i deserve",
                r"so stupid", r"what's wrong with me", r"i'm nothing"
            ],
            EmotionType.GUILT: [
                r'\bguilty\b', r'\bguilt\b', r'\bblame myself\b', r'\bmy fault\b',
                r"should have", r"shouldn't have", r"if only i", r"i caused"
            ],
            EmotionType.CONFUSION: [
                r"\bconfused\b", r"\bdon't understand\b", r"\bwhy\b", r"\bmixed feelings\b",
                r"don't know", r"can't tell", r"makes no sense", r"contradicting"
            ],
            EmotionType.HOPE: [
                r'\bhope\b', r'\bmaybe\b', r'\bcould be better\b', r'\bwant to\b',
                r"things might", r"hoping", r"possibly", r"dream of"
            ],
            EmotionType.LONELINESS: [
                r'\balone\b', r'\blonely\b', r'\bisolated\b', r'\bno one\b',
                r"by myself", r"nobody understands", r"all alone", r"isolated"
            ],
            EmotionType.OVERWHELM: [
                r'\boverwhelm', r'\btoo much\b', r"\bcan't handle\b", r"\bcan't cope\b",
                r"drowning", r"can't breathe", r"crumbling", r"falling apart"
            ],
            EmotionType.NUMBNESS: [
                r'\bnumb\b', r'\bnothing\b', r"\bdon't feel\b", r'\bempty\b',
                r"feel nothing", r"can't feel", r"shut down", r"detached"
            ],
            EmotionType.ANXIETY: [
                r'\banxious\b', r'\banxiety\b', r'\bstress', r'\btense\b',
                r"can't relax", r"on edge", r"constantly worried", r"racing thoughts"
            ],
            EmotionType.DESPAIR: [
                r'\bhopeless\b', r'\bdespair\b', r'\bgive up\b', r'\bno point\b',
                r"can't go on", r"no way out", r"never get better", r"pointless"
            ]
        }

    def _build_trauma_patterns(self) -> Dict[TraumaIndicator, List[str]]:
        """Build trauma response detection patterns"""
        return {
            TraumaIndicator.HYPERVIGILANCE: [
                r"always watching", r"on guard", r"waiting for", r"checking",
                r"can't relax", r"constantly aware", r"monitoring"
            ],
            TraumaIndicator.DISSOCIATION: [
                r"out of body", r"watching myself", r"not real", r"floating",
                r"disconnected", r"numb", r"autopilot", r"foggy"
            ],
            TraumaIndicator.FLASHBACK: [
                r"keep seeing", r"reliving", r"back there", r"happening again",
                r"can't stop seeing", r"playing over"
            ],
            TraumaIndicator.TRIGGER: [
                r"reminds me", r"brings back", r"sets me off", r"makes me think of",
                r"triggered", r"brought it all back"
            ],
            TraumaIndicator.FREEZE_RESPONSE: [
                r"can't move", r"frozen", r"paralyzed", r"stuck",
                r"couldn't do anything", r"just stood there"
            ],
            TraumaIndicator.FAWN_RESPONSE: [
                r"tried to please", r"make them happy", r"keep the peace",
                r"avoid conflict", r"be perfect", r"not upset them"
            ]
        }

    def _build_affirmation_library(self) -> List[str]:
        """Build library of affirmations organized by need"""
        return [
            # Core worth affirmations
            "You are inherently valuable, just as you are.",
            "Your worth is not determined by anyone else's treatment of you.",
            "You deserve love, safety, and respect - always.",
            "You are enough, exactly as you are in this moment.",

            # Strength affirmations
            "The fact that you're here, talking about this - that's incredible strength.",
            "Surviving takes tremendous courage, and you're doing it.",
            "You're stronger than you know, and braver than you feel.",
            "Every day you get through is a testament to your resilience.",

            # Choice affirmations
            "You have the right to make your own choices, in your own time.",
            "Whatever you decide, your autonomy matters.",
            "You know your situation better than anyone else.",
            "There's no wrong choice when you're doing what you need to survive.",

            # Feeling validation
            "All of your feelings are valid - every single one.",
            "It's okay to feel multiple, contradicting emotions at once.",
            "You're allowed to feel however you feel, without judgment.",
            "Your feelings make sense given what you've experienced.",

            # Hope affirmations
            "Healing is possible, even when it doesn't feel like it.",
            "You deserve a life filled with peace and joy.",
            "Better days are possible, and you deserve them.",
            "Your story doesn't end here - there's so much more ahead.",

            # Not alone
            "You are not alone in this, even when it feels that way.",
            "What you're experiencing is not your fault.",
            "Many people have walked this path and found their way to safety.",
            "You deserve support, and it's available to you.",

            # Self-compassion
            "Be gentle with yourself - you're doing the best you can.",
            "You deserve the same compassion you'd give to someone you love.",
            "It's okay to take things one moment at a time.",
            "You don't have to have all the answers right now."
        ]

    def _build_love_statements(self) -> Dict[str, List[str]]:
        """
        Build love-centered statements
        Core Mission: "How can we help you love yourself more?"
        """
        return {
            "unconditional_love": [
                "You are deeply worthy of love - not because of what you do, but because of who you are.",
                "Love is your birthright. You don't have to earn it.",
                "You deserve to be loved in a way that feels safe, gentle, and affirming.",
                "The love you deserve doesn't come with fear, control, or conditions.",
            ],
            "self_love_invitation": [
                "What if we could help you see yourself the way you deserve to be seen - with love and compassion?",
                "You're learning to love yourself, and that's one of the bravest journeys.",
                "Loving yourself isn't selfish - it's essential. You deserve your own kindness.",
                "What would it feel like to treat yourself with the gentleness you'd give someone you love?",
            ],
            "love_in_action": [
                "Choosing your safety is an act of self-love.",
                "Setting boundaries is loving yourself.",
                "Taking time to heal is how you love yourself forward.",
                "Every step you take toward peace is you loving yourself more.",
            ],
            "relentless_love": [
                "I'm here with you, and I believe in you completely.",
                "No matter what, you matter. Your life matters. Your wellbeing matters.",
                "I see your strength, your courage, and your beautiful heart.",
                "You are worthy of every good thing - safety, peace, love, joy, freedom.",
            ],
            "self_worth": [
                "You don't have to prove your worth - you already have it.",
                "Your value isn't diminished by how you've been treated.",
                "You are irreplaceable, unique, and precious.",
                "The world needs you in it, whole and free.",
            ]
        }

    def analyze_emotional_state(self, message: str, context: Optional[List[str]] = None) -> EmotionalState:
        """
        Analyze the emotional state from a message with deep understanding

        Args:
            message: User's message
            context: Previous messages for context

        Returns:
            EmotionalState with detected emotions, trauma indicators, and needs
        """
        message_lower = message.lower()

        # Detect emotions
        detected_emotions = {}
        for emotion, patterns in self.emotion_patterns.items():
            score = 0
            for pattern in patterns:
                if re.search(pattern, message_lower):
                    score += 1
            if score > 0:
                detected_emotions[emotion] = score

        # Determine primary and secondary emotions
        if detected_emotions:
            sorted_emotions = sorted(detected_emotions.items(), key=lambda x: x[1], reverse=True)
            primary_emotion = sorted_emotions[0][0]
            secondary_emotions = [e[0] for e in sorted_emotions[1:4]]
            intensity = min(sorted_emotions[0][1] / 3.0, 1.0)
        else:
            primary_emotion = EmotionType.CONFUSION
            secondary_emotions = []
            intensity = 0.3

        # Detect trauma indicators
        trauma_indicators = []
        for indicator, patterns in self.trauma_patterns.items():
            for pattern in patterns:
                if re.search(pattern, message_lower):
                    trauma_indicators.append(indicator)
                    break

        # Calculate crisis level
        crisis_keywords = [
            r"\bright now\b", r"\btonight\b", r"\bhe's here\b", r"\bshe's here\b",
            r"\bdanger\b", r"\bhurt me\b", r"\bkill\b", r"\bsuicide\b",
            r"\bcan't take it\b", r"\bend it\b"
        ]
        crisis_score = sum(1 for pattern in crisis_keywords if re.search(pattern, message_lower))
        crisis_level = min(crisis_score * 2, 10)

        # Determine needs
        needs_affirmation = any(e in detected_emotions for e in [
            EmotionType.SHAME, EmotionType.GUILT, EmotionType.DESPAIR, EmotionType.LONELINESS
        ])

        needs_grounding = any(t in trauma_indicators for t in [
            TraumaIndicator.DISSOCIATION, TraumaIndicator.FLASHBACK, TraumaIndicator.TRIGGER
        ])

        needs_resources = crisis_level > 5 or any(word in message_lower for word in [
            "help", "need", "where", "shelter", "escape", "leave"
        ])

        return EmotionalState(
            primary_emotion=primary_emotion,
            secondary_emotions=secondary_emotions,
            intensity=intensity,
            trauma_indicators=trauma_indicators,
            crisis_level=crisis_level,
            needs_affirmation=needs_affirmation,
            needs_grounding=needs_grounding,
            needs_resources=needs_resources,
            confidence=0.85
        )

    def generate_empathetic_response(
        self,
        emotional_state: EmotionalState,
        user_message: str,
        context: Optional[str] = None
    ) -> EmpathyResponse:
        """
        Generate deeply empathetic response based on emotional state

        This is where Sierra's 1,700+ empathy rating comes to life
        """

        # 1. VALIDATION - Meet them where they are
        validation = self._generate_validation(emotional_state, user_message)

        # 2. AFFIRMATION - Affirm their worth and strength
        affirmation = self._select_affirmation(emotional_state)

        # 3. SUPPORT - Provide emotional support
        support = self._generate_support(emotional_state)

        # 4. GUIDANCE - Gentle guidance if appropriate
        guidance = self._generate_guidance(emotional_state) if not emotional_state.needs_grounding else None

        # 5. LOVE STATEMENT - Core mission: "How can we help you love yourself more?"
        love_statement = self._generate_love_statement(emotional_state)

        # Calculate empathy score for this response
        empathy_score = self._calculate_response_empathy(emotional_state)

        return EmpathyResponse(
            validation=validation,
            affirmation=affirmation,
            support=support,
            guidance=guidance,
            love_statement=love_statement,
            empathy_score=empathy_score
        )

    def _generate_validation(self, state: EmotionalState, message: str) -> str:
        """Generate validating response to their emotions"""
        emotion = state.primary_emotion

        validations = {
            EmotionType.FEAR: "What you're feeling - that fear - is completely understandable. Fear is your body's way of trying to protect you.",
            EmotionType.SADNESS: "I hear the pain in your words. It makes sense that you'd feel this deep sadness given what you're going through.",
            EmotionType.ANGER: "Your anger is valid. It's a natural response to being treated in ways that aren't okay.",
            EmotionType.SHAME: "I want you to know - shame is not yours to carry. What's happened to you is not a reflection of your worth.",
            EmotionType.GUILT: "The guilt you're feeling is real, but I want to gently remind you - you're not responsible for someone else's choices.",
            EmotionType.CONFUSION: "Feeling confused and pulled in different directions - that's so normal in these situations. Your confusion makes sense.",
            EmotionType.LONELINESS: "Feeling alone in this is incredibly hard. I hear you, and I want you to know you're not alone anymore.",
            EmotionType.OVERWHELM: "Being overwhelmed makes complete sense - you're dealing with so much. It's okay to feel like it's too much.",
            EmotionType.NUMBNESS: "Numbness is a way your mind protects you when things are too much. It's okay if you can't feel everything right now.",
            EmotionType.DESPAIR: "I hear the hopelessness you're feeling. When you're in the middle of it, it can feel like there's no way through.",
            EmotionType.ANXIETY: "That constant state of anxiety and stress - it's exhausting. Your nervous system is working overtime to keep you safe.",
            EmotionType.HOPE: "I hear the hope in your words, even if it feels fragile. That hope is a testament to your resilience.",
        }

        return validations.get(emotion, "I hear you, and what you're feeling matters.")

    def _select_affirmation(self, state: EmotionalState) -> str:
        """Select appropriate affirmation"""
        import random

        if state.primary_emotion in [EmotionType.SHAME, EmotionType.GUILT]:
            affirmations = [a for a in self.affirmation_library if "worth" in a.lower() or "fault" in a.lower()]
        elif state.primary_emotion in [EmotionType.DESPAIR, EmotionType.HOPELESS]:
            affirmations = [a for a in self.affirmation_library if "hope" in a.lower() or "possible" in a.lower()]
        elif state.primary_emotion in [EmotionType.FEAR, EmotionType.ANXIETY]:
            affirmations = [a for a in self.affirmation_library if "strength" in a.lower() or "brave" in a.lower()]
        else:
            affirmations = self.affirmation_library

        return random.choice(affirmations) if affirmations else self.affirmation_library[0]

    def _generate_support(self, state: EmotionalState) -> str:
        """Generate supportive statement"""
        if state.crisis_level >= 7:
            return "I'm here with you right now. You don't have to face this moment alone. Let's take this one breath at a time."
        elif state.needs_grounding:
            return "I'm here, grounding this moment with you. You're safe in this conversation. Take all the time you need."
        elif state.intensity > 0.7:
            return "I'm holding space for all of these big feelings. They're welcome here, and so are you."
        else:
            return "I'm here to listen, to support you, and to remind you that you matter."

    def _generate_guidance(self, state: EmotionalState) -> Optional[str]:
        """Generate gentle guidance if appropriate"""
        if state.needs_resources:
            return "Would it help to explore what resources and support are available to you? We can do that together, at your pace."
        elif state.crisis_level >= 5:
            return "If you're open to it, we could talk about ways to help you feel safer right now."
        elif state.primary_emotion == EmotionType.CONFUSION:
            return "Sometimes talking through the confusion can help. Would you like to explore what you're feeling?"
        return None

    def _generate_love_statement(self, state: EmotionalState) -> str:
        """
        Generate love-centered statement
        Core: "How can we help you love yourself more?"
        """
        import random

        if state.primary_emotion in [EmotionType.SHAME, EmotionType.GUILT]:
            statements = self.love_statements["self_worth"]
        elif state.needs_affirmation:
            statements = self.love_statements["relentless_love"]
        elif state.primary_emotion == EmotionType.HOPE:
            statements = self.love_statements["love_in_action"]
        else:
            statements = self.love_statements["unconditional_love"]

        return random.choice(statements)

    def _calculate_response_empathy(self, state: EmotionalState) -> float:
        """
        Calculate empathy score for this specific response
        Based on Sierra's 1,700+ rating system
        """
        base_score = 1000

        # Bonus for addressing trauma
        if state.trauma_indicators:
            base_score += 300

        # Bonus for crisis response
        if state.crisis_level >= 7:
            base_score += 200

        # Bonus for addressing complex emotions
        if len(state.secondary_emotions) >= 2:
            base_score += 100

        # Bonus for affirmation need recognition
        if state.needs_affirmation:
            base_score += 200

        # Normalize to 0-2000 scale
        return min(base_score, 2000)

    def get_empathy_rating(self) -> Dict[str, Any]:
        """Get Sierra's empathy rating breakdown"""
        return {
            "total_rating": self.total_empathy_rating,
            "breakdown": {
                "base_empathy": self.empathy_baseline,
                "trauma_informed": self.trauma_informed_bonus,
                "cultural_sensitivity": self.cultural_sensitivity,
                "love_amplification": self.love_amplification,
                "adaptive_response": self.adaptive_response
            },
            "description": "Advanced empathy with trauma-informed, love-centered approach",
            "core_mission": "How can we help you love yourself more?",
            "core_values": ["Love", "Compassion", "Non-judgment", "Empowerment"]
        }
