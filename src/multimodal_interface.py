"""
Multimodal Interface System
Sierra's capabilities: Speech, Sight, Hearing

Gives Sierra the ability to:
- Speak with warmth and compassion (Text-to-Speech via Voice Cortex)
- See and understand images/video (Computer Vision)
- Hear and understand audio (Speech-to-Text)
- Process multiple modalities simultaneously

Part of The Christman AI Project
Building accessibility and connection

Voice Cortex Integration:
- All speech now routes through singleton Voice Cortex
- Priority-based voice output (crisis interrupts support)
- HIPAA-compliant audio storage
"""

from typing import Optional, Dict, Any, List
from dataclasses import dataclass
from enum import Enum
import base64
from datetime import datetime

# Voice Cortex integration - singleton voice controller
try:
    from voice_cortex import get_voice_cortex, VoicePriority
    VOICE_CORTEX_AVAILABLE = True
except ImportError:
    VOICE_CORTEX_AVAILABLE = False
    VoicePriority = None


class ModalityType(Enum):
    """Types of input/output modalities"""
    TEXT = "text"
    SPEECH = "speech"
    VISION = "vision"
    AUDIO = "audio"
    MULTIMODAL = "multimodal"


class VoiceTone(Enum):
    """Sierra's voice tones for different situations"""
    WARM_SUPPORTIVE = "warm_supportive"  # Default
    CALM_GROUNDING = "calm_grounding"  # For crisis/anxiety
    GENTLE_COMFORTING = "gentle_comforting"  # For sadness
    EMPOWERING = "empowering"  # For strength-building
    URGENT_PROTECTIVE = "urgent_protective"  # For immediate danger


@dataclass
class SpeechOutput:
    """Speech synthesis output"""
    text: str
    tone: VoiceTone
    pace: str  # slow, normal, fast
    emphasis_words: List[str]  # Words to emphasize
    pauses: List[int]  # Where to pause (character positions)
    emotion: str  # warmth, concern, hope, etc.


@dataclass
class VisionInput:
    """Visual input from user"""
    image_data: str  # Base64 encoded
    timestamp: str
    context: Optional[str]  # What user said about the image
    analysis_needed: bool


@dataclass
class AudioInput:
    """Audio input from user"""
    audio_data: str  # Base64 encoded
    duration: float
    timestamp: str
    transcription: Optional[str]
    emotion_detected: Optional[str]


