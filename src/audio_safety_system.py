"""
Sierra's Integrated Audio Safety System

Combines speech recognition with danger detection for comprehensive audio monitoring

System Components:
1. Speech Recognition - What the user is saying
2. Danger Detection - What's happening in the background
3. Crisis Response - Immediate intervention when danger detected

Adapted from Derek's RealSpeechRecognitionEngine + AudioPatternService
Specialized for domestic violence survivor safety

Core Mission: "How can we help you love yourself more?"
"""

import logging
import os
import queue
import threading
import time
from typing import Callable, Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from datetime import datetime

import numpy as np

# Try to import sounddevice for live audio
try:
    import sounddevice as sd
    SOUNDDEVICE_AVAILABLE = True
except ImportError:
    SOUNDDEVICE_AVAILABLE = False
    logging.warning("sounddevice not available - audio safety system limited")

# Import Sierra's danger detection
from audio_danger_service import SierraAudioDangerService, DangerLevel, AudioDangerAssessment

# Import Voice Cortex for crisis response
try:
    from voice_cortex import get_voice_cortex, VoicePriority
    VOICE_CORTEX_AVAILABLE = True
except ImportError:
    VOICE_CORTEX_AVAILABLE = False

logger = logging.getLogger(__name__)

# Audio configuration
AUDIO_SAMPLE_RATE = 44100  # Match danger service sample rate
MIN_SPEECH_DURATION = 0.5
SILENCE_THRESHOLD = 0.1
AUDIO_CACHE_DIR = "audio_cache"

if not os.path.exists(AUDIO_CACHE_DIR):
    os.makedirs(AUDIO_CACHE_DIR)


@dataclass
class AudioSafetyEvent:
    """Event from audio safety system"""
    timestamp: datetime
    event_type: str  # "speech", "danger", "crisis"
    content: str  # Transcribed text or danger description
    confidence: float
    danger_assessment: Optional[AudioDangerAssessment]
    metadata: Dict[str, Any]


