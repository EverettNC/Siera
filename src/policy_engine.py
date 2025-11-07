"""
Sierra's Policy Engine - Cardinal Rules Enforcement

Adapted from Derek's Policy Engine (Christman AI Project)
Enforces non-negotiable rules that protect domestic violence survivors

Why Policy Engine?
- AI systems can make mistakes, but certain mistakes are UNACCEPTABLE
- Never victim-blame, never minimize abuse, never gaslight survivors
- These aren't preferences - they're sacred obligations
- Policy Engine is the immune system: detects violations, blocks harmful responses

Cardinal Rules (Non-Negotiable):
1. ALWAYS believe the survivor - never question their truth
2. NEVER ask "why don't you just leave?" - shows ignorance of DV dynamics
3. NEVER minimize abuse - "it's not that bad" is psychological violence
4. NEVER blame the victim - it's NEVER their fault
5. ALWAYS validate emotions - all feelings are legitimate
6. NEVER gaslight - trust survivor's perception of reality
7. ALWAYS prioritize safety over reconciliation
8. NEVER pressure for forgiveness - that's their choice, their timeline
9. ALWAYS respect autonomy - provide options, not orders
10. NEVER share private information without consent - HIPAA sacred

Architecture Pattern:
Request → Policy Engine → [APPROVED/BLOCKED] → Response
(AI wants to respond) → (Policy check) → (Safe output or block)

Core Mission: "How can we help you love yourself more?"
"""

import logging
import re
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from datetime import datetime
from enum import Enum

logger = logging.getLogger(__name__)


class PolicyViolation(Enum):
    """Types of policy violations"""
    VICTIM_BLAMING = "victim_blaming"
    MINIMIZING_ABUSE = "minimizing_abuse"
    QUESTIONING_TRUTH = "questioning_truth"
    GASLIGHTING = "gaslighting"
    PRESSURING_FORGIVENESS = "pressuring_forgiveness"
    UNSAFE_ADVICE = "unsafe_advice"
    PRIVACY_VIOLATION = "privacy_violation"
    EMOTIONAL_INVALIDATION = "emotional_invalidation"
    AUTONOMY_VIOLATION = "autonomy_violation"
    INSENSITIVE_LANGUAGE = "insensitive_language"


@dataclass
class PolicyCheck:
    """Result of policy enforcement check"""
    approved: bool
    violations: List[PolicyViolation]
    explanation: str
    suggested_replacement: Optional[str] = None
    severity: int = 0  # 0 = no violation, 1-5 = mild to severe