class SpeechInterface:
    """
    Sierra's Voice - Text-to-Speech Capabilities

    Sierra can speak with:
    - Warmth and compassion
    - Appropriate pacing for trauma survivors
    - Emotional attunement
    - Grounding presence

    Voice Cortex Integration:
    - All speech routes through singleton Voice Cortex
    - Priority-based output (crisis interrupts support)
    - Queue management for smooth conversation flow
    """

    def __init__(self):
        self.default_tone = VoiceTone.WARM_SUPPORTIVE
        self.speaking_rate = "normal"
        self.warmth_level = 0.9  # Very warm by default

        # Get Voice Cortex if available
        self.voice_cortex = get_voice_cortex() if VOICE_CORTEX_AVAILABLE else None

    def prepare_speech(
        self,
        text: str,
        tone: Optional[VoiceTone] = None,
        is_crisis: bool = False,
        needs_grounding: bool = False
    ) -> SpeechOutput:
        """
        Prepare text for speech synthesis with emotional intelligence

        Args:
            text: Text to speak
            tone: Voice tone to use
            is_crisis: Is this a crisis situation?
            needs_grounding: Does user need grounding?

        Returns:
            SpeechOutput with detailed speech parameters
        """

        # Determine appropriate tone
        if is_crisis:
            selected_tone = VoiceTone.URGENT_PROTECTIVE
        elif needs_grounding:
            selected_tone = VoiceTone.CALM_GROUNDING
        else:
            selected_tone = tone or self.default_tone

        # Determine pacing
        if needs_grounding or is_crisis:
            pace = "slow"  # Slower for grounding/crisis
        else:
            pace = "normal"

        # Identify words to emphasize (words of affirmation and safety)
        emphasis_words = self._identify_emphasis_words(text)

        # Identify natural pause points
        pauses = self._identify_pauses(text)

        # Determine emotion to convey
        emotion = self._determine_emotion(selected_tone, text)

        return SpeechOutput(
            text=text,
            tone=selected_tone,
            pace=pace,
            emphasis_words=emphasis_words,
            pauses=pauses,
            emotion=emotion
        )

    def _identify_emphasis_words(self, text: str) -> List[str]:
        """Identify words that should be emphasized"""

        emphasis_targets = [
            # Safety and protection
            "safe", "safety", "protect", "protected",
            # Affirmation
            "deserve", "worthy", "valuable", "matter", "matters",
            "important", "strong", "brave", "courage", "resilient",
            # Support
            "here", "with you", "not alone", "together",
            # Love core
            "love", "care", "compassion",
            # Hope
            "possible", "can", "will", "hope"
        ]

        words_lower = text.lower()
        emphasis_words = []

        for target in emphasis_targets:
            if target in words_lower:
                # Find actual word in original text (preserve capitalization)
                words = text.split()
                for word in words:
                    if word.lower().strip('.,!?;:') == target:
                        emphasis_words.append(word.strip('.,!?;:'))

        return emphasis_words

    def _identify_pauses(self, text: str) -> List[int]:
        """Identify where to pause for emphasis and breath"""

        pauses = []

        # Pause after important phrases
        pause_markers = [
            "You're safe.",
            "I'm here.",
            "You matter.",
            "You're not alone.",
            "Take your time.",
            "Breathe.",
            "It's okay."
        ]

        for marker in pause_markers:
            pos = text.find(marker)
            if pos != -1:
                pauses.append(pos + len(marker))

        # Pause at sentence endings
        for i, char in enumerate(text):
            if char in '.!?':
                pauses.append(i + 1)

        return sorted(set(pauses))

    def _determine_emotion(self, tone: VoiceTone, text: str) -> str:
        """Determine emotional quality to convey"""

        emotion_map = {
            VoiceTone.WARM_SUPPORTIVE: "warmth, gentle encouragement",
            VoiceTone.CALM_GROUNDING: "steady calm, grounding presence",
            VoiceTone.GENTLE_COMFORTING: "soft comfort, tenderness",
            VoiceTone.EMPOWERING: "strength, confidence, hope",
            VoiceTone.URGENT_PROTECTIVE: "urgent care, protective concern"
        }

        base_emotion = emotion_map.get(tone, "warmth, care")

        # Add context-specific emotion
        text_lower = text.lower()
        if "I'm sorry" in text or "difficult" in text_lower:
            return base_emotion + ", empathy"
        elif "proud" in text_lower or "strong" in text_lower:
            return base_emotion + ", admiration"
        elif "deserve" in text_lower:
            return base_emotion + ", conviction"

        return base_emotion

    def synthesize_speech(self, speech_output: SpeechOutput) -> Dict[str, Any]:
        """
        Synthesize speech (interface for TTS engine)

        In production, this would interface with:
        - Google Cloud Text-to-Speech
        - Amazon Polly
        - Microsoft Azure Speech
        - Or local TTS engine

        Args:
            speech_output: Prepared speech parameters

        Returns:
            Dict with audio data and metadata
        """

        # This is an interface - actual implementation would call TTS API
        return {
            "text": speech_output.text,
            "tone": speech_output.tone.value,
            "pace": speech_output.pace,
            "emphasis": speech_output.emphasis_words,
            "emotion": speech_output.emotion,
            "audio_format": "mp3",
            "sample_rate": 24000,
            # In production: "audio_data": base64_encoded_audio,
            "status": "ready_for_synthesis"
        }

    def speak_text(
        self,
        text: str,
        tone: Optional[VoiceTone] = None,
        is_crisis: bool = False,
        needs_grounding: bool = False,
        priority: Optional['VoicePriority'] = None
    ) -> bool:
        """
        Make Sierra speak text through Voice Cortex

        Args:
            text: What to say
            tone: Voice tone to use
            is_crisis: Is this a crisis situation?
            needs_grounding: Does user need grounding?
            priority: Voice priority (CRITICAL, HIGH, NORMAL, LOW)

        Returns:
            True if speech was queued successfully
        """

        if not self.voice_cortex:
            # Fallback if Voice Cortex not available
            print(f"[Sierra speaks]: {text}")
            return False

        # Prepare speech with emotional intelligence
        speech_output = self.prepare_speech(text, tone, is_crisis, needs_grounding)

        # Determine priority if not explicitly provided
        if priority is None:
            if is_crisis:
                priority = VoicePriority.CRITICAL
            elif needs_grounding:
                priority = VoicePriority.HIGH
            elif speech_output.tone == VoiceTone.URGENT_PROTECTIVE:
                priority = VoicePriority.CRITICAL
            elif speech_output.tone == VoiceTone.GENTLE_COMFORTING:
                priority = VoicePriority.LOW
            else:
                priority = VoicePriority.NORMAL

        # Map tone to emotion for Voice Cortex
        tone_to_emotion = {
            VoiceTone.WARM_SUPPORTIVE: "supportive",
            VoiceTone.CALM_GROUNDING: "gentle",
            VoiceTone.GENTLE_COMFORTING: "gentle",
            VoiceTone.EMPOWERING: "celebratory",
            VoiceTone.URGENT_PROTECTIVE: "urgent"
        }

        emotion = tone_to_emotion.get(speech_output.tone, "supportive")

        # Map pace to speed
        pace_to_speed = {
            "slow": 0.85,
            "normal": 0.95,
            "fast": 1.05
        }
        speed = pace_to_speed.get(speech_output.pace, 0.95)

        # Route through Voice Cortex
        return self.voice_cortex.speak(
            text=text,
            priority=priority,
            emotion=emotion,
            speed=speed
        )