class SierraAudioSafetySystem:
    """
    Sierra's Integrated Audio Safety System

    Real-time audio monitoring with dual analysis:
    1. Speech recognition for user communication
    2. Danger detection for environmental threats

    Safety Features:
    - Continuous background monitoring (non-intrusive)
    - Crisis detection → immediate Voice Cortex alert
    - Escalation tracking (danger increasing over time)
    - HIPAA-compliant (no audio storage, only metadata)

    Integration Points:
    - behavioral_capture.py - Comprehensive danger assessment
    - voice_cortex.py - Crisis voice output
    - sierra.py - Main AI system for context-aware responses
    """

    def __init__(self, language: str = "en-US"):
        """Initialize Sierra's audio safety system"""
        self.language = language
        self.is_listening = False

        # Callbacks for different event types
        self.speech_callbacks: List[Callable] = []
        self.danger_callbacks: List[Callable] = []
        self.crisis_callbacks: List[Callable] = []

        # Audio processing
        self.audio_buffer = []
        self.last_speech_time = 0
        self.silence_threshold = SILENCE_THRESHOLD
        self.min_speech_duration = MIN_SPEECH_DURATION
        self.audio_queue = queue.Queue()

        # Danger detection service
        self.danger_service = SierraAudioDangerService()

        # Voice Cortex for crisis response
        self.voice_cortex = get_voice_cortex() if VOICE_CORTEX_AVAILABLE else None

        # Safety state tracking
        self.current_danger_level = DangerLevel.SAFE
        self.danger_history: List[AudioDangerAssessment] = []
        self.crisis_mode_active = False

        # Audio device setup
        if SOUNDDEVICE_AVAILABLE:
            self.devices = sd.query_devices()
            logger.info(f"Available audio devices: {len(self.devices)}")

            self.input_device = next(
                (i for i, d in enumerate(self.devices) if d["max_input_channels"] > 0),
                None
            )
            if self.input_device is None:
                self.input_device = sd.default.device[0]
        else:
            self.devices = []
            self.input_device = None

        logger.info("Sierra Audio Safety System initialized")
        logger.info(f"  Language: {language}")
        logger.info(f"  Sounddevice Available: {SOUNDDEVICE_AVAILABLE}")
        logger.info(f"  Voice Cortex Available: {VOICE_CORTEX_AVAILABLE}")
        logger.info(f"  Danger Detection: Active")

    def start_monitoring(
        self,
        speech_callback: Optional[Callable] = None,
        danger_callback: Optional[Callable] = None,
        crisis_callback: Optional[Callable] = None
    ) -> bool:
        """
        Start continuous audio safety monitoring

        Args:
            speech_callback: Called when speech detected (text, confidence, metadata)
            danger_callback: Called when danger detected (assessment)
            crisis_callback: Called when crisis-level danger detected (assessment)

        Returns:
            True if monitoring started successfully
        """
        if self.is_listening:
            logger.warning("Audio safety monitoring already active")
            return False

        if not SOUNDDEVICE_AVAILABLE:
            logger.error("Cannot start monitoring - sounddevice not available")
            return False

        # Register callbacks
        if speech_callback:
            self.speech_callbacks.append(speech_callback)
        if danger_callback:
            self.danger_callbacks.append(danger_callback)
        if crisis_callback:
            self.crisis_callbacks.append(crisis_callback)

        self.is_listening = True
        self._start_audio_processing_thread()

        try:
            self.stream = sd.InputStream(
                samplerate=AUDIO_SAMPLE_RATE,
                channels=1,
                callback=self._audio_callback,
                device=self.input_device
            )
            self.stream.start()
            logger.info("Started audio stream for safety monitoring")
        except Exception as e:
            logger.error(f"Failed to start audio stream: {e}")
            self.is_listening = False
            return False

        logger.info("Sierra audio safety monitoring started")

        # Speak confirmation if voice available
        if self.voice_cortex:
            self.voice_cortex.speak_gentle(
                "Audio safety monitoring is now active. I'm here to help keep you safe."
            )

        return True

    def stop_monitoring(self) -> bool:
        """Stop audio safety monitoring"""
        if not self.is_listening:
            logger.warning("Audio safety monitoring is not active")
            return False

        self.is_listening = False
        if hasattr(self, "stream"):
            self.stream.stop()
            self.stream.close()

        logger.info("Sierra audio safety monitoring stopped")

        # Speak confirmation if voice available and not in crisis
        if self.voice_cortex and not self.crisis_mode_active:
            self.voice_cortex.speak("Audio monitoring stopped.")

        return True

    def _audio_callback(self, indata, frames, time_info, status):
        """Audio stream callback - captures raw audio"""
        if status:
            logger.debug(f"Audio callback status: {status}")
        self.audio_queue.put(indata.copy())

    def _start_audio_processing_thread(self):
        """Start background thread for audio processing"""
        thread = threading.Thread(target=self._audio_processing_loop)
        thread.daemon = True
        thread.start()

    def _audio_processing_loop(self):
        """Main audio processing loop - runs in background thread"""
        try:
            while self.is_listening:
                try:
                    audio_chunk = self.audio_queue.get(timeout=1.0)

                    # Dual analysis:
                    # 1. Speech detection (what user is saying)
                    # 2. Danger detection (what's happening around them)

                    self._process_audio_chunk(audio_chunk)

                except queue.Empty:
                    continue
        except Exception as e:
            logger.error(f"Error in audio processing loop: {e}", exc_info=True)
            self.is_listening = False

    def _process_audio_chunk(self, audio_chunk: np.ndarray):
        """
        Process audio chunk with dual analysis:
        1. Speech recognition
        2. Danger detection
        """
        # Add to buffer
        self.audio_buffer.append(audio_chunk.flatten())

        # Limit buffer size (5 seconds max)
        max_buffer_size = int(AUDIO_SAMPLE_RATE * 5)
        total_samples = sum(len(chunk) for chunk in self.audio_buffer)
        while total_samples > max_buffer_size and self.audio_buffer:
            removed = self.audio_buffer.pop(0)
            total_samples -= len(removed)

        # Convert to bytes for danger analysis
        audio_bytes = audio_chunk.astype(np.float32).tobytes()

        # DANGER DETECTION (always run - critical for safety)
        danger_assessment = self.danger_service.analyze_audio(audio_bytes)

        # Track danger level changes
        if danger_assessment.danger_level != self.current_danger_level:
            self._handle_danger_level_change(danger_assessment)

        self.current_danger_level = danger_assessment.danger_level
        self.danger_history.append(danger_assessment)

        # Trigger danger callbacks
        if danger_assessment.danger_level.value >= DangerLevel.ELEVATED.value:
            for callback in self.danger_callbacks:
                callback(danger_assessment)

        # CRISIS DETECTION
        if danger_assessment.danger_level.value >= DangerLevel.CRITICAL.value:
            self._handle_crisis(danger_assessment)

        # SPEECH DETECTION (if speech detected in chunk)
        if self._detect_speech(audio_chunk):
            self.last_speech_time = time.time()
            if self._check_speech_duration():
                # Process accumulated speech
                combined_audio = np.concatenate(self.audio_buffer)
                text, confidence, metadata = self._process_speech(combined_audio)

                if text:
                    # Trigger speech callbacks
                    for callback in self.speech_callbacks:
                        callback(text, confidence, metadata)

                    # Clear buffer after processing speech
                    self.audio_buffer = []

    def _detect_speech(self, audio_chunk: np.ndarray) -> bool:
        """Detect if audio chunk contains speech"""
        energy = np.mean(np.abs(audio_chunk))
        return energy > self.silence_threshold

    def _check_speech_duration(self) -> bool:
        """Check if speech has been long enough to process"""
        if not self.audio_buffer:
            return False
        return (time.time() - self.last_speech_time) > self.min_speech_duration

    def _process_speech(self, audio_data: np.ndarray) -> Tuple[str, float, Dict[str, Any]]:
        """
        Process speech from audio data
        (Interface - production would use Whisper API or similar)
        """
        # Calculate audio features
        frame_size = int(AUDIO_SAMPLE_RATE * 0.02)
        frames = [
            audio_data[i:i + frame_size]
            for i in range(0, len(audio_data), frame_size)
        ]
        energies = [
            np.mean(np.abs(frame)) for frame in frames if len(frame) == frame_size
        ]

        if not energies:
            return "", 0.0, {"error": "No audio data"}

        avg_energy = np.mean(energies)

        if avg_energy > self.silence_threshold * 2:
            # Speech detected - in production, this would call Whisper API
            text = "[Speech detected - transcription would appear here]"
            confidence = min(max(avg_energy / (self.silence_threshold * 4), 0.1), 0.9)

            return text, confidence, {
                "language": self.language,
                "duration": len(audio_data) / AUDIO_SAMPLE_RATE,
                "timestamp": time.time(),
                "energy": float(avg_energy)
            }

        return "", 0.0, {"error": "No clear speech detected"}

    def _handle_danger_level_change(self, assessment: AudioDangerAssessment):
        """Handle danger level change"""
        old_level = self.current_danger_level
        new_level = assessment.danger_level

        logger.warning(
            f"Danger level changed: {old_level.name} → {new_level.name} "
            f"(confidence: {assessment.confidence:.2f})"
        )

        # If escalating to HIGH or above, speak warning
        if new_level.value >= DangerLevel.HIGH.value and self.voice_cortex:
            if new_level.value > old_level.value:  # Escalating
                self.voice_cortex.speak(
                    "I'm noticing concerning sounds. Are you safe right now?",
                    VoicePriority.HIGH,
                    emotion="urgent"
                )

    def _handle_crisis(self, assessment: AudioDangerAssessment):
        """Handle crisis-level danger detection"""
        if self.crisis_mode_active:
            return  # Already in crisis mode

        self.crisis_mode_active = True

        logger.critical(
            f"CRISIS DETECTED: {assessment.danger_level.name} "
            f"Patterns: {', '.join(assessment.patterns_detected)}"
        )

        # Trigger crisis callbacks
        for callback in self.crisis_callbacks:
            callback(assessment)

        # Immediate voice crisis response
        if self.voice_cortex:
            self.voice_cortex.speak_crisis(
                "I'm very concerned about your safety right now. "
                "If you're in immediate danger, call 911. "
                "The National Domestic Violence Hotline is 1-800-799-7233."
            )

        # Log crisis event (HIPAA-compliant - no user data)
        logger.critical(f"CRISIS ACTION: {assessment.recommended_action}")

    def get_safety_status(self) -> Dict:
        """Get current audio safety status"""
        recent_danger = self.danger_history[-5:] if self.danger_history else []

        return {
            "monitoring_active": self.is_listening,
            "current_danger_level": self.current_danger_level.name,
            "crisis_mode": self.crisis_mode_active,
            "danger_events_detected": len(self.danger_history),
            "recent_danger_levels": [d.danger_level.name for d in recent_danger],
            "escalation_detected": self.danger_service._is_escalating() if self.danger_history else False,
            "voice_cortex_available": VOICE_CORTEX_AVAILABLE
        }

    def reset_crisis_mode(self):
        """Reset crisis mode (use after danger has passed)"""
        self.crisis_mode_active = False
        logger.info("Crisis mode reset - monitoring continues")


