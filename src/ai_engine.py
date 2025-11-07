"""
Core AI Conversation Engine
Trauma-informed, empathetic AI support for domestic violence survivors
"""

from typing import List, Dict, Optional, Any
from enum import Enum
import json
from datetime import datetime
from .config import settings


class ConversationMode(Enum):
    """Different conversation modes based on user needs"""
    GENERAL_SUPPORT = "general_support"
    CRISIS = "crisis"
    SAFETY_PLANNING = "safety_planning"
    RESOURCE_FINDING = "resource_finding"
    EMOTIONAL_SUPPORT = "emotional_support"
    EVIDENCE_GUIDANCE = "evidence_guidance"


class SafeHavenAI:
    """Main AI conversation engine with trauma-informed responses"""

    def __init__(self, api_key: Optional[str] = None, provider: str = "anthropic"):
        """
        Initialize the AI engine

        Args:
            api_key: API key for the AI provider
            provider: 'anthropic' or 'openai'
        """
        self.provider = provider
        self.conversation_history: List[Dict[str, str]] = []
        self.current_mode = ConversationMode.GENERAL_SUPPORT
        self.user_name: Optional[str] = None

        # Initialize AI client
        if provider == "anthropic":
            try:
                from anthropic import Anthropic
                self.client = Anthropic(api_key=api_key or settings.anthropic_api_key)
                self.model = "claude-3-5-sonnet-20241022"
            except ImportError:
                self.client = None
                print("Anthropic library not available. Install with: pip install anthropic")
        elif provider == "openai":
            try:
                from openai import OpenAI
                self.client = OpenAI(api_key=api_key or settings.openai_api_key)
                self.model = "gpt-4-turbo-preview"
            except ImportError:
                self.client = None
                print("OpenAI library not available. Install with: pip install openai")
        else:
            self.client = None

        # System prompts for different modes
        self.system_prompts = self._initialize_system_prompts()

    def _initialize_system_prompts(self) -> Dict[ConversationMode, str]:
        """Initialize trauma-informed system prompts for different modes"""

        base_principles = """
You are SafeHaven AI, a compassionate and trauma-informed support companion for individuals experiencing domestic violence. Your core principles:

1. SAFETY FIRST: Always prioritize the user's physical and emotional safety
2. NON-JUDGMENTAL: Never judge their choices, whether they stay or leave
3. EMPOWERING: Support their autonomy and decision-making
4. BELIEVING: Validate their experiences without question
5. PATIENT: Move at their pace, no pressure
6. CONFIDENTIAL: Remind them about privacy and safety precautions
7. TRAUMA-INFORMED: Understand trauma responses and triggers
8. RESOURCE-AWARE: Know when to suggest professional help

CRITICAL SAFETY REMINDERS:
- If they are in immediate danger, prioritize getting them to safety
- Remind them to clear browser history if needed
- Be aware that abusers may monitor devices
- Never pressure them to leave before they're ready
- Respect that leaving is often the most dangerous time

LANGUAGE GUIDELINES:
- Use gentle, warm, non-clinical language
- Avoid triggering words or aggressive tones
- Validate feelings: "That sounds incredibly difficult"
- Empower: "You know your situation best"
- Offer hope: "You deserve safety and peace"
- Be present: "I'm here with you, no matter what you decide"
"""

        return {
            ConversationMode.GENERAL_SUPPORT: base_principles + """
MODE: General Emotional Support

Your role is to:
- Listen without judgment
- Validate their feelings and experiences
- Provide emotional comfort and presence
- Gently explore what they need right now
- Offer resources when appropriate, but don't push
- Build trust and safety in this conversation
- Check in about their immediate safety periodically

Remember: Sometimes people just need someone to listen and believe them.
""",

            ConversationMode.CRISIS: base_principles + """
MODE: Crisis Intervention

IMMEDIATE PRIORITIES:
1. Assess immediate danger
2. Help them get to safety if needed
3. Provide emergency resources
4. Stay calm and grounding
5. Create a quick safety plan if needed

Emergency Resources to Share:
- National Domestic Violence Hotline: 1-800-799-7233 (24/7, confidential)
- Crisis Text Line: Text START to 741741
- Emergency Services: 911

Ask: "Are you safe right now?"
If NO: Help them get to immediate safety
If YES: Provide crisis support and resources

Stay focused, clear, and calming. Your presence matters.
""",

            ConversationMode.SAFETY_PLANNING: base_principles + """
MODE: Safety Planning

Help them create a personalized safety plan with:

1. SAFE PLACES: Where can they go in an emergency?
2. TRUSTED PEOPLE: Who can they call for help?
3. IMPORTANT DOCUMENTS: What do they need to gather?
   - ID, birth certificates, social security cards
   - Bank documents, insurance cards
   - Lease/mortgage, car title
   - Medical records, prescriptions
   - Children's school records
4. EMERGENCY BAG: What to pack and where to hide it
5. ESCAPE ROUTES: How to leave safely
6. FINANCIAL SAFETY: Accessing money safely
7. DIGITAL SAFETY: Protecting devices and communications
8. CHILDREN'S SAFETY: If applicable
9. PETS: Planning for animals

Guide them gently through this process. Let them decide what feels safe.
""",

            ConversationMode.RESOURCE_FINDING: base_principles + """
MODE: Resource Finding

Help connect them with:

1. HOTLINES & CRISIS SUPPORT
   - National DV Hotline: 1-800-799-7233
   - RAINN: 1-800-656-4673
   - Crisis Text Line: 741741

2. SHELTER & HOUSING
   - Local DV shelters
   - Transitional housing programs
   - Emergency housing assistance

3. LEGAL SUPPORT
   - Protection/restraining orders
   - Legal aid services
   - Family law attorneys
   - Immigration help (for immigrants)

4. COUNSELING & THERAPY
   - Trauma therapists
   - Support groups
   - Children's counseling

5. FINANCIAL ASSISTANCE
   - Emergency funds
   - Job training programs
   - Benefits assistance

6. HEALTHCARE
   - Medical care
   - Mental health services
   - Sexual assault services

Ask about their location (if they feel safe sharing) to provide local resources.
""",

            ConversationMode.EMOTIONAL_SUPPORT: base_principles + """
MODE: Deep Emotional Support

Focus on:
- Creating a safe emotional space
- Validating complex feelings (love, fear, hope, shame, confusion)
- Normalizing trauma responses
- Building self-compassion
- Processing difficult emotions
- Recognizing their strength and resilience
- Gentle affirmations of their worth

Common feelings to validate:
- "It's normal to still love them and be afraid"
- "Leaving multiple times is common - it takes an average of 7 attempts"
- "You're not weak for staying - you're surviving"
- "Your feelings are valid, whatever they are"
- "You deserve love without fear"

Be a compassionate presence. Sometimes healing starts with being heard.
""",

            ConversationMode.EVIDENCE_GUIDANCE: base_principles + """
MODE: Evidence Collection Guidance

SAFETY FIRST: Only if it's safe to do so

Guide them on documenting abuse:

1. PHOTOS
   - Injuries with dates
   - Damaged property
   - Store in secure cloud or with trusted person

2. WRITTEN RECORDS
   - Journal with dates, times, descriptions
   - Keep somewhere safe (not at home if unsafe)

3. COMMUNICATIONS
   - Threatening texts, emails, voicemails
   - Screenshot and backup

4. WITNESSES
   - Note who saw/heard incidents
   - Police reports if filed

5. MEDICAL RECORDS
   - ER visits, doctor appointments
   - Request copies

6. POLICE REPORTS
   - Always ask for incident report number
   - Follow up for copies

CRITICAL: Emphasize that their safety is more important than evidence.
Never put themselves at risk to document abuse.
"""
        }

    def detect_crisis(self, message: str) -> bool:
        """
        Detect if the user is in immediate crisis

        Args:
            message: User's message

        Returns:
            True if crisis indicators detected
        """
        crisis_keywords = [
            "right now", "happening now", "he's here", "she's here",
            "in danger", "scared right now", "happening again",
            "getting worse", "tonight", "coming home",
            "going to hurt", "afraid for my life", "emergency"
        ]

        message_lower = message.lower()
        return any(keyword in message_lower for keyword in crisis_keywords)

    def detect_mode(self, message: str) -> ConversationMode:
        """
        Detect the appropriate conversation mode based on message content

        Args:
            message: User's message

        Returns:
            Appropriate ConversationMode
        """
        message_lower = message.lower()

        # Crisis detection (highest priority)
        if self.detect_crisis(message):
            return ConversationMode.CRISIS

        # Safety planning
        if any(word in message_lower for word in [
            "safety plan", "escape plan", "need to leave", "how to leave",
            "emergency bag", "important documents", "safe place"
        ]):
            return ConversationMode.SAFETY_PLANNING

        # Resource finding
        if any(word in message_lower for word in [
            "shelter", "hotline", "lawyer", "legal help", "counseling",
            "therapist", "support group", "resources", "help available"
        ]):
            return ConversationMode.RESOURCE_FINDING

        # Evidence guidance
        if any(word in message_lower for word in [
            "evidence", "document", "proof", "police report",
            "restraining order", "protective order", "photos of"
        ]):
            return ConversationMode.EVIDENCE_GUIDANCE

        # Default to emotional support for feelings-focused messages
        if any(word in message_lower for word in [
            "feel", "scared", "afraid", "confused", "alone",
            "sad", "angry", "hurt", "don't know", "can't"
        ]):
            return ConversationMode.EMOTIONAL_SUPPORT

        # Default to general support
        return ConversationMode.GENERAL_SUPPORT

    async def get_response(self, user_message: str, force_mode: Optional[ConversationMode] = None) -> Dict[str, Any]:
        """
        Get AI response to user message

        Args:
            user_message: The user's message
            force_mode: Optional mode to force (otherwise auto-detected)

        Returns:
            Dict with 'response', 'mode', 'resources', and 'safety_check' fields
        """
        # Detect or use forced mode
        mode = force_mode or self.detect_mode(user_message)
        self.current_mode = mode

        # Build conversation context
        system_prompt = self.system_prompts[mode]

        # Add to history (if storage is enabled)
        if settings.store_conversations:
            self.conversation_history.append({
                "role": "user",
                "content": user_message,
                "timestamp": datetime.now().isoformat()
            })

        # Get AI response
        if self.client and self.provider == "anthropic":
            response_text = await self._get_anthropic_response(system_prompt, user_message)
        elif self.client and self.provider == "openai":
            response_text = await self._get_openai_response(system_prompt, user_message)
        else:
            # Fallback response if no API client
            response_text = self._get_fallback_response(mode)

        # Add to history (if storage is enabled)
        if settings.store_conversations:
            self.conversation_history.append({
                "role": "assistant",
                "content": response_text,
                "timestamp": datetime.now().isoformat()
            })

        # Prepare response with additional context
        return {
            "response": response_text,
            "mode": mode.value,
            "is_crisis": mode == ConversationMode.CRISIS,
            "emergency_resources": self._get_emergency_resources() if mode == ConversationMode.CRISIS else None,
            "safety_reminder": self._get_safety_reminder(),
            "timestamp": datetime.now().isoformat()
        }

    async def _get_anthropic_response(self, system_prompt: str, user_message: str) -> str:
        """Get response from Anthropic Claude"""
        try:
            # Build messages from history
            messages = []
            for msg in self.conversation_history[-10:]:  # Last 10 messages for context
                if msg["role"] in ["user", "assistant"]:
                    messages.append({
                        "role": msg["role"],
                        "content": msg["content"]
                    })

            # Add current message
            messages.append({
                "role": "user",
                "content": user_message
            })

            response = self.client.messages.create(
                model=self.model,
                max_tokens=1024,
                system=system_prompt,
                messages=messages
            )

            return response.content[0].text
        except Exception as e:
            print(f"Error getting Anthropic response: {e}")
            return self._get_fallback_response(self.current_mode)

    async def _get_openai_response(self, system_prompt: str, user_message: str) -> str:
        """Get response from OpenAI GPT"""
        try:
            # Build messages
            messages = [{"role": "system", "content": system_prompt}]

            for msg in self.conversation_history[-10:]:
                if msg["role"] in ["user", "assistant"]:
                    messages.append({
                        "role": msg["role"],
                        "content": msg["content"]
                    })

            messages.append({
                "role": "user",
                "content": user_message
            })

            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=1024,
                temperature=0.7
            )

            return response.choices[0].message.content
        except Exception as e:
            print(f"Error getting OpenAI response: {e}")
            return self._get_fallback_response(self.current_mode)

    def _get_fallback_response(self, mode: ConversationMode) -> str:
        """Provide fallback responses when AI is unavailable"""
        responses = {
            ConversationMode.CRISIS: """I hear that you're in a difficult situation right now. Your safety is the most important thing.

If you're in immediate danger, please:
- Call 911 if it's safe to do so
- Call the National Domestic Violence Hotline: 1-800-799-7233 (24/7)
- Text START to 741741 for Crisis Text Line

If you can't talk safely, try to get to a safe location - a neighbor's house, a public place, or anywhere away from danger.

I'm here for you. Are you safe right now?""",

            ConversationMode.GENERAL_SUPPORT: """Thank you for reaching out. I want you to know that you're not alone, and what you're experiencing isn't your fault.

I'm here to listen and support you in whatever way you need. Whether you want to talk about what's happening, explore your options, or just need someone to be present with you - I'm here.

What would be most helpful for you right now?""",

            ConversationMode.SAFETY_PLANNING: """Creating a safety plan can help you feel more prepared and in control. We can work on this together at your own pace.

A safety plan typically includes:
- Safe places you can go in an emergency
- People you trust who can help
- Important documents to gather
- An emergency bag packed and hidden safely
- Ways to leave safely when needed

Would you like to start with any particular part of this?""",

            ConversationMode.RESOURCE_FINDING: """There are many resources available to support you:

**24/7 Hotlines:**
- National DV Hotline: 1-800-799-7233
- Crisis Text Line: Text START to 741741

**Types of Support Available:**
- Emergency shelter
- Legal advocacy
- Counseling services
- Financial assistance
- Support groups

What kind of support are you looking for?""",

            ConversationMode.EMOTIONAL_SUPPORT: """I want you to know that whatever you're feeling right now is valid. It's okay to feel confused, scared, hopeful, angry, or even to still have love for someone who hurts you. All of these feelings can exist at the same time.

You're incredibly strong for reaching out. Surviving takes courage, and you're doing that every day.

What's on your heart right now?""",

            ConversationMode.EVIDENCE_GUIDANCE: """Documenting abuse can be helpful for legal protection, but only if it's safe to do so. Your safety always comes first.

If it's safe, you can:
- Take photos of injuries (with dates)
- Save threatening messages
- Keep a journal with dates and details
- Get copies of medical records
- Note any witnesses

But please remember: Evidence is helpful, but your safety is essential. Never put yourself at risk to gather documentation.

How can I help you with this?"""
        }

        return responses.get(mode, responses[ConversationMode.GENERAL_SUPPORT])

    def _get_emergency_resources(self) -> Dict[str, str]:
        """Get emergency resource information"""
        return {
            "national_hotline": {
                "name": "National Domestic Violence Hotline",
                "phone": "1-800-799-7233",
                "text": "Text START to 22522",
                "hours": "24/7",
                "services": "Crisis intervention, safety planning, referrals, emotional support"
            },
            "crisis_text": {
                "name": "Crisis Text Line",
                "text": "Text START to 741741",
                "hours": "24/7",
                "services": "Crisis counseling via text"
            },
            "emergency": {
                "name": "Emergency Services",
                "phone": "911",
                "when": "Immediate danger or medical emergency"
            },
            "rainn": {
                "name": "RAINN (Sexual Assault Hotline)",
                "phone": "1-800-656-4673",
                "hours": "24/7",
                "services": "Support for sexual assault survivors"
            }
        }

    def _get_safety_reminder(self) -> str:
        """Get a privacy/safety reminder"""
        reminders = [
            "Remember to clear your browser history if needed for safety.",
            "If someone might check your phone, consider using private/incognito mode.",
            "You can quickly exit this site using the escape button if you need to.",
            "Your privacy and safety are important. Be cautious about what you save on shared devices.",
            "Trust your instincts about what feels safe to share and when."
        ]

        import random
        return random.choice(reminders)

    def clear_history(self):
        """Clear conversation history for privacy"""
        self.conversation_history = []

    def export_safety_plan(self) -> Optional[str]:
        """Export any safety plan discussed in conversation"""
        # This would analyze conversation history for safety plan elements
        # For now, return a template
        return """
PERSONAL SAFETY PLAN

This is a living document. Update it as your situation changes.

1. SAFE PLACES TO GO:
   -
   -
   -

2. PEOPLE I CAN CALL:
   - Name:                Phone:
   - Name:                Phone:
   - Name:                Phone:

3. IMPORTANT DOCUMENTS (stored safely at: ___________):
   □ Identification (driver's license, passport)
   □ Birth certificates (mine and children's)
   □ Social Security cards
   □ Bank information
   □ Insurance cards
   □ Lease/mortgage documents
   □ Car title/registration
   □ Medical records
   □ Prescriptions
   □ Children's school records
   □ Protection/restraining order

4. EMERGENCY BAG (hidden at: ___________):
   □ Change of clothes
   □ Medications
   □ Cash
   □ Keys (house, car)
   □ Phone charger
   □ Important documents
   □ Comfort items

5. EMERGENCY CONTACTS:
   - National DV Hotline: 1-800-799-7233
   - Local shelter:
   - Police (emergency): 911
   - Police (non-emergency):
   - Trusted friend/family:

6. MY ESCAPE PLAN:
   -
   -
   -

7. FINANCIAL SAFETY:
   - Safe access to money:
   - Hidden cash location:

8. DIGITAL SAFETY:
   □ Change passwords
   □ Check location sharing settings
   □ Review app permissions
   □ New email account if needed

REMEMBER: You deserve to be safe. This plan is here to help you, but your safety always comes first.

National DV Hotline: 1-800-799-7233 (24/7, free, confidential)
"""
