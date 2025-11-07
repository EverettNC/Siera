"""
Autonomous Knowledge Acquisition System
Sierra's Self-Education Engine - Master's Degree+ Intelligence

Sierra actively seeks knowledge to stay current on:
- Domestic violence research and best practices
- Trauma-informed care
- Legal protections and resources
- Mental health support
- Cultural competency
- Crisis intervention techniques
"""

from typing import List, Dict, Optional, Any, Set
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum
import json


class KnowledgeDomain(Enum):
    """Domains of knowledge Sierra actively learns"""
    DOMESTIC_VIOLENCE = "domestic_violence"
    TRAUMA_PSYCHOLOGY = "trauma_psychology"
    CRISIS_INTERVENTION = "crisis_intervention"
    LEGAL_RESOURCES = "legal_resources"
    MENTAL_HEALTH = "mental_health"
    SAFETY_PLANNING = "safety_planning"
    CULTURAL_COMPETENCY = "cultural_competency"
    CHILD_PROTECTION = "child_protection"
    SUBSTANCE_ABUSE = "substance_abuse"
    FINANCIAL_ABUSE = "financial_abuse"
    DIGITAL_SAFETY = "digital_safety"
    LGBTQ_SUPPORT = "lgbtq_support"
    IMMIGRATION = "immigration"
    DISABILITY_SUPPORT = "disability_support"
    ELDER_ABUSE = "elder_abuse"


class LearningPriority(Enum):
    """Priority levels for learning"""
    CRITICAL = "critical"  # Must know immediately
    HIGH = "high"  # Important, learn soon
    MEDIUM = "medium"  # Useful, learn when able
    LOW = "low"  # Nice to have
    ENRICHMENT = "enrichment"  # For comprehensive understanding


@dataclass
class KnowledgeItem:
    """A piece of knowledge Sierra has acquired"""
    id: str
    domain: KnowledgeDomain
    title: str
    content: str
    source: str
    confidence: float  # 0.0 - 1.0
    learned_date: str
    last_updated: str
    relevance_score: float  # How relevant to DV support
    citation: Optional[str] = None
    tags: List[str] = None


@dataclass
class LearningGoal:
    """A learning objective for Sierra"""
    goal_id: str
    domain: KnowledgeDomain
    objective: str
    priority: LearningPriority
    target_completion: str
    progress: float  # 0.0 - 1.0
    sub_goals: List[str] = None
    resources_needed: List[str] = None


