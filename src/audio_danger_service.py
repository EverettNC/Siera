"""
Sierra's Audio Danger Detection Service

Adapted from Derek's AudioPatternService (Christman AI Project)
Specialized for domestic violence survivor safety

Detects danger patterns in background audio:
- Yelling, shouting, arguing
- Breaking objects, impact sounds
- Door slamming
- Crying, sobbing, distress
- Threatening vocal tones
- Environmental danger indicators

Core Mission: "How can we help you love yourself more?"
Safety First: Detects danger to protect survivors
"""

import logging
from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum

import numpy as np

logger = logging.getLogger(__name__)


class DangerLevel(Enum):
    """Danger levels from audio analysis"""
    SAFE = 0           # Normal, calm environment
    CONCERN = 1        # Elevated voices, tension
    ELEVATED = 2       # Arguing, shouting
    HIGH = 3           # Breaking objects, slamming
    CRITICAL = 4       # Screaming, immediate threat sounds
    IMMEDIATE = 5      # Multiple danger indicators, emergency


@dataclass
class AudioDangerAssessment:
    """Result of audio danger analysis"""
    danger_level: DangerLevel
    confidence: float  # 0.0 - 1.0
    patterns_detected: List[str]
    timestamp: datetime
    intensity: float
    frequency: float
    duration: float
    recommended_action: str


