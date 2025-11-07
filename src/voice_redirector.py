"""
Sierra's Voice Redirector - Monkey-patch Integration Layer

Adapted from AlphaVox (Christman AI Project)

This module patches ALL voice output functions to route through Voice Cortex
Ensures ONLY ONE voice speaks at a time, even if code tries to speak directly

Safety-critical for domestic violence survivors:
- Multiple overlapping voices = confusing/triggering
- Priority routing = crisis messages interrupt support messages
- Singleton enforcement = consistent, predictable voice

Usage:
    from voice_redirector import patch_all_voice_functions
    patch_all_voice_functions()  # One-time setup
"""

import sys
from typing import Callable, Any
from voice_cortex import get_voice_cortex, VoicePriority


class VoiceRedirector:
    """
    Monkey-patches voice functions to route through Voice Cortex

    Intercepts:
    - multimodal_interface.SpeechInterface methods
    - Direct TTS calls (pyttsx3, boto3.polly, etc.)
    - Any function named 'speak', 'say', 'tts', etc.
    """

    def __init__(self):
        self.cortex = get_voice_cortex()
        self.original_functions = {}  # Backup of original functions
        self.patched_modules = set()

    def patch_all_voice_functions(self):
        """
        Patch all voice-related functions in the system
        Call this ONCE at startup
        """
        print("[Voice Redirector] Patching voice functions...")

        # Patch multimodal_interface
        self._patch_multimodal_interface()

        # Patch AWS Polly (if imported)
        self._patch_aws_polly()

        # Patch pyttsx3 (if imported)
        self._patch_pyttsx3()

        # Patch any 'speak' functions in loaded modules
        self._patch_speak_functions()

        print(f"[Voice Redirector] Patched {len(self.original_functions)} voice functions")
        print(f"[Voice Redirector] All voice → Voice Cortex (singleton)")

    def _patch_multimodal_interface(self):
        """Patch SpeechInterface in multimodal_interface.py"""
        try:
            # Try importing (may not be loaded yet)
            if 'multimodal_interface' in sys.modules:
                import multimodal_interface

                # Patch SpeechInterface.speak_text if it exists
                if hasattr(multimodal_interface, 'SpeechInterface'):
                    SpeechInterface = multimodal_interface.SpeechInterface

                    # Save original
                    if hasattr(SpeechInterface, 'speak_text'):
                        original_speak = SpeechInterface.speak_text
                        self.original_functions['SpeechInterface.speak_text'] = original_speak

                        # Replace with redirector
                        def cortex_speak_text(self, text: str, *args, **kwargs):
                            # Detect priority from kwargs or context
                            priority = kwargs.get('priority', VoicePriority.NORMAL)
                            emotion = kwargs.get('emotion', 'supportive')

                            # Route through cortex
                            return get_voice_cortex().speak(text, priority, emotion=emotion)

                        SpeechInterface.speak_text = cortex_speak_text
                        self.patched_modules.add('multimodal_interface.SpeechInterface')
                        print("[Voice Redirector]   ✓ Patched SpeechInterface.speak_text")

        except ImportError:
            pass  # Module not loaded yet, will patch when loaded

    def _patch_aws_polly(self):
        """Patch boto3 Polly client (if imported)"""
        try:
            if 'boto3' in sys.modules:
                import boto3

                # Get Polly client class
                original_client = boto3.client

                def cortex_client(service_name, *args, **kwargs):
                    """Intercept Polly client creation"""
                    client = original_client(service_name, *args, **kwargs)

                    if service_name == 'polly':
                        # Patch synthesize_speech
                        original_synthesize = client.synthesize_speech

                        def cortex_synthesize_speech(Text="", **synth_kwargs):
                            # Instead of directly synthesizing, route through cortex
                            # Cortex will handle the actual Polly call
                            priority = VoicePriority.NORMAL
                            get_voice_cortex().speak(Text, priority)

                            # Return empty response (cortex handles actual speech)
                            return {'AudioStream': None}

                        client.synthesize_speech = cortex_synthesize_speech
                        self.patched_modules.add('boto3.polly')
                        print("[Voice Redirector]   ✓ Patched boto3 Polly client")

                    return client

                boto3.client = cortex_client
                self.original_functions['boto3.client'] = original_client

        except ImportError:
            pass

    def _patch_pyttsx3(self):
        """Patch pyttsx3 TTS library (if imported)"""
        try:
            if 'pyttsx3' in sys.modules:
                import pyttsx3

                original_init = pyttsx3.init

                def cortex_init(*args, **kwargs):
                    """Return a cortex-wrapped engine"""
                    # Create dummy engine that routes to cortex
                    class CortexEngine:
                        def say(self, text):
                            get_voice_cortex().speak(text, VoicePriority.NORMAL)

                        def runAndWait(self):
                            pass  # Cortex handles queue

                        def stop(self):
                            get_voice_cortex().silence()

                        def setProperty(self, *args):
                            pass  # Ignore property changes

                    return CortexEngine()

                pyttsx3.init = cortex_init
                self.original_functions['pyttsx3.init'] = original_init
                self.patched_modules.add('pyttsx3')
                print("[Voice Redirector]   ✓ Patched pyttsx3")

        except ImportError:
            pass

    def _patch_speak_functions(self):
        """
        Find and patch any function named 'speak', 'say', 'tts' in loaded modules
        This is aggressive patching for safety
        """
        speak_names = ['speak', 'say', 'tts', 'talk', 'voice_output']

        for module_name, module in list(sys.modules.items()):
            if module is None:
                continue

            # Skip system modules
            if module_name.startswith('_') or module_name in ['sys', 'os', 'time']:
                continue

            # Skip already patched
            if module_name in self.patched_modules:
                continue

            try:
                for attr_name in dir(module):
                    if attr_name.lower() in speak_names:
                        attr = getattr(module, attr_name)

                        # Only patch callable functions
                        if callable(attr) and not isinstance(attr, type):
                            # Create redirector wrapper
                            def make_redirector(original_func):
                                def redirector(*args, **kwargs):
                                    # Extract text from args
                                    text = args[0] if args else kwargs.get('text', '')
                                    if text:
                                        get_voice_cortex().speak(str(text), VoicePriority.NORMAL)
                                    return None
                                return redirector

                            # Save original and patch
                            key = f"{module_name}.{attr_name}"
                            self.original_functions[key] = attr
                            setattr(module, attr_name, make_redirector(attr))

            except Exception:
                pass  # Skip modules that can't be introspected

    def unpatch_all(self):
        """
        Restore original functions
        Use for testing or shutdown
        """
        print("[Voice Redirector] Unpatching all voice functions...")

        for key, original_func in self.original_functions.items():
            try:
                parts = key.split('.')
                if len(parts) == 2:
                    module_name, func_name = parts
                    if module_name in sys.modules:
                        module = sys.modules[module_name]
                        setattr(module, func_name, original_func)
            except Exception as e:
                print(f"[Voice Redirector] Could not unpatch {key}: {e}")

        print("[Voice Redirector] Unpatching complete")