# Global instance
_audio_safety_system = None

def get_audio_safety_system() -> SierraAudioSafetySystem:
    """Get singleton audio safety system"""
    global _audio_safety_system
    if _audio_safety_system is None:
        _audio_safety_system = SierraAudioSafetySystem()
    return _audio_safety_system


# Test execution
if __name__ == "__main__":
    print("="*70)
    print("SIERRA AUDIO SAFETY SYSTEM TEST")
    print("="*70)
    print()

    # Initialize system
    safety_system = get_audio_safety_system()

    # Define callbacks
    def on_speech(text, confidence, metadata):
        print(f"💬 Speech detected: \"{text}\" (confidence: {confidence:.2f})")

    def on_danger(assessment):
        print(f"⚠️  Danger detected: {assessment.danger_level.name}")
        print(f"   Patterns: {', '.join(assessment.patterns_detected)}")

    def on_crisis(assessment):
        print(f"🚨 CRISIS: {assessment.danger_level.name}")
        print(f"   Action: {assessment.recommended_action}")

    # Start monitoring
    if SOUNDDEVICE_AVAILABLE:
        print("Starting audio safety monitoring...")
        print("Speak or make sounds to test danger detection")
        print("Press Ctrl+C to stop")
        print()

        success = safety_system.start_monitoring(
            speech_callback=on_speech,
            danger_callback=on_danger,
            crisis_callback=on_crisis
        )

        if success:
            try:
                # Monitor for 30 seconds
                for i in range(30):
                    time.sleep(1)
                    if i % 5 == 0:
                        status = safety_system.get_safety_status()
                        print(f"\nStatus: {status['current_danger_level']} "
                              f"(Events: {status['danger_events_detected']})")
            except KeyboardInterrupt:
                print("\n\nStopping...")

            safety_system.stop_monitoring()
    else:
        print("⚠️  Sounddevice not available - cannot test live audio")
        print("Install with: pip install sounddevice")

    print("\n" + "="*70)
    print("✅ Audio Safety System test complete")
    print("🛡️  Sierra's audio protection ready")
    print("💜 Keeping survivors safe through sound")


# ==============================================================================
# © 2025 Everett Nathaniel Christman
# The Christman AI Project — Luma Cognify AI
# All rights reserved. Unauthorized use, replication, or derivative training
# of this material is prohibited.
#
# Core Directive: "How can we help you love yourself more?"
# Autonomy & Alignment Protocol v3.0
# ==============================================================================