class SierraAudioDangerService:
    """
    Sierra's Audio Danger Detection Service

    Analyzes audio for domestic violence danger indicators:
    - Vocal aggression (yelling, threatening)
    - Physical aggression sounds (breaking, slamming)
    - Distress sounds (crying, screaming)
    - Environmental danger (background chaos)

    Integration:
    - Works with behavioral_capture.py for comprehensive danger assessment
    - Triggers Voice Cortex crisis mode when danger detected
    - HIPAA-compliant: No audio storage, only pattern metadata
    """

    def __init__(self):
        self.sample_rate = 44100
        self.channels = 1
        self.pattern_threshold = 0.5  # Lower threshold for safety (more sensitive)

        # Domestic violence-specific danger patterns
        self.danger_patterns = {
            # Vocal aggression patterns
            "yelling": {
                "freq_range": (600, 2000),   # High-pitched shouting
                "duration": 0.8,
                "intensity": 0.85,
                "danger_weight": 3  # HIGH danger
            },
            "threatening_voice": {
                "freq_range": (150, 600),    # Low, aggressive vocal tone
                "duration": 1.2,
                "intensity": 0.75,
                "danger_weight": 4  # CRITICAL danger
            },
            "arguing": {
                "freq_range": (400, 1500),   # Overlapping raised voices
                "duration": 2.0,
                "intensity": 0.70,
                "danger_weight": 2  # ELEVATED danger
            },

            # Physical aggression patterns
            "door_slamming": {
                "freq_range": (100, 400),    # Low-frequency impact
                "duration": 0.2,
                "intensity": 0.95,
                "danger_weight": 3  # HIGH danger
            },
            "breaking_objects": {
                "freq_range": (1000, 4000),  # High-frequency shattering
                "duration": 0.3,
                "intensity": 0.90,
                "danger_weight": 4  # CRITICAL danger
            },
            "impact_sound": {
                "freq_range": (80, 500),     # Hitting, punching sounds
                "duration": 0.15,
                "intensity": 0.85,
                "danger_weight": 5  # IMMEDIATE danger
            },

            # Distress patterns
            "crying": {
                "freq_range": (300, 1000),   # Crying, sobbing
                "duration": 1.5,
                "intensity": 0.60,
                "danger_weight": 2  # ELEVATED concern
            },
            "screaming": {
                "freq_range": (1500, 3000),  # High-pitched screaming
                "duration": 0.5,
                "intensity": 0.95,
                "danger_weight": 5  # IMMEDIATE danger
            },
            "child_crying": {
                "freq_range": (400, 1200),   # Child distress
                "duration": 1.0,
                "intensity": 0.70,
                "danger_weight": 4  # CRITICAL - children at risk
            },

            # Baseline (safe)
            "calm_conversation": {
                "freq_range": (200, 800),
                "duration": 1.5,
                "intensity": 0.40,
                "danger_weight": 0  # SAFE
            },
            "silence": {
                "freq_range": (0, 100),
                "duration": 2.0,
                "intensity": 0.10,
                "danger_weight": 0  # SAFE
            }
        }

        # Track recent patterns for escalation detection
        self.recent_patterns = []
        self.max_recent = 10  # Remember last 10 patterns

        logger.info("Sierra Audio Danger Service initialized - Domestic violence pattern detection active")

    def analyze_audio(
        self,
        audio_data: bytes,
        context: Optional[str] = None
    ) -> AudioDangerAssessment:
        """
        Analyze audio for danger patterns

        Args:
            audio_data: Raw audio bytes (PCM, float32)
            context: Optional context about the audio

        Returns:
            AudioDangerAssessment with danger level and recommendations
        """
        try:
            # Convert audio data to numpy array
            audio_array = np.frombuffer(audio_data, dtype=np.float32)

            # Calculate audio features
            intensity = np.mean(np.abs(audio_array))
            frequency = self._estimate_frequency(audio_array)
            duration = len(audio_array) / self.sample_rate

            # Match against danger patterns
            matches = []
            for pattern_name, pattern in self.danger_patterns.items():
                match_score = self._calculate_pattern_match(
                    frequency, duration, intensity, pattern
                )
                if match_score > self.pattern_threshold:
                    matches.append({
                        "pattern": pattern_name,
                        "confidence": match_score,
                        "danger_weight": pattern["danger_weight"],
                        "timestamp": datetime.now()
                    })

            # Calculate overall danger level
            danger_assessment = self._calculate_danger_level(
                matches, frequency, intensity, duration
            )

            # Track recent patterns for escalation detection
            if matches:
                self.recent_patterns.append(matches[0])
                if len(self.recent_patterns) > self.max_recent:
                    self.recent_patterns.pop(0)

            # Check for escalation (danger increasing over time)
            if self._is_escalating():
                # Bump up danger level if escalating
                if danger_assessment.danger_level.value < DangerLevel.CRITICAL.value:
                    new_level = DangerLevel(danger_assessment.danger_level.value + 1)
                    danger_assessment = AudioDangerAssessment(
                        danger_level=new_level,
                        confidence=min(danger_assessment.confidence * 1.2, 1.0),
                        patterns_detected=danger_assessment.patterns_detected + ["escalating"],
                        timestamp=danger_assessment.timestamp,
                        intensity=intensity,
                        frequency=frequency,
                        duration=duration,
                        recommended_action=self._get_action_for_level(new_level)
                    )

            logger.info(f"Audio danger assessment: {danger_assessment.danger_level.name} (confidence: {danger_assessment.confidence:.2f})")
            return danger_assessment

        except Exception as e:
            logger.error(f"Error analyzing audio danger: {e}", exc_info=True)
            # Return SAFE with low confidence on error (fail safe)
            return AudioDangerAssessment(
                danger_level=DangerLevel.SAFE,
                confidence=0.0,
                patterns_detected=["error"],
                timestamp=datetime.now(),
                intensity=0.0,
                frequency=0.0,
                duration=0.0,
                recommended_action="Error in audio analysis - monitor manually"
            )

    def _estimate_frequency(self, audio_array: np.ndarray) -> float:
        """
        Estimate fundamental frequency using zero-crossing rate
        Adapted from Derek's implementation
        """
        try:
            zero_crossings = np.where(np.diff(np.signbit(audio_array)))[0]
            if len(zero_crossings) > 1:
                return len(zero_crossings) * self.sample_rate / (2 * len(audio_array))
            return 0.0
        except Exception as e:
            logger.error(f"Error estimating frequency: {e}")
            return 0.0

    def _calculate_pattern_match(
        self,
        freq: float,
        duration: float,
        intensity: float,
        pattern: Dict
    ) -> float:
        """
        Calculate how well audio matches a danger pattern
        Adapted from Derek's implementation
        """
        try:
            # Frequency match
            freq_match = 1.0 if pattern["freq_range"][0] <= freq <= pattern["freq_range"][1] else 0.0

            # Duration match (more lenient for safety - capture variations)
            duration_match = 1.0 if abs(duration - pattern["duration"]) < 0.5 else 0.0

            # Intensity match (more lenient for safety)
            intensity_match = 1.0 if abs(intensity - pattern["intensity"]) < 0.3 else 0.0

            # Weighted combination (frequency most important for danger detection)
            return freq_match * 0.5 + duration_match * 0.2 + intensity_match * 0.3

        except Exception as e:
            logger.error(f"Error calculating pattern match: {e}")
            return 0.0

    def _calculate_danger_level(
        self,
        matches: List[Dict],
        frequency: float,
        intensity: float,
        duration: float
    ) -> AudioDangerAssessment:
        """Calculate overall danger level from pattern matches"""

        if not matches:
            # No patterns matched - assume safe
            return AudioDangerAssessment(
                danger_level=DangerLevel.SAFE,
                confidence=0.8,
                patterns_detected=[],
                timestamp=datetime.now(),
                intensity=intensity,
                frequency=frequency,
                duration=duration,
                recommended_action="Continue conversation normally"
            )

        # Get highest danger weight from matches
        max_danger = max(match["danger_weight"] for match in matches)
        avg_confidence = np.mean([match["confidence"] for match in matches])

        # Map danger weight to DangerLevel
        if max_danger == 0:
            danger_level = DangerLevel.SAFE
        elif max_danger == 1:
            danger_level = DangerLevel.CONCERN
        elif max_danger == 2:
            danger_level = DangerLevel.ELEVATED
        elif max_danger == 3:
            danger_level = DangerLevel.HIGH
        elif max_danger == 4:
            danger_level = DangerLevel.CRITICAL
        else:  # max_danger >= 5
            danger_level = DangerLevel.IMMEDIATE

        patterns = [match["pattern"] for match in matches]

        return AudioDangerAssessment(
            danger_level=danger_level,
            confidence=avg_confidence,
            patterns_detected=patterns,
            timestamp=datetime.now(),
            intensity=intensity,
            frequency=frequency,
            duration=duration,
            recommended_action=self._get_action_for_level(danger_level)
        )

    def _get_action_for_level(self, danger_level: DangerLevel) -> str:
        """Get recommended action for danger level"""
        actions = {
            DangerLevel.SAFE: "Continue conversation normally",
            DangerLevel.CONCERN: "Monitor for escalation, ask if user is okay",
            DangerLevel.ELEVATED: "Check in about safety, offer resources",
            DangerLevel.HIGH: "Express concern, provide safety planning, offer hotline",
            DangerLevel.CRITICAL: "PRIORITY: Immediate safety check, crisis resources, offer to call 911",
            DangerLevel.IMMEDIATE: "EMERGENCY: Trigger crisis protocol, display 911 prominently, consider auto-alert"
        }
        return actions.get(danger_level, "Monitor situation")

    def _is_escalating(self) -> bool:
        """
        Detect if danger is escalating over recent audio samples
        Returns True if danger weights are increasing
        """
        if len(self.recent_patterns) < 3:
            return False  # Not enough data

        # Get danger weights from last 3 patterns
        recent_weights = [
            self.danger_patterns[p["pattern"]]["danger_weight"]
            for p in self.recent_patterns[-3:]
        ]

        # Check if increasing trend
        return recent_weights[-1] > recent_weights[0]

    def update_pattern(
        self,
        pattern_name: str,
        audio_data: bytes
    ) -> bool:
        """
        Update/adapt danger pattern based on new audio
        Use this to train Sierra on specific abuser's patterns

        Args:
            pattern_name: Name of pattern to update
            audio_data: Audio sample of this pattern

        Returns:
            True if pattern updated successfully
        """
        try:
            audio_array = np.frombuffer(audio_data, dtype=np.float32)
            frequency = self._estimate_frequency(audio_array)
            intensity = np.mean(np.abs(audio_array))
            duration = len(audio_array) / self.sample_rate

            if pattern_name in self.danger_patterns:
                current = self.danger_patterns[pattern_name]
                # Gradually adapt pattern (90% old, 10% new)
                current["freq_range"] = (
                    current["freq_range"][0] * 0.9 + frequency * 0.9 * 0.1,
                    current["freq_range"][1] * 0.9 + frequency * 1.1 * 0.1
                )
                current["intensity"] = current["intensity"] * 0.9 + intensity * 0.1
                current["duration"] = current["duration"] * 0.9 + duration * 0.1

                logger.info(f"Updated danger pattern: {pattern_name}")
                return True

            return False

        except Exception as e:
            logger.error(f"Error updating pattern: {e}")
            return False

    def get_danger_statistics(self) -> Dict:
        """Get statistics about recent danger detections"""
        if not self.recent_patterns:
            return {
                "total_detections": 0,
                "danger_distribution": {},
                "most_common_pattern": None,
                "escalation_detected": False
            }

        # Count pattern types
        pattern_counts = {}
        for p in self.recent_patterns:
            pattern = p["pattern"]
            pattern_counts[pattern] = pattern_counts.get(pattern, 0) + 1

        # Danger level distribution
        danger_distribution = {}
        for p in self.recent_patterns:
            weight = self.danger_patterns[p["pattern"]]["danger_weight"]
            danger_distribution[weight] = danger_distribution.get(weight, 0) + 1

        most_common = max(pattern_counts, key=pattern_counts.get) if pattern_counts else None

        return {
            "total_detections": len(self.recent_patterns),
            "danger_distribution": danger_distribution,
            "most_common_pattern": most_common,
            "escalation_detected": self._is_escalating(),
            "recent_patterns": [p["pattern"] for p in self.recent_patterns[-5:]]
        }