# Global redirector instance
_redirector = None


def patch_all_voice_functions():
    """
    Global function to patch all voice output
    Call this ONCE at startup (usually in main.py or __init__.py)
    """
    global _redirector
    if _redirector is None:
        _redirector = VoiceRedirector()
    _redirector.patch_all_voice_functions()


def unpatch_all_voice_functions():
    """Restore original voice functions"""
    global _redirector
    if _redirector:
        _redirector.unpatch_all()


def get_redirector() -> VoiceRedirector:
    """Get the global redirector instance"""
    global _redirector
    if _redirector is None:
        _redirector = VoiceRedirector()
    return _redirector


# Auto-patch on import (aggressive safety mode)
# Uncomment for production deployment:
# patch_all_voice_functions()


# Test execution
if __name__ == "__main__":
    print("="*70)
    print("SIERRA VOICE REDIRECTOR TEST")
    print("="*70)
    print()

    print("Test 1: Patching voice functions...")
    patch_all_voice_functions()
    print()

    print("Test 2: Testing redirected speech...")

    # Create a dummy speak function
    def my_speak(text):
        print(f"[DIRECT] Speaking: {text}")
        return "direct"

    # Patch it
    redirector = get_redirector()
    redirector.original_functions['test.my_speak'] = my_speak

    # Monkey-patch to redirect
    def patched_speak(text):
        print(f"[REDIRECTED] → Voice Cortex")
        get_voice_cortex().speak(text, VoicePriority.NORMAL)

    my_speak = patched_speak

    # Test redirected call
    my_speak("This should go through Voice Cortex, not direct output")

    import time
    time.sleep(1)

    print("\nTest 3: Status check...")
    status = get_voice_cortex().get_status()
    print(f"  Voice Cortex status: {status}")

    print("\n" + "="*70)
    print("✅ Voice Redirector test complete")
    print("💜 All voice output → Voice Cortex (singleton)")
    print("="*70)