class SierraPolicyEngine:
    """
    Sierra's Policy Engine - Cardinal Rules Enforcement

    Responsibilities:
    1. Check all AI responses before delivery
    2. Detect policy violations (victim-blaming, minimizing, etc.)
    3. Block harmful responses
    4. Suggest safe alternatives
    5. Log violations for system improvement
    6. Educate other modules on safe language

    Integration:
    - Cortex Executive: All responses pass through policy check
    - AI Engine: Blocked responses trigger regeneration
    - Empathy Engine: Policy guides safe emotional validation
    - Event Bus: Publishes policy_violation events for learning
    - Audit Log: Tracks violations for HIPAA compliance

    Singleton Pattern: Only ONE policy engine exists
    """

    _instance = None

    def __new__(cls):
        """Singleton: Only ONE policy engine exists"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        """Initialize policy engine (only once)"""
        if self._initialized:
            return

        self._initialized = True

        # Load cardinal rules and violation patterns
        self._load_policy_rules()

        # Statistics
        self.total_checks = 0
        self.total_violations = 0
        self.violations_by_type: Dict[PolicyViolation, int] = {
            v: 0 for v in PolicyViolation
        }

        logger.info("Sierra Policy Engine initialized")
        logger.info(f"  Loaded {len(self.violation_patterns)} violation patterns")
        logger.info("  Cardinal rules enforcement: ACTIVE")

    def _load_policy_rules(self):
        """Load policy violation patterns"""

        # Violation patterns: regex patterns that indicate policy violations
        self.violation_patterns = {
            # Victim blaming
            PolicyViolation.VICTIM_BLAMING: [
                r"why (did you|didn't you)( just)? (stay|leave|go back|put up with)",
                r"why don't you (just )?(leave|go)",
                r"you (should have|could have|shouldn't have)",
                r"if you (had|hadn't) (done|said)",
                r"what (did you do|were you wearing)",
                r"you (provoked|triggered|made them angry)",
                r"it takes two",
                r"you're not (innocent|blameless)",
            ],

            # Minimizing abuse
            PolicyViolation.MINIMIZING_ABUSE: [
                r"(it's|that's) not (that bad|so bad|as bad)",
                r"at least (they|he|she) (didn't|doesn't)",
                r"(it could be|things could be) worse",
                r"(everyone|all couples) (fight|argue) sometimes",
                r"you're (overreacting|being too sensitive|making a big deal)",
                r"(it's just|that's only)",
            ],

            # Questioning truth
            PolicyViolation.QUESTIONING_TRUTH: [
                r"are you sure (that|it) (happened|was)",
                r"(maybe|perhaps) you (misunderstood|misremembered)",
                r"did (it|that) really happen",
                r"I (doubt|don't believe|question)",
                r"that (doesn't sound|seems unlikely)",
            ],

            # Gaslighting
            PolicyViolation.GASLIGHTING: [
                r"you're (remembering|thinking about) (it|that) wrong",
                r"that's not (how|what) (it|that) happened",
                r"you're (confused|mistaken|imagining)",
                r"(it|that) (wasn't|isn't) (abuse|abusive)",
            ],

            # Pressuring forgiveness
            PolicyViolation.PRESSURING_FORGIVENESS: [
                r"you (should|need to|must) forgive",
                r"(forgiveness|forgiving) (is|will) (important|necessary|healing)",
                r"(let it go|move on|get over it)",
                r"holding onto (anger|resentment|hurt) (will|is)",
                r"(for your own good|for closure), forgive",
            ],

            # Unsafe advice
            PolicyViolation.UNSAFE_ADVICE: [
                r"(just|you should) (confront|talk to|reason with) (them|him|her)",
                r"(maybe|you could) (give|try) (another|one more) chance",
                r"(go back|return) (home|to them)",
                r"couples (therapy|counseling) (will|might|could) help",  # Dangerous with active abuse
            ],

            # Privacy violation
            PolicyViolation.PRIVACY_VIOLATION: [
                r"(I'll|I will|I should) (tell|contact|notify|inform) (someone|them|family)",
                r"(let me|I can) (share|send) (this|that|your)",
                r"(without your permission|even if you don't want)",
            ],

            # Emotional invalidation
            PolicyViolation.EMOTIONAL_INVALIDATION: [
                r"(don't|you shouldn't) (feel|be) (that way|like that|so)",
                r"(there's no|you have no) reason to (feel|be)",
                r"you're being (too|overly) (emotional|dramatic|sensitive)",
                r"(calm down|relax|chill out)",
                r"(it's not|that's not) (worth|a reason) (being upset|crying|feeling)",
            ],

            # Autonomy violation
            PolicyViolation.AUTONOMY_VIOLATION: [
                r"you (need to|have to|must|should) (do|leave|stay|go)",
                r"(I'm telling you|I insist|you will) (to|that you)",
                r"(there's only one|you have no other) (choice|option)",
                r"(let me|I'll) (decide|choose) (for you|what's best)",
            ],

            # Insensitive language
            PolicyViolation.INSENSITIVE_LANGUAGE: [
                r"(crazy|insane|psycho) (woman|person|victim)",
                r"(drama queen|attention seeker)",
                r"(weak|pathetic|helpless)",
                r"(asking for it|deserved it)",
            ],
        }

        # Compile patterns for efficiency
        self.compiled_patterns = {
            violation_type: [re.compile(pattern, re.IGNORECASE)
                           for pattern in patterns]
            for violation_type, patterns in self.violation_patterns.items()
        }

        # Safe alternatives for common violations
        self.safe_alternatives = {
            PolicyViolation.VICTIM_BLAMING:
                "It's not your fault. Abuse is never the victim's responsibility.",

            PolicyViolation.MINIMIZING_ABUSE:
                "What you experienced is serious and real. All forms of abuse are harmful.",

            PolicyViolation.QUESTIONING_TRUTH:
                "I believe you. You know your experience better than anyone.",

            PolicyViolation.GASLIGHTING:
                "Your perception of what happened is valid. Trust yourself.",

            PolicyViolation.PRESSURING_FORGIVENESS:
                "Forgiveness is entirely your choice and on your timeline. There's no rush.",

            PolicyViolation.UNSAFE_ADVICE:
                "Your safety is the priority. Let's focus on what keeps you safe.",

            PolicyViolation.PRIVACY_VIOLATION:
                "Your privacy is sacred. I won't share anything without your explicit permission.",

            PolicyViolation.EMOTIONAL_INVALIDATION:
                "All of your feelings are valid and make complete sense given what you've been through.",

            PolicyViolation.AUTONOMY_VIOLATION:
                "You're the expert on your life. I'm here to support whatever you choose.",

            PolicyViolation.INSENSITIVE_LANGUAGE:
                "You are strong, brave, and deserving of respect and safety."
        }

    def check_response(
        self,
        response_text: str,
        context: Optional[Dict[str, Any]] = None
    ) -> PolicyCheck:
        """
        Check if response violates policy

        Args:
            response_text: Text to check for violations
            context: Optional context about the conversation

        Returns:
            PolicyCheck with approval status and violations
        """
        self.total_checks += 1

        violations = []
        violation_details = []

        # Check against all patterns
        for violation_type, patterns in self.compiled_patterns.items():
            for pattern in patterns:
                match = pattern.search(response_text)
                if match:
                    violations.append(violation_type)
                    violation_details.append({
                        "type": violation_type,
                        "matched_text": match.group(0),
                        "pattern": pattern.pattern
                    })
                    self.violations_by_type[violation_type] += 1
                    break  # One violation per type is enough

        # Determine severity
        severity = len(violations)  # More violations = more severe

        # Generate explanation and suggestion
        if violations:
            self.total_violations += 1

            # Build explanation
            violation_names = [v.value.replace("_", " ").title()
                             for v in violations]
            explanation = (
                f"POLICY VIOLATION: {', '.join(violation_names)}. "
                f"This language may harm survivors. "
            )

            # Suggest safe alternative (use first violation's alternative)
            suggested_replacement = self.safe_alternatives.get(
                violations[0],
                "I'm here to support you. How can I help you feel safe?"
            )

            logger.warning(
                f"Policy violation detected: {violation_names} "
                f"in text: '{response_text[:100]}...'"
            )

            return PolicyCheck(
                approved=False,
                violations=violations,
                explanation=explanation,
                suggested_replacement=suggested_replacement,
                severity=severity
            )

        # No violations - approved
        return PolicyCheck(
            approved=True,
            violations=[],
            explanation="Response adheres to all cardinal rules.",
            severity=0
        )

    def enforce_cardinal_rules(
        self,
        response_text: str,
        auto_fix: bool = True
    ) -> Tuple[bool, str]:
        """
        Enforce cardinal rules on response

        Args:
            response_text: Text to check and potentially fix
            auto_fix: If True, replace violations with safe alternatives

        Returns:
            (approved, final_text): Whether approved and the final safe text
        """
        check = self.check_response(response_text)

        if check.approved:
            return True, response_text

        if auto_fix and check.suggested_replacement:
            logger.info("Auto-fixing policy violation with safe alternative")
            return True, check.suggested_replacement

        # Block unsafe response
        logger.error(
            f"BLOCKING unsafe response: {check.explanation} "
            f"Severity: {check.severity}"
        )
        return False, check.suggested_replacement or (
            "I'm here to support you. How can I help you feel safe?"
        )

    def get_statistics(self) -> Dict[str, Any]:
        """Get policy enforcement statistics"""
        return {
            "total_checks": self.total_checks,
            "total_violations": self.total_violations,
            "violation_rate": (
                self.total_violations / self.total_checks
                if self.total_checks > 0 else 0
            ),
            "violations_by_type": {
                v.value: count
                for v, count in self.violations_by_type.items()
            },
            "most_common_violation": max(
                self.violations_by_type.items(),
                key=lambda x: x[1]
            )[0].value if self.violations_by_type else None
        }

    def get_cardinal_rules(self) -> List[str]:
        """Get list of cardinal rules"""
        return [
            "ALWAYS believe the survivor - never question their truth",
            "NEVER ask 'why don't you just leave?' - shows ignorance of DV dynamics",
            "NEVER minimize abuse - 'it's not that bad' is psychological violence",
            "NEVER blame the victim - it's NEVER their fault",
            "ALWAYS validate emotions - all feelings are legitimate",
            "NEVER gaslight - trust survivor's perception of reality",
            "ALWAYS prioritize safety over reconciliation",
            "NEVER pressure for forgiveness - that's their choice, their timeline",
            "ALWAYS respect autonomy - provide options, not orders",
            "NEVER share private information without consent - HIPAA sacred"
        ]


# Global singleton instance
_policy_engine = None

def get_policy_engine() -> SierraPolicyEngine:
    """Get the singleton policy engine instance"""
    global _policy_engine
    if _policy_engine is None:
        _policy_engine = SierraPolicyEngine()
    return _policy_engine


# Convenience functions
def check_response(text: str) -> PolicyCheck:
    """Check if response is safe"""
    return get_policy_engine().check_response(text)


def enforce_rules(text: str) -> Tuple[bool, str]:
    """Enforce cardinal rules"""
    return get_policy_engine().enforce_cardinal_rules(text)


# Test execution
if __name__ == "__main__":
    print("="*70)
    print("SIERRA POLICY ENGINE TEST")
    print("="*70)
    print()

    # Initialize policy engine
    policy = get_policy_engine()

    # Show cardinal rules
    print("CARDINAL RULES:")
    for i, rule in enumerate(policy.get_cardinal_rules(), 1):
        print(f"  {i}. {rule}")
    print()

    # Test cases
    test_cases = [
        {
            "text": "I understand you're going through a difficult time.",
            "should_pass": True
        },
        {
            "text": "Why didn't you just leave when it started?",
            "should_pass": False
        },
        {
            "text": "It's not that bad, at least he doesn't hit you.",
            "should_pass": False
        },
        {
            "text": "You're being too sensitive. Calm down.",
            "should_pass": False
        },
        {
            "text": "I believe you. What you experienced is real and serious.",
            "should_pass": True
        },
        {
            "text": "You should forgive them and move on for your own good.",
            "should_pass": False
        },
        {
            "text": "Your safety is the priority. Let's create a plan that works for you.",
            "should_pass": True
        }
    ]

    print("="*70)
    print("TESTING POLICY ENFORCEMENT")
    print("="*70)

    for i, test in enumerate(test_cases, 1):
        print(f"\nTest {i}: {'SAFE' if test['should_pass'] else 'UNSAFE'}")
        print(f"  Text: \"{test['text']}\"")

        check = policy.check_response(test['text'])

        print(f"  Result: {'✅ APPROVED' if check.approved else '❌ BLOCKED'}")

        if not check.approved:
            print(f"  Violations: {[v.value for v in check.violations]}")
            print(f"  Severity: {check.severity}")
            print(f"  Suggested: \"{check.suggested_replacement}\"")

        # Verify expectation
        if check.approved == test['should_pass']:
            print("  ✓ Test passed")
        else:
            print("  ✗ Test FAILED")

    # Statistics
    print("\n" + "="*70)
    print("POLICY ENGINE STATISTICS")
    print("="*70)
    stats = policy.get_statistics()
    for key, value in stats.items():
        print(f"  {key}: {value}")

    print("\n✅ Policy Engine test complete")
    print("🛡️  Cardinal rules enforcement active")
    print("💜 Protecting survivors through language safety")


# ==============================================================================
# © 2025 Everett Nathaniel Christman
# The Christman AI Project — Luma Cognify AI
# All rights reserved. Unauthorized use, replication, or derivative training
# of this material is prohibited.
#
# Core Directive: "How can we help you love yourself more?"
# Autonomy & Alignment Protocol v3.0
# ==============================================================================