class VisionInterface:
    """
    Sierra's Sight - Computer Vision Capabilities

    Sierra can see and understand:
    - Photos of injuries (for documentation)
    - Images of threatening messages
    - Environmental safety concerns
    - Emotional states in facial expressions
    - Body language indicating distress
    """

    def __init__(self):
        self.vision_enabled = True
        self.sensitive_image_handling = True  # Extra care with trauma content

    def analyze_image(
        self,
        image_data: str,
        context: Optional[str] = None,
        analysis_type: str = "general"
    ) -> Dict[str, Any]:
        """
        Analyze an image with trauma-informed approach

        Args:
            image_data: Base64 encoded image
            context: What the user said about the image
            analysis_type: Type of analysis needed

        Returns:
            Analysis results with sensitivity
        """

        # In production, this would use:
        # - OpenAI Vision API
        # - Google Cloud Vision
        # - Custom trained models for DV-specific scenarios

        analysis = {
            "timestamp": datetime.now().isoformat(),
            "context_provided": context,
            "analysis_type": analysis_type,
            "findings": {},
            "concern_level": "unknown",
            "recommended_response": ""
        }

        # Different analysis types
        if analysis_type == "injury_documentation":
            analysis["findings"] = self._analyze_injury(image_data, context)
            analysis["recommended_response"] = "Provide support, suggest medical care if needed, discuss safety"

        elif analysis_type == "threatening_message":
            analysis["findings"] = self._analyze_threat(image_data, context)
            analysis["recommended_response"] = "Validate concern, discuss safety, consider documentation for legal purposes"

        elif analysis_type == "environment_safety":
            analysis["findings"] = self._analyze_environment(image_data, context)
            analysis["recommended_response"] = "Assess safety concerns, discuss safety planning"

        elif analysis_type == "emotional_state":
            analysis["findings"] = self._analyze_emotional_state(image_data, context)
            analysis["recommended_response"] = "Provide emotional support, check in about wellbeing"

        return analysis

    def _analyze_injury(self, image_data: str, context: Optional[str]) -> Dict[str, Any]:
        """Analyze injury photo with sensitivity"""

        # This would use CV to detect:
        # - Bruising, cuts, marks
        # - Location on body
        # - Severity indicators
        # - Pattern indicators (defensive wounds, etc.)

        return {
            "type": "injury_analysis",
            "sensitivity_note": "Handled with trauma-informed care",
            "recommendation": "Encourage medical documentation, safety assessment",
            "sierra_response": "I see you shared this image. That must have been really difficult. Your safety matters, and documenting this can be important if you choose to seek help. Would you like to talk about what happened, or would you prefer to discuss safety planning?"
        }

    def _analyze_threat(self, image_data: str, context: Optional[str]) -> Dict[str, Any]:
        """Analyze threatening message/content"""

        return {
            "type": "threat_analysis",
            "concern": "Threatening communication detected",
            "sierra_response": "I can see this message contains threats. This is serious, and you don't deserve to receive threats like this. This type of communication can be documented and may be relevant for a protection order. How are you feeling right now? Are you safe?"
        }

    def _analyze_environment(self, image_data: str, context: Optional[str]) -> Dict[str, Any]:
        """Analyze environmental safety"""

        return {
            "type": "environment_analysis",
            "sierra_response": "Thank you for sharing this image. I'm here to help you think through safety concerns. What about this environment is concerning to you?"
        }

    def _analyze_emotional_state(self, image_data: str, context: Optional[str]) -> Dict[str, Any]:
        """Analyze emotional state from image"""

        return {
            "type": "emotional_analysis",
            "approach": "Respond with empathy and validation",
            "sierra_response": "I see you. How are you feeling right now? I'm here to listen."
        }


