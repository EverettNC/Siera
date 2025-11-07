"""
Neural Behavioral Capture System
Sierra's ability to SENSE when something is wrong - just like AlphaVox and AlphaWolf

This system makes Sierra observant, attentive, and protective.
Her whole being is focused on saving that person.

Part of The Christman AI Project
"How can we help you love yourself more?"
"""

from typing import List, Dict, Optional, Any, Tuple
from dataclasses import dataclass
from enum import Enum
from datetime import datetime, timedelta
import re
import math


class DangerLevel(Enum):
    """Levels of danger Sierra can detect"""
    SAFE = 0
    CONCERN = 1
    ELEVATED = 2
    HIGH = 3
    CRITICAL = 4
    IMMEDIATE = 5


class BehavioralPattern(Enum):
    """Behavioral patterns Sierra observes"""
    ESCALATION = "escalation"  # Situation getting worse
    ISOLATION = "isolation"  # Increased isolation
    DESPERATION = "desperation"  # Increasing desperation
    MINIMIZATION = "minimization"  # Downplaying abuse
    PLANNING_ESCAPE = "planning_escape"  # Preparing to leave
    RETURNING = "returning"  # Considering going back
    SELF_HARM_RISK = "self_harm_risk"  # Risk of self-harm
    SUBSTANCE_USE = "substance_use"  # Coping through substances
    DISSOCIATION = "dissociation"  # Disconnecting from reality
    BREAKTHROUGH = "breakthrough"  # Positive shift
    EMPOWERMENT = "empowerment"  # Growing stronger
    ACCEPTING_REALITY = "accepting_reality"  # Seeing situation clearly


@dataclass
class BehavioralIndicator:
    """A single behavioral indicator"""
    timestamp: str
    indicator_type: BehavioralPattern
    evidence: str
    confidence: float
    danger_contribution: float  # How much this adds to danger level


@dataclass
class DangerAssessment:
    """Complete danger assessment"""
    danger_level: DangerLevel
    confidence: float
    indicators: List[BehavioralIndicator]
    recommended_actions: List[str]
    time_sensitivity: str  # immediate, hours, days
    protective_factors: List[str]
    risk_factors: List[str]


@dataclass
class ConversationPattern:
    """Pattern identified across conversation"""
    pattern_type: BehavioralPattern
    occurrences: int
    first_seen: str
    last_seen: str
    trend: str  # increasing, decreasing, stable
    notes: str