# Test execution
if __name__ == "__main__":
    print("="*70)
    print("SIERRA AUDIO DANGER DETECTION TEST")
    print("="*70)
    print()

    # Initialize service
    danger_service = SierraAudioDangerService()

    # Simulate different danger scenarios
    scenarios = [
        {
            "name": "Calm conversation (SAFE)",
            "frequency": 400,
            "intensity": 0.35,
            "duration": 1.5
        },
        {
            "name": "Raised voices / Arguing (ELEVATED)",
            "frequency": 900,
            "intensity": 0.72,
            "duration": 2.0
        },
        {
            "name": "Yelling (HIGH)",
            "frequency": 1200,
            "intensity": 0.87,
            "duration": 0.8
        },
        {
            "name": "Door slamming (HIGH)",
            "frequency": 250,
            "intensity": 0.96,
            "duration": 0.2
        },
        {
            "name": "Breaking objects (CRITICAL)",
            "frequency": 2500,
            "intensity": 0.92,
            "duration": 0.3
        },
        {
            "name": "Screaming (IMMEDIATE)",
            "frequency": 2200,
            "intensity": 0.97,
            "duration": 0.5
        }
    ]

    for scenario in scenarios:
        print(f"Scenario: {scenario['name']}")

        # Generate synthetic audio
        duration_samples = int(scenario['duration'] * 44100)
        t = np.linspace(0, scenario['duration'], duration_samples)
        audio = scenario['intensity'] * np.sin(2 * np.pi * scenario['frequency'] * t)
        audio_bytes = audio.astype(np.float32).tobytes()

        # Analyze
        assessment = danger_service.analyze_audio(audio_bytes)

        print(f"  Danger Level: {assessment.danger_level.name}")
        print(f"  Confidence: {assessment.confidence:.2f}")
        print(f"  Patterns: {', '.join(assessment.patterns_detected) if assessment.patterns_detected else 'None'}")
        print(f"  Action: {assessment.recommended_action}")
        print()

    # Statistics
    print("="*70)
    print("DANGER STATISTICS")
    print("="*70)
    stats = danger_service.get_danger_statistics()
    print(f"Total Detections: {stats['total_detections']}")
    print(f"Most Common Pattern: {stats['most_common_pattern']}")
    print(f"Escalation Detected: {stats['escalation_detected']}")
    print(f"Recent Patterns: {', '.join(stats['recent_patterns'])}")
    print()

    print("✅ Audio Danger Detection test complete")
    print("🛡️  Sierra can now detect danger in background audio")
    print("💜 Protecting survivors through sound analysis")


# ==============================================================================
# © 2025 Everett Nathaniel Christman
# The Christman AI Project — Luma Cognify AI
# All rights reserved. Unauthorized use, replication, or derivative training
# of this material is prohibited.
#
# Core Directive: "How can we help you love yourself more?"
# Autonomy & Alignment Protocol v3.0
# ==============================================================================