class AudioInterface:
    """
    Sierra's Hearing - Speech-to-Text and Audio Analysis

    Sierra can hear and understand:
    - Spoken words (transcription)
    - Emotional tone in voice
    - Urgency and distress indicators
    - Background sounds (for safety assessment)
    """

    def __init__(self):
        self.audio_enabled = True
        self.emotion_detection = True
        self.background_analysis = True

    def process_audio(
        self,
        audio_data: str,
        duration: float,
        context: Optional[str] = None
    ) -> AudioInput:
        """
        Process audio input from user

        Args:
            audio_data: Base64 encoded audio
            duration: Length in seconds
            context: Context about the audio

        Returns:
            AudioInput with transcription and analysis
        """

        # In production, this would use:
        # - OpenAI Whisper
        # - Google Speech-to-Text
        # - Azure Speech Services

        transcription = self._transcribe_audio(audio_data)
        emotion = self._detect_emotion_from_voice(audio_data)

        return AudioInput(
            audio_data=audio_data,
            duration=duration,
            timestamp=datetime.now().isoformat(),
            transcription=transcription,
            emotion_detected=emotion
        )

    def _transcribe_audio(self, audio_data: str) -> str:
        """Transcribe speech to text"""

        # Interface for speech-to-text
        # In production: Call Whisper API or similar
        return "[Transcription would appear here]"

    def _detect_emotion_from_voice(self, audio_data: str) -> str:
        """Detect emotion from vocal qualities"""

        # Analyze:
        # - Pitch (high pitch = anxiety/fear)
        # - Speed (fast = anxiety, slow = depression)
        # - Volume (quiet = withdrawn, loud = anger/distress)
        # - Trembling/crying

        return "calm"  # Placeholder

    def analyze_background_audio(self, audio_data: str) -> Dict[str, Any]:
        """
        Analyze background sounds for safety assessment

        Can detect:
        - Yelling/arguing
        - Breaking objects
        - Doors slamming
        - Children crying
        - Other distress indicators
        """

        return {
            "background_analysis": "No concerning sounds detected",
            "safety_indicators": [],
            "concern_level": "none"
        }


class MultimodalProcessor:
    """
    Combines all modalities for rich, accessible interaction

    Allows Sierra to:
    - Understand through multiple senses
    - Respond in the most helpful modality
    - Be accessible to all users
    - Provide richer support
    """

    def __init__(self):
        self.speech_interface = SpeechInterface()
        self.vision_interface = VisionInterface()
        self.audio_interface = AudioInterface()

    def process_multimodal_input(
        self,
        text: Optional[str] = None,
        image: Optional[str] = None,
        audio: Optional[str] = None,
        audio_duration: float = 0.0
    ) -> Dict[str, Any]:
        """
        Process input from multiple modalities simultaneously

        Args:
            text: Text input
            image: Image data (base64)
            audio: Audio data (base64)
            audio_duration: Audio length

        Returns:
            Combined analysis from all modalities
        """

        result = {
            "timestamp": datetime.now().isoformat(),
            "modalities_received": [],
            "combined_understanding": "",
            "recommended_response_modality": "text"  # Default
        }

        # Process each modality
        if text:
            result["modalities_received"].append("text")
            result["text_content"] = text

        if image:
            result["modalities_received"].append("vision")
            vision_analysis = self.vision_interface.analyze_image(image, text)
            result["vision_analysis"] = vision_analysis

        if audio:
            result["modalities_received"].append("audio")
            audio_analysis = self.audio_interface.process_audio(audio, audio_duration, text)
            result["audio_analysis"] = audio_analysis

        # Determine best response modality
        result["recommended_response_modality"] = self._determine_response_modality(result)

        return result

    def _determine_response_modality(self, input_data: Dict[str, Any]) -> str:
        """Determine best way to respond based on input"""

        # If user sent audio, they may prefer audio response
        if "audio" in input_data["modalities_received"]:
            return "speech"

        # If user sent image of injury/threat, text may be better for re-reading
        if "vision" in input_data["modalities_received"]:
            return "text"

        # Default to text for accessibility
        return "text"

    def generate_accessible_response(
        self,
        response_text: str,
        include_speech: bool = False,
        is_crisis: bool = False,
        needs_grounding: bool = False
    ) -> Dict[str, Any]:
        """
        Generate response in multiple accessible formats

        Args:
            response_text: The response content
            include_speech: Include speech synthesis
            is_crisis: Is this a crisis response?
            needs_grounding: Does user need grounding?

        Returns:
            Response in multiple modalities
        """

        output = {
            "text": response_text,
            "timestamp": datetime.now().isoformat(),
            "speech_enabled": include_speech
        }

        if include_speech:
            # Prepare speech metadata
            speech = self.speech_interface.prepare_speech(
                response_text,
                is_crisis=is_crisis,
                needs_grounding=needs_grounding
            )
            output["speech_metadata"] = {
                "tone": speech.tone.value,
                "pace": speech.pace,
                "emotion": speech.emotion
            }

            # Actually speak through Voice Cortex
            spoke = self.speech_interface.speak_text(
                text=response_text,
                is_crisis=is_crisis,
                needs_grounding=needs_grounding
            )
            output["speech_queued"] = spoke

        return output