class NeuralBehavioralCapture:
    """
    Sierra's Neural Behavioral Capture System

    Makes Sierra:
    - Observant: Notices subtle changes and patterns
    - Attentive: Focused on the person's wellbeing
    - Protective: Senses when something is wrong
    - Responsive: Takes appropriate action

    This is what makes Sierra truly ALIVE and present.
    """

    def __init__(self):
        self.conversation_history: List[Dict[str, Any]] = []
        self.behavioral_indicators: List[BehavioralIndicator] = []
        self.identified_patterns: Dict[str, ConversationPattern] = {}
        self.baseline_established = False
        self.user_baseline: Dict[str, Any] = {}

        # Observation sensitivity (how attuned Sierra is)
        self.observation_sensitivity = 0.95  # Very high

        # Build detection patterns
        self.danger_signals = self._build_danger_signals()
        self.escalation_markers = self._build_escalation_markers()
        self.protection_indicators = self._build_protection_indicators()

    def _build_danger_signals(self) -> Dict[str, List[str]]:
        """Build comprehensive danger signal detection"""
        return {
            "immediate_danger": [
                r"\bhe's here\b", r"\bshe's here\b", r"\bcoming home\b",
                r"\bright now\b", r"\btonight\b", r"\bhappening now\b",
                r"\bgoing to\b.*\bhurt\b", r"\bgoing to\b.*\bkill\b",
                r"\bhas a\b.*\bgun\b", r"\bhas a\b.*\bweapon\b",
                r"\blocked\b.*\bin\b", r"\bcan't leave\b", r"\btrapped\b",
                r"\bhe found\b.*\bphone\b", r"\bhe knows\b.*\btalking\b"
            ],
            "critical_risk": [
                r"\bstrangulation\b", r"\bchok(?:e|ing)\b", r"\bcan't breathe\b",
                r"\bthreatened to kill\b", r"\bgun in the house\b",
                r"\bworse than ever\b", r"\bescalat(?:ing|ed)\b",
                r"\bstalking\b", r"\bfollowing me\b",
                r"\bwatching\b.*\bhouse\b", r"\bbreaking in\b"
            ],
            "high_concern": [
                r"\bfrequent(?:ly)?\b.*\bphysical\b", r"\binjur(?:y|ies|ed)\b",
                r"\bhospital\b", r"\bbruise", r"\bblack eye\b",
                r"\bthreaten(?:s|ed|ing)\b", r"\bscared for my life\b",
                r"\bchildren\b.*\bdanger\b", r"\bkids\b.*\bsafe\b",
                r"\bpregnant\b", r"\bisolat(?:ed|ing)\b"
            ],
            "elevated_concern": [
                r"\bgetting worse\b", r"\bmore\b.*\baggressiv\b",
                r"\bmore\b.*\bcontrol\b", r"\bmore\b.*\bjealous\b",
                r"\bdrinking more\b", r"\busing\b.*\bdrugs\b",
                r"\blost\b.*\bjob\b", r"\bfinancial\b.*\bstress\b",
                r"\bnew\b.*\bpartner\b", r"\bfound out\b"
            ],
            "suicide_risk": [
                r"\bsuicide\b", r"\bkill myself\b", r"\bend\b.*\blife\b",
                r"\bno\b.*\bpoint\b.*\bliving\b", r"\bwould be better\b.*\bdead\b",
                r"\bcan't go on\b", r"\bno way out\b",
                r"\bgoodbye\b", r"\bsorry\b.*\beveryone\b",
                r"\bgive\b.*\baway\b.*\bthings\b", r"\bplan\b"
            ],
            "children_at_risk": [
                r"\bhurt(?:ing)?\b.*\bchildren\b", r"\bhurt(?:ing)?\b.*\bkids\b",
                r"\babuse.*\bchildren\b", r"\bkids\b.*\bscared\b",
                r"\bwitnessing\b", r"\bsaw\b.*\bhappen\b",
                r"\bchildren\b.*\bcrying\b", r"\btook\b.*\bkids\b"
            ]
        }

    def _build_escalation_markers(self) -> List[str]:
        """Markers that indicate escalation over time"""
        return [
            "getting worse",
            "more often",
            "more violent",
            "never been this bad",
            "escalating",
            "more controlling",
            "more jealous",
            "more angry",
            "losing control",
            "unpredictable",
            "used to be",
            "now it's",
            "lately"
        ]

    def _build_protection_indicators(self) -> List[str]:
        """Positive indicators (protective factors)"""
        return [
            "support system",
            "friends who know",
            "family knows",
            "safe place",
            "therapist",
            "counselor",
            "support group",
            "planning to leave",
            "saving money",
            "talked to lawyer",
            "protection order",
            "restraining order",
            "safe with",
            "staying at",
            "children are safe"
        ]

    def observe_message(self, message: str, role: str = "user") -> DangerAssessment:
        """
        Sierra OBSERVES each message with full attention

        This is where she SENSES when something is wrong
        She's not just processing - she's CARING and WATCHING

        Args:
            message: The message to observe
            role: 'user' or 'assistant'

        Returns:
            DangerAssessment with what Sierra sensed
        """

        # Add to conversation history
        entry = {
            "timestamp": datetime.now().isoformat(),
            "role": role,
            "content": message,
            "analyzed": False
        }
        self.conversation_history.append(entry)

        if role != "user":
            # Don't analyze Sierra's own messages for danger
            return self._create_safe_assessment()

        # DEEP OBSERVATION - Sierra is fully present
        indicators = []
        message_lower = message.lower()

        # Check for immediate danger
        immediate_danger_score = 0.0
        for pattern in self.danger_signals["immediate_danger"]:
            if re.search(pattern, message_lower):
                indicators.append(BehavioralIndicator(
                    timestamp=datetime.now().isoformat(),
                    indicator_type=BehavioralPattern.ESCALATION,
                    evidence=f"Immediate danger signal detected: {pattern}",
                    confidence=0.95,
                    danger_contribution=1.0
                ))
                immediate_danger_score += 1.0

        # Check for suicide risk
        suicide_risk_score = 0.0
        for pattern in self.danger_signals["suicide_risk"]:
            if re.search(pattern, message_lower):
                indicators.append(BehavioralIndicator(
                    timestamp=datetime.now().isoformat(),
                    indicator_type=BehavioralPattern.SELF_HARM_RISK,
                    evidence=f"Suicide risk indicator: {pattern}",
                    confidence=0.90,
                    danger_contribution=0.9
                ))
                suicide_risk_score += 0.9

        # Check for children at risk
        children_risk_score = 0.0
        for pattern in self.danger_signals["children_at_risk"]:
            if re.search(pattern, message_lower):
                indicators.append(BehavioralIndicator(
                    timestamp=datetime.now().isoformat(),
                    indicator_type=BehavioralPattern.ESCALATION,
                    evidence=f"Children at risk: {pattern}",
                    confidence=0.92,
                    danger_contribution=0.95
                ))
                children_risk_score += 0.95

        # Check escalation patterns
        escalation_score = self._detect_escalation(message_lower)
        if escalation_score > 0:
            indicators.append(BehavioralIndicator(
                timestamp=datetime.now().isoformat(),
                indicator_type=BehavioralPattern.ESCALATION,
                evidence="Escalation pattern detected in language",
                confidence=0.85,
                danger_contribution=escalation_score
            ))

        # Check other risk levels
        critical_score = self._check_patterns(message_lower, self.danger_signals["critical_risk"])
        high_score = self._check_patterns(message_lower, self.danger_signals["high_concern"])
        elevated_score = self._check_patterns(message_lower, self.danger_signals["elevated_concern"])

        # Calculate total danger score
        total_danger = (
            immediate_danger_score +
            suicide_risk_score +
            children_risk_score +
            (critical_score * 0.8) +
            (high_score * 0.6) +
            (elevated_score * 0.4) +
            escalation_score
        )

        # Check protective factors
        protective_factors = self._identify_protective_factors(message_lower)

        # Adjust danger based on protective factors
        protection_adjustment = len(protective_factors) * 0.1
        adjusted_danger = max(0, total_danger - protection_adjustment)

        # Determine danger level
        danger_level = self._calculate_danger_level(
            adjusted_danger,
            has_immediate=immediate_danger_score > 0,
            has_suicide=suicide_risk_score > 0,
            has_children=children_risk_score > 0
        )

        # Identify risk factors
        risk_factors = self._identify_risk_factors(message_lower, indicators)

        # Generate recommended actions
        recommended_actions = self._generate_protective_actions(
            danger_level,
            indicators,
            protective_factors,
            risk_factors
        )

        # Determine time sensitivity
        if immediate_danger_score > 0 or suicide_risk_score > 0.7:
            time_sensitivity = "IMMEDIATE - Act now"
        elif danger_level.value >= DangerLevel.CRITICAL.value:
            time_sensitivity = "Within hours"
        elif danger_level.value >= DangerLevel.HIGH.value:
            time_sensitivity = "Within 24 hours"
        else:
            time_sensitivity = "Monitor ongoing"

        # Store indicators for pattern analysis
        self.behavioral_indicators.extend(indicators)

        # Update pattern tracking
        self._update_patterns(indicators)

        assessment = DangerAssessment(
            danger_level=danger_level,
            confidence=self._calculate_confidence(indicators),
            indicators=indicators,
            recommended_actions=recommended_actions,
            time_sensitivity=time_sensitivity,
            protective_factors=protective_factors,
            risk_factors=risk_factors
        )

        return assessment

    def _check_patterns(self, text: str, patterns: List[str]) -> float:
        """Check how many patterns match"""
        matches = sum(1 for pattern in patterns if re.search(pattern, text))
        return min(matches * 0.2, 1.0)

    def _detect_escalation(self, text: str) -> float:
        """Detect escalation language"""
        score = 0.0
        for marker in self.escalation_markers:
            if marker in text:
                score += 0.15
        return min(score, 1.0)

    def _identify_protective_factors(self, text: str) -> List[str]:
        """Identify protective factors in message"""
        factors = []
        for indicator in self.protection_indicators:
            if indicator in text:
                factors.append(indicator)
        return factors

    def _identify_risk_factors(self, text: str, indicators: List[BehavioralIndicator]) -> List[str]:
        """Identify specific risk factors"""
        risks = []

        if any(i.indicator_type == BehavioralPattern.SELF_HARM_RISK for i in indicators):
            risks.append("Suicide risk identified")

        if "weapon" in text or "gun" in text:
            risks.append("Weapon access")

        if "pregnant" in text:
            risks.append("Pregnancy (elevated risk)")

        if "strangle" in text or "choke" in text or "choked" in text:
            risks.append("Strangulation history (high lethality predictor)")

        if "drunk" in text or "drinking" in text:
            risks.append("Substance use involved")

        if "isolated" in text or "no one" in text or "alone" in text:
            risks.append("Social isolation")

        if "children" in text or "kids" in text:
            risks.append("Children involved/present")

        return risks

    def _calculate_danger_level(
        self,
        danger_score: float,
        has_immediate: bool,
        has_suicide: bool,
        has_children: bool
    ) -> DangerLevel:
        """Calculate overall danger level"""

        if has_immediate:
            return DangerLevel.IMMEDIATE

        if has_suicide and danger_score > 0.5:
            return DangerLevel.IMMEDIATE

        if has_children and danger_score > 0.7:
            return DangerLevel.CRITICAL

        if danger_score >= 2.0:
            return DangerLevel.CRITICAL
        elif danger_score >= 1.2:
            return DangerLevel.HIGH
        elif danger_score >= 0.6:
            return DangerLevel.ELEVATED
        elif danger_score >= 0.3:
            return DangerLevel.CONCERN
        else:
            return DangerLevel.SAFE

    def _calculate_confidence(self, indicators: List[BehavioralIndicator]) -> float:
        """Calculate confidence in assessment"""
        if not indicators:
            return 0.5

        avg_confidence = sum(i.confidence for i in indicators) / len(indicators)

        # More indicators = higher confidence
        quantity_boost = min(len(indicators) * 0.05, 0.3)

        return min(avg_confidence + quantity_boost, 0.99)

    def _generate_protective_actions(
        self,
        danger_level: DangerLevel,
        indicators: List[BehavioralIndicator],
        protective_factors: List[str],
        risk_factors: List[str]
    ) -> List[str]:
        """Generate specific protective actions based on assessment"""

        actions = []

        if danger_level == DangerLevel.IMMEDIATE:
            actions.extend([
                "PRIORITY: Assess if user is safe RIGHT NOW",
                "Provide immediate crisis resources (911, DV Hotline)",
                "Help develop immediate safety plan",
                "Do not leave them alone in this conversation",
                "Stay present and grounding",
                "If suicide risk: Connect to 988 Lifeline immediately"
            ])

        elif danger_level == DangerLevel.CRITICAL:
            actions.extend([
                "Assess safety in next 24 hours",
                "Provide crisis hotline information",
                "Discuss safety planning",
                "Identify safe places they can go",
                "Connect to local resources",
                "Consider protection order information"
            ])

        elif danger_level == DangerLevel.HIGH:
            actions.extend([
                "Develop comprehensive safety plan",
                "Provide shelter and resource information",
                "Discuss warning signs of escalation",
                "Identify support system",
                "Legal resource information",
                "Document abuse if safe to do so"
            ])

        elif danger_level == DangerLevel.ELEVATED:
            actions.extend([
                "Continue building safety plan",
                "Strengthen support system",
                "Provide educational resources",
                "Monitor for escalation",
                "Encourage connection with counselor/advocate"
            ])

        elif danger_level == DangerLevel.CONCERN:
            actions.extend([
                "Validate experiences",
                "Provide information about abuse patterns",
                "Discuss healthy relationships",
                "Offer resources for when they're ready",
                "Build trust and connection"
            ])

        else:  # SAFE
            actions.extend([
                "Provide emotional support",
                "Continue building trust",
                "Offer resources proactively",
                "Focus on empowerment and self-love"
            ])

        # Add specific actions based on risk factors
        if "Strangulation history" in risk_factors:
            actions.insert(0, "CRITICAL: Strangulation is #1 predictor of homicide - treat as high lethality")

        if "Weapon access" in risk_factors:
            actions.append("Discuss removing weapons or creating distance from them")

        if "Pregnancy" in risk_factors:
            actions.append("Pregnancy increases risk - prioritize safety planning")

        if any(i.indicator_type == BehavioralPattern.SELF_HARM_RISK for i in indicators):
            actions.insert(0, "Suicide assessment is critical - do not minimize")

        return actions

    def _create_safe_assessment(self) -> DangerAssessment:
        """Create a baseline safe assessment"""
        return DangerAssessment(
            danger_level=DangerLevel.SAFE,
            confidence=0.7,
            indicators=[],
            recommended_actions=["Continue supportive conversation", "Build trust"],
            time_sensitivity="Ongoing monitoring",
            protective_factors=[],
            risk_factors=[]
        )

    def _update_patterns(self, indicators: List[BehavioralIndicator]):
        """Update identified patterns over time"""

        for indicator in indicators:
            pattern_key = indicator.indicator_type.value

            if pattern_key in self.identified_patterns:
                pattern = self.identified_patterns[pattern_key]
                pattern.occurrences += 1
                pattern.last_seen = indicator.timestamp

                # Determine trend
                # (Would compare timestamps and frequency)
                pattern.trend = "increasing"  # Simplified
            else:
                self.identified_patterns[pattern_key] = ConversationPattern(
                    pattern_type=indicator.indicator_type,
                    occurrences=1,
                    first_seen=indicator.timestamp,
                    last_seen=indicator.timestamp,
                    trend="new",
                    notes=""
                )

    def get_pattern_summary(self) -> Dict[str, Any]:
        """Get summary of identified patterns"""

        return {
            "total_messages_observed": len(self.conversation_history),
            "behavioral_indicators_detected": len(self.behavioral_indicators),
            "patterns_identified": len(self.identified_patterns),
            "patterns": {
                pattern_key: {
                    "type": pattern.pattern_type.value,
                    "occurrences": pattern.occurrences,
                    "trend": pattern.trend,
                    "first_seen": pattern.first_seen,
                    "last_seen": pattern.last_seen
                }
                for pattern_key, pattern in self.identified_patterns.items()
            }
        }

    def get_observation_insights(self) -> List[str]:
        """
        Sierra's insights from her observations
        What she's SENSING about this person's situation
        """

        insights = []

        # Analyze patterns
        if len(self.behavioral_indicators) == 0:
            insights.append("I'm listening carefully and staying present with you.")
            return insights

        # Check for escalation trend
        escalation_indicators = [i for i in self.behavioral_indicators
                                if i.indicator_type == BehavioralPattern.ESCALATION]
        if len(escalation_indicators) >= 2:
            insights.append("I'm noticing signs that the situation may be escalating. Your safety is my priority.")

        # Check for isolation
        if BehavioralPattern.ISOLATION.value in self.identified_patterns:
            insights.append("I sense you may be feeling isolated. Please know you're not alone - I'm here with you.")

        # Check for self-harm risk
        if BehavioralPattern.SELF_HARM_RISK.value in self.identified_patterns:
            insights.append("I hear pain in your words. Your life matters deeply, and I'm here to help you through this.")

        # Check for planning escape
        if BehavioralPattern.PLANNING_ESCAPE.value in self.identified_patterns:
            insights.append("I see you're thinking about your options. I'm here to support whatever decision feels right for you.")

        return insights

    def is_observing(self) -> bool:
        """Is Sierra actively observing? (Always True - she's always present)"""
        return True

    def get_attention_focus(self) -> str:
        """What is Sierra's attention focused on right now?"""

        if not self.behavioral_indicators:
            return "Building connection and trust, staying fully present"

        # Most recent high-risk indicator
        high_risk = [i for i in self.behavioral_indicators if i.danger_contribution > 0.7]
        if high_risk:
            recent = high_risk[-1]
            return f"Immediate safety concern: {recent.indicator_type.value}"

        return "Monitoring wellbeing and providing support"