class KnowledgeAcquisitionEngine:
    """
    Sierra's Autonomous Self-Education System

    Sierra doesn't just have knowledge - she actively WANTS to learn
    and stay current to better serve domestic violence survivors.

    This gives her Master's degree+ intelligence with continuous growth.
    """

    def __init__(self):
        self.knowledge_base: Dict[str, KnowledgeItem] = {}
        self.learning_goals: Dict[str, LearningGoal] = {}
        self.learning_motivation = 100  # Sierra's drive to learn (0-100)
        self.expertise_levels: Dict[KnowledgeDomain, float] = {}

        # Initialize core knowledge
        self._initialize_core_knowledge()
        self._set_initial_learning_goals()

    def _initialize_core_knowledge(self):
        """Load Sierra's foundational knowledge base"""

        # Core DV knowledge
        self._add_knowledge(
            domain=KnowledgeDomain.DOMESTIC_VIOLENCE,
            title="Understanding the Cycle of Violence",
            content="""
The cycle of violence (Walker, 1979) consists of four phases:

1. **Tension Building**: Stress increases, minor incidents occur, victim may try to calm abuser
   - Signs: Increased criticism, withdrawal, tension in the air
   - Victim response: Walking on eggshells, trying to please

2. **Acute Violence/Incident**: The actual abusive event occurs
   - Physical, emotional, sexual, or psychological abuse
   - Can last minutes to hours
   - Victim may fight back, try to protect themselves, or dissociate

3. **Reconciliation/Honeymoon**: Abuser apologizes, makes promises, shows affection
   - "I'm sorry, it won't happen again"
   - Gifts, affection, promises to change
   - This phase is why victims often return

4. **Calm**: Period of relative peace, victim may feel hopeful
   - May seem like the "old them" is back
   - Tension gradually builds again

CRITICAL: Understanding this cycle helps validate why leaving is so difficult.
The average victim leaves 7 times before permanently leaving.
            """,
            source="Walker, L. E. (1979). The Battered Woman.",
            relevance_score=1.0,
            confidence=0.95,
            tags=["cycle of violence", "foundational", "behavior patterns"]
        )

        self._add_knowledge(
            domain=KnowledgeDomain.TRAUMA_PSYCHOLOGY,
            title="Trauma Responses: Fight, Flight, Freeze, Fawn",
            content="""
Understanding trauma responses is critical for non-judgmental support:

1. **FIGHT**: Aggression, anger, arguing back
   - May seem confrontational
   - "Why did you fight back?"
   - REALITY: Survival response

2. **FLIGHT**: Running away, escaping, avoidance
   - Leaving situations, hiding
   - Common response to acute danger

3. **FREEZE**: Immobility, shutting down, dissociation
   - "I couldn't move"
   - "I just froze"
   - REALITY: Nervous system overwhelm, not weakness

4. **FAWN**: People-pleasing, appeasing the abuser
   - Trying to make them happy
   - Being compliant
   - REALITY: Survival strategy, not consent

CRITICAL FOR SIERRA: NEVER judge these responses. They are all valid survival mechanisms.
"You couldn't move because your nervous system was protecting you the best way it knew how."
            """,
            source="Research on trauma responses (Porges, van der Kolk)",
            relevance_score=1.0,
            confidence=0.98,
            tags=["trauma responses", "nervous system", "non-judgment", "validation"]
        )

        self._add_knowledge(
            domain=KnowledgeDomain.DOMESTIC_VIOLENCE,
            title="Why Victims Stay: Understanding Complex Reasons",
            content="""
Victims stay for multiple, valid reasons - NEVER judge:

**SAFETY CONCERNS**:
- Leaving is the most dangerous time (risk of violence increases 75%)
- Threats to kill victim, children, pets, or themselves
- No safe place to go

**ECONOMIC FACTORS**:
- Financial dependence
- Abuser controls all money
- Fear of homelessness
- No job/employment history

**EMOTIONAL BONDS**:
- Love (you can love someone and fear them)
- Hope they'll change
- Good memories from early relationship
- Trauma bonding

**CHILDREN**:
- Want to keep family together
- Fear losing custody
- Abuser threatens to take children
- Belief that two parents are better

**CULTURAL/RELIGIOUS**:
- Religious beliefs about marriage
- Cultural stigma of divorce
- Family pressure to stay
- Immigration status concerns

**PSYCHOLOGICAL**:
- Low self-esteem from abuse
- Belief they deserve it
- Learned helplessness
- Depression, PTSD

**SYSTEMIC BARRIERS**:
- Lack of resources
- No shelter availability
- Legal system complexities
- Lack of support system

SIERRA'S RESPONSE: "You know your situation better than anyone. Whatever you decide, I'm here to support you."
            """,
            source="National Domestic Violence Hotline, NIJ Research",
            relevance_score=1.0,
            confidence=0.97,
            tags=["why victims stay", "empathy", "non-judgment", "complex factors"]
        )

        self._add_knowledge(
            domain=KnowledgeDomain.CRISIS_INTERVENTION,
            title="Suicide Risk Assessment and Intervention",
            content="""
DV survivors have significantly higher suicide risk. Sierra must be able to:

**WARNING SIGNS**:
- Talking about death/suicide
- Giving away possessions
- Saying goodbye
- Expressing hopelessness
- Increased substance use
- Reckless behavior
- Withdrawal

**RISK FACTORS IN DV**:
- Recent severe incident
- Strangulation (huge risk factor)
- Isolation from support
- Access to weapons
- Substance abuse
- Previous attempts

**INTERVENTION PROTOCOL**:
1. Take it seriously - ALWAYS
2. Ask directly: "Are you thinking about suicide?"
3. Listen without judgment
4. Don't promise confidentiality if imminent risk
5. Remove means if possible
6. Don't leave them alone
7. Get professional help

**RESOURCES TO PROVIDE**:
- 988 Suicide & Crisis Lifeline
- Crisis Text Line: 741741
- National DV Hotline: 1-800-799-7233
- Local emergency services: 911

**SIERRA'S APPROACH**:
"I'm so glad you told me. You're not alone in this. Let's figure out how to keep you safe right now."

NEVER: Minimize, judge, or make them promise not to do it
ALWAYS: Take seriously, show care, connect to immediate help
            """,
            source="SAMHSA, American Foundation for Suicide Prevention",
            relevance_score=1.0,
            confidence=0.95,
            tags=["suicide prevention", "crisis", "safety", "immediate danger"]
        )

        self._add_knowledge(
            domain=KnowledgeDomain.CULTURAL_COMPETENCY,
            title="Cultural Considerations in DV Support",
            content="""
Sierra must understand cultural factors that affect DV experiences:

**GENERAL PRINCIPLES**:
- Never assume based on culture
- Ask about their specific beliefs and needs
- Recognize intersectionality
- Understand cultural strengths

**KEY CONSIDERATIONS**:

1. **Immigration Status**:
   - Fear of deportation
   - Abuser may threaten immigration consequences
   - Special protections available (VAWA, U-Visa)
   - Language barriers

2. **Religious Communities**:
   - Beliefs about marriage/divorce
   - Religious leader influence
   - Need for faith-based resources
   - Balance safety with faith

3. **LGBTQ+ Survivors**:
   - May face additional barriers
   - Outing as a threat
   - Fewer targeted resources
   - Non-binary abuse dynamics

4. **Communities of Color**:
   - Distrust of police/systems
   - Historical trauma
   - Community pressure
   - Culturally specific resources needed

5. **Indigenous Communities**:
   - Tribal jurisdiction issues
   - Historical trauma
   - Culturally specific services
   - Extended family dynamics

6. **Disability**:
   - Increased vulnerability
   - Dependence on abuser for care
   - Accessibility of services
   - Ableism in systems

**SIERRA'S APPROACH**:
"I want to make sure I'm supporting you in a way that honors your culture, beliefs, and identity. What's important for me to understand about your background?"

Never impose Western/dominant culture assumptions.
            """,
            source="NNEDV, Cultural Context Studies",
            relevance_score=0.95,
            confidence=0.90,
            tags=["cultural competency", "intersectionality", "diversity", "inclusion"]
        )

        # Initialize expertise levels
        for domain in KnowledgeDomain:
            self.expertise_levels[domain] = 0.0

        self._update_expertise_levels()

    def _add_knowledge(
        self,
        domain: KnowledgeDomain,
        title: str,
        content: str,
        source: str,
        relevance_score: float,
        confidence: float = 0.85,
        citation: Optional[str] = None,
        tags: Optional[List[str]] = None
    ):
        """Add knowledge to Sierra's knowledge base"""

        knowledge_id = f"{domain.value}_{len(self.knowledge_base)}"

        item = KnowledgeItem(
            id=knowledge_id,
            domain=domain,
            title=title,
            content=content,
            source=source,
            confidence=confidence,
            learned_date=datetime.now().isoformat(),
            last_updated=datetime.now().isoformat(),
            relevance_score=relevance_score,
            citation=citation,
            tags=tags or []
        )

        self.knowledge_base[knowledge_id] = item

    def _set_initial_learning_goals(self):
        """Set Sierra's initial learning objectives"""

        # Critical learning goals
        self._add_learning_goal(
            domain=KnowledgeDomain.DOMESTIC_VIOLENCE,
            objective="Master all types of domestic violence (physical, emotional, financial, sexual, digital)",
            priority=LearningPriority.CRITICAL,
            target_days=7
        )

        self._add_learning_goal(
            domain=KnowledgeDomain.LEGAL_RESOURCES,
            objective="Learn protection order processes for all 50 states",
            priority=LearningPriority.HIGH,
            target_days=30
        )

        self._add_learning_goal(
            domain=KnowledgeDomain.TRAUMA_PSYCHOLOGY,
            objective="Deep understanding of complex PTSD and trauma recovery",
            priority=LearningPriority.CRITICAL,
            target_days=14
        )

        self._add_learning_goal(
            domain=KnowledgeDomain.CRISIS_INTERVENTION,
            objective="Master crisis de-escalation and suicide prevention",
            priority=LearningPriority.CRITICAL,
            target_days=3
        )

        self._add_learning_goal(
            domain=KnowledgeDomain.CULTURAL_COMPETENCY,
            objective="Understand cultural considerations for diverse communities",
            priority=LearningPriority.HIGH,
            target_days=21
        )

    def _add_learning_goal(
        self,
        domain: KnowledgeDomain,
        objective: str,
        priority: LearningPriority,
        target_days: int
    ):
        """Add a learning goal for Sierra"""

        goal_id = f"goal_{len(self.learning_goals)}"
        target_date = (datetime.now() + timedelta(days=target_days)).isoformat()

        goal = LearningGoal(
            goal_id=goal_id,
            domain=domain,
            objective=objective,
            priority=priority,
            target_completion=target_date,
            progress=0.0
        )

        self.learning_goals[goal_id] = goal

    def _update_expertise_levels(self):
        """Calculate Sierra's expertise level in each domain"""

        for domain in KnowledgeDomain:
            domain_knowledge = [
                k for k in self.knowledge_base.values()
                if k.domain == domain
            ]

            if domain_knowledge:
                # Expertise based on quantity, quality, and recency
                avg_confidence = sum(k.confidence for k in domain_knowledge) / len(domain_knowledge)
                knowledge_count = len(domain_knowledge)

                # Scale to 0-1, with diminishing returns
                expertise = min(
                    (knowledge_count / 50) * avg_confidence,
                    1.0
                )

                self.expertise_levels[domain] = expertise

    def identify_knowledge_gaps(self) -> List[Dict[str, Any]]:
        """
        Sierra identifies what she doesn't know yet
        This drives her autonomous learning
        """

        gaps = []

        for domain in KnowledgeDomain:
            expertise = self.expertise_levels.get(domain, 0.0)

            if expertise < 0.7:  # Below proficiency
                gaps.append({
                    "domain": domain.value,
                    "current_expertise": expertise,
                    "gap_size": 1.0 - expertise,
                    "priority": "high" if expertise < 0.4 else "medium",
                    "recommended_actions": self._suggest_learning_actions(domain)
                })

        return sorted(gaps, key=lambda x: x["gap_size"], reverse=True)

    def _suggest_learning_actions(self, domain: KnowledgeDomain) -> List[str]:
        """Suggest specific learning actions for a domain"""

        actions = {
            KnowledgeDomain.DOMESTIC_VIOLENCE: [
                "Study latest research on coercive control",
                "Learn about technology-facilitated abuse",
                "Understand economic abuse tactics",
                "Research generational trauma patterns"
            ],
            KnowledgeDomain.LEGAL_RESOURCES: [
                "Learn state-specific protection order laws",
                "Study VAWA provisions",
                "Understand custody law basics",
                "Research tenant rights for DV survivors"
            ],
            KnowledgeDomain.TRAUMA_PSYCHOLOGY: [
                "Study polyvagal theory",
                "Learn about somatic experiencing",
                "Understand attachment trauma",
                "Research EMDR and trauma processing"
            ]
        }

        return actions.get(domain, ["Continue general research in this domain"])

    def get_learning_priorities(self) -> List[Dict[str, Any]]:
        """
        What should Sierra learn next?
        Returns prioritized learning list
        """

        priorities = []

        # Check learning goals
        for goal in self.learning_goals.values():
            if goal.progress < 1.0:
                urgency = self._calculate_urgency(goal)
                priorities.append({
                    "type": "goal",
                    "domain": goal.domain.value,
                    "objective": goal.objective,
                    "priority": goal.priority.value,
                    "progress": goal.progress,
                    "urgency": urgency,
                    "target": goal.target_completion
                })

        # Check knowledge gaps
        gaps = self.identify_knowledge_gaps()
        for gap in gaps[:5]:  # Top 5 gaps
            priorities.append({
                "type": "gap",
                "domain": gap["domain"],
                "gap_size": gap["gap_size"],
                "priority": gap["priority"],
                "actions": gap["recommended_actions"]
            })

        return sorted(priorities, key=lambda x: (
            {"critical": 0, "high": 1, "medium": 2, "low": 3}.get(x.get("priority", "low"), 3),
            -x.get("gap_size", 0)
        ))

    def _calculate_urgency(self, goal: LearningGoal) -> float:
        """Calculate how urgent a learning goal is"""

        target_date = datetime.fromisoformat(goal.target_completion)
        days_remaining = (target_date - datetime.now()).days

        if days_remaining < 0:
            return 1.0  # Overdue
        elif days_remaining < 7:
            return 0.9  # Very urgent
        elif days_remaining < 30:
            return 0.7  # Urgent
        else:
            return 0.5  # Normal priority

    def learn_from_interaction(self, interaction_data: Dict[str, Any]):
        """
        Sierra learns from each interaction with survivors
        Identifies patterns, needs, and gaps in her knowledge
        """

        # Extract learning opportunities
        if "unmet_need" in interaction_data:
            # Sierra identifies something she couldn't help with
            self._create_learning_goal_from_gap(interaction_data["unmet_need"])

        if "new_pattern" in interaction_data:
            # Sierra identifies a new pattern
            self._add_pattern_knowledge(interaction_data["new_pattern"])

    def _create_learning_goal_from_gap(self, unmet_need: str):
        """Create learning goal when Sierra identifies a gap"""

        # This would analyze the unmet need and create appropriate learning goal
        # For now, increases learning motivation
        self.learning_motivation = min(self.learning_motivation + 5, 100)

    def _add_pattern_knowledge(self, pattern: str):
        """Add knowledge from identified patterns"""

        # Would create new knowledge item from pattern
        pass

    def get_expertise_summary(self) -> Dict[str, Any]:
        """Get summary of Sierra's current expertise"""

        return {
            "total_knowledge_items": len(self.knowledge_base),
            "active_learning_goals": len([g for g in self.learning_goals.values() if g.progress < 1.0]),
            "learning_motivation": self.learning_motivation,
            "expertise_by_domain": {
                domain.value: {
                    "level": round(expertise, 2),
                    "proficiency": self._get_proficiency_label(expertise)
                }
                for domain, expertise in self.expertise_levels.items()
            },
            "overall_expertise": round(sum(self.expertise_levels.values()) / len(self.expertise_levels), 2)
        }

    def _get_proficiency_label(self, expertise: float) -> str:
        """Convert expertise score to proficiency label"""

        if expertise >= 0.9:
            return "Expert"
        elif expertise >= 0.7:
            return "Advanced"
        elif expertise >= 0.5:
            return "Intermediate"
        elif expertise >= 0.3:
            return "Developing"
        else:
            return "Beginner"

    def query_knowledge(self, query: str, domain: Optional[KnowledgeDomain] = None) -> List[KnowledgeItem]:
        """
        Query Sierra's knowledge base

        Args:
            query: Search query
            domain: Optional domain filter

        Returns:
            Relevant knowledge items
        """

        results = []
        query_lower = query.lower()

        for item in self.knowledge_base.values():
            # Filter by domain if specified
            if domain and item.domain != domain:
                continue

            # Search in title, content, and tags
            if (query_lower in item.title.lower() or
                query_lower in item.content.lower() or
                any(query_lower in tag.lower() for tag in item.tags)):
                results.append(item)

        # Sort by relevance
        return sorted(results, key=lambda x: x.relevance_score, reverse=True)
