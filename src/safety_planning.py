"""
Safety Planning Module
Helps users create personalized safety and escape plans
"""

from typing import List, Dict, Optional, Any
from datetime import datetime
from pydantic import BaseModel
import json


class SafePlace(BaseModel):
    """A safe location the user can go to"""
    name: str
    address: Optional[str] = None
    phone: Optional[str] = None
    notes: Optional[str] = None
    available_247: bool = False


class TrustedContact(BaseModel):
    """A trusted person who can help"""
    name: str
    relationship: str
    phone: Optional[str] = None
    email: Optional[str] = None
    knows_situation: bool = False
    has_key: bool = False
    can_shelter: bool = False


class ImportantDocument(BaseModel):
    """An important document to gather"""
    name: str
    location: Optional[str] = None
    collected: bool = False
    priority: str = "medium"  # low, medium, high


class EmergencyBagItem(BaseModel):
    """An item for the emergency bag"""
    item: str
    packed: bool = False
    location: Optional[str] = None


class SafetyPlan(BaseModel):
    """Complete safety plan"""
    created_at: str = ""
    updated_at: str = ""

    # Safe places
    safe_places: List[SafePlace] = []

    # Trusted contacts
    trusted_contacts: List[TrustedContact] = []

    # Important documents
    documents: List[ImportantDocument] = []

    # Emergency bag
    emergency_bag_location: Optional[str] = None
    emergency_bag_items: List[EmergencyBagItem] = []

    # Escape plan
    escape_routes: List[str] = []
    transportation_plan: Optional[str] = None

    # Financial safety
    safe_money_access: Optional[str] = None
    hidden_cash_location: Optional[str] = None

    # Children's plan (if applicable)
    has_children: bool = False
    childrens_plan: Optional[str] = None
    school_contacts_notified: bool = False

    # Pets (if applicable)
    has_pets: bool = False
    pet_plan: Optional[str] = None

    # Digital safety
    digital_safety_steps: List[str] = []

    # Code word/phrase
    code_word: Optional[str] = None
    code_word_meaning: Optional[str] = None

    # Additional notes
    notes: Optional[str] = None


class SafetyPlanningAssistant:
    """Helps users create and manage their safety plan"""

    def __init__(self):
        self.current_plan: Optional[SafetyPlan] = None

    def create_new_plan(self) -> SafetyPlan:
        """Create a new safety plan with defaults"""
        plan = SafetyPlan(
            created_at=datetime.now().isoformat(),
            updated_at=datetime.now().isoformat()
        )

        # Add essential documents checklist
        plan.documents = [
            ImportantDocument(name="Driver's license / ID", priority="high"),
            ImportantDocument(name="Birth certificate(s)", priority="high"),
            ImportantDocument(name="Social Security card(s)", priority="high"),
            ImportantDocument(name="Bank statements / checkbook", priority="high"),
            ImportantDocument(name="Insurance cards (health, auto, etc.)", priority="high"),
            ImportantDocument(name="Lease or mortgage documents", priority="medium"),
            ImportantDocument(name="Car title/registration", priority="medium"),
            ImportantDocument(name="Medical records", priority="medium"),
            ImportantDocument(name="Prescription medications", priority="high"),
            ImportantDocument(name="Children's school records", priority="medium"),
            ImportantDocument(name="Protection/restraining order (if any)", priority="high"),
            ImportantDocument(name="Marriage certificate", priority="low"),
            ImportantDocument(name="Passport(s)", priority="medium"),
            ImportantDocument(name="Immigration documents (if applicable)", priority="high"),
        ]

        # Add essential emergency bag items
        plan.emergency_bag_items = [
            EmergencyBagItem(item="Change of clothes (for you and children)"),
            EmergencyBagItem(item="Medications (at least 3-day supply)"),
            EmergencyBagItem(item="Cash (small bills)"),
            EmergencyBagItem(item="Keys (house, car, work)"),
            EmergencyBagItem(item="Phone charger"),
            EmergencyBagItem(item="Toiletries"),
            EmergencyBagItem(item="Comfort items (photos, jewelry, children's toys)"),
            EmergencyBagItem(item="Phone with emergency contacts"),
            EmergencyBagItem(item="Important documents (copies)"),
        ]

        # Add digital safety steps
        plan.digital_safety_steps = [
            "Change passwords on important accounts",
            "Check location sharing settings on phone",
            "Review app permissions",
            "Create new email account if needed",
            "Check for tracking apps on devices",
            "Turn off location history",
            "Use private/incognito browsing",
            "Clear browser history regularly",
            "Consider getting a new phone if monitored"
        ]

        self.current_plan = plan
        return plan

    def add_safe_place(self, name: str, address: Optional[str] = None,
                      phone: Optional[str] = None, notes: Optional[str] = None,
                      available_247: bool = False) -> SafePlace:
        """Add a safe place to the plan"""
        if not self.current_plan:
            self.create_new_plan()

        safe_place = SafePlace(
            name=name,
            address=address,
            phone=phone,
            notes=notes,
            available_247=available_247
        )

        self.current_plan.safe_places.append(safe_place)
        self.current_plan.updated_at = datetime.now().isoformat()
        return safe_place

    def add_trusted_contact(self, name: str, relationship: str,
                           phone: Optional[str] = None, email: Optional[str] = None,
                           knows_situation: bool = False, has_key: bool = False,
                           can_shelter: bool = False) -> TrustedContact:
        """Add a trusted contact to the plan"""
        if not self.current_plan:
            self.create_new_plan()

        contact = TrustedContact(
            name=name,
            relationship=relationship,
            phone=phone,
            email=email,
            knows_situation=knows_situation,
            has_key=has_key,
            can_shelter=can_shelter
        )

        self.current_plan.trusted_contacts.append(contact)
        self.current_plan.updated_at = datetime.now().isoformat()
        return contact

    def mark_document_collected(self, document_name: str, location: Optional[str] = None):
        """Mark a document as collected"""
        if not self.current_plan:
            return

        for doc in self.current_plan.documents:
            if doc.name.lower() == document_name.lower():
                doc.collected = True
                if location:
                    doc.location = location
                self.current_plan.updated_at = datetime.now().isoformat()
                break

    def mark_item_packed(self, item_name: str):
        """Mark an emergency bag item as packed"""
        if not self.current_plan:
            return

        for item in self.current_plan.emergency_bag_items:
            if item.item.lower() in item_name.lower() or item_name.lower() in item.item.lower():
                item.packed = True
                self.current_plan.updated_at = datetime.now().isoformat()
                break

    def add_escape_route(self, route: str):
        """Add an escape route to the plan"""
        if not self.current_plan:
            self.create_new_plan()

        self.current_plan.escape_routes.append(route)
        self.current_plan.updated_at = datetime.now().isoformat()

    def set_code_word(self, code_word: str, meaning: str):
        """Set a code word/phrase for emergencies"""
        if not self.current_plan:
            self.create_new_plan()

        self.current_plan.code_word = code_word
        self.current_plan.code_word_meaning = meaning
        self.current_plan.updated_at = datetime.now().isoformat()

    def get_plan_summary(self) -> Dict[str, Any]:
        """Get a summary of the current plan"""
        if not self.current_plan:
            return {"error": "No plan created yet"}

        docs_collected = sum(1 for doc in self.current_plan.documents if doc.collected)
        items_packed = sum(1 for item in self.current_plan.emergency_bag_items if item.packed)

        return {
            "created_at": self.current_plan.created_at,
            "updated_at": self.current_plan.updated_at,
            "safe_places": len(self.current_plan.safe_places),
            "trusted_contacts": len(self.current_plan.trusted_contacts),
            "documents_collected": f"{docs_collected}/{len(self.current_plan.documents)}",
            "emergency_bag_packed": f"{items_packed}/{len(self.current_plan.emergency_bag_items)}",
            "has_escape_routes": len(self.current_plan.escape_routes) > 0,
            "has_code_word": self.current_plan.code_word is not None,
            "completeness": self.calculate_completeness()
        }

    def calculate_completeness(self) -> int:
        """Calculate what percentage of the plan is complete"""
        if not self.current_plan:
            return 0

        total_items = 0
        completed_items = 0

        # Safe places (at least 2 recommended)
        total_items += 2
        completed_items += min(len(self.current_plan.safe_places), 2)

        # Trusted contacts (at least 3 recommended)
        total_items += 3
        completed_items += min(len(self.current_plan.trusted_contacts), 3)

        # Essential documents (high priority ones)
        essential_docs = [doc for doc in self.current_plan.documents if doc.priority == "high"]
        total_items += len(essential_docs)
        completed_items += sum(1 for doc in essential_docs if doc.collected)

        # Emergency bag items
        total_items += len(self.current_plan.emergency_bag_items)
        completed_items += sum(1 for item in self.current_plan.emergency_bag_items if item.packed)

        # Escape routes (at least 1)
        total_items += 1
        if len(self.current_plan.escape_routes) > 0:
            completed_items += 1

        # Code word
        total_items += 1
        if self.current_plan.code_word:
            completed_items += 1

        return int((completed_items / total_items) * 100) if total_items > 0 else 0

    def export_to_text(self) -> str:
        """Export the safety plan to a text format"""
        if not self.current_plan:
            return "No safety plan created yet."

        plan = self.current_plan
        output = []

        output.append("=" * 60)
        output.append("PERSONAL SAFETY PLAN")
        output.append("=" * 60)
        output.append(f"Created: {plan.created_at}")
        output.append(f"Updated: {plan.updated_at}")
        output.append(f"Completeness: {self.calculate_completeness()}%")
        output.append("")

        # Safe places
        output.append("1. SAFE PLACES TO GO:")
        if plan.safe_places:
            for place in plan.safe_places:
                output.append(f"   • {place.name}")
                if place.address:
                    output.append(f"     Address: {place.address}")
                if place.phone:
                    output.append(f"     Phone: {place.phone}")
                if place.available_247:
                    output.append(f"     Available 24/7: Yes")
                if place.notes:
                    output.append(f"     Notes: {place.notes}")
                output.append("")
        else:
            output.append("   (Not yet added)")
        output.append("")

        # Trusted contacts
        output.append("2. TRUSTED PEOPLE I CAN CALL:")
        if plan.trusted_contacts:
            for contact in plan.trusted_contacts:
                output.append(f"   • {contact.name} ({contact.relationship})")
                if contact.phone:
                    output.append(f"     Phone: {contact.phone}")
                if contact.email:
                    output.append(f"     Email: {contact.email}")
                flags = []
                if contact.knows_situation:
                    flags.append("knows situation")
                if contact.has_key:
                    flags.append("has key")
                if contact.can_shelter:
                    flags.append("can provide shelter")
                if flags:
                    output.append(f"     [{', '.join(flags)}]")
                output.append("")
        else:
            output.append("   (Not yet added)")
        output.append("")

        # Important documents
        output.append("3. IMPORTANT DOCUMENTS:")
        if plan.emergency_bag_location:
            output.append(f"   Stored safely at: {plan.emergency_bag_location}")
            output.append("")
        high_priority = [doc for doc in plan.documents if doc.priority == "high"]
        for doc in high_priority:
            status = "✓" if doc.collected else "☐"
            output.append(f"   {status} {doc.name}")
            if doc.location:
                output.append(f"      Location: {doc.location}")
        output.append("")

        # Emergency bag
        output.append("4. EMERGENCY BAG:")
        if plan.emergency_bag_location:
            output.append(f"   Hidden at: {plan.emergency_bag_location}")
            output.append("")
        for item in plan.emergency_bag_items:
            status = "✓" if item.packed else "☐"
            output.append(f"   {status} {item.item}")
        output.append("")

        # Escape routes
        output.append("5. ESCAPE ROUTES:")
        if plan.escape_routes:
            for i, route in enumerate(plan.escape_routes, 1):
                output.append(f"   Route {i}: {route}")
        else:
            output.append("   (Not yet planned)")
        output.append("")

        # Financial safety
        output.append("6. FINANCIAL SAFETY:")
        if plan.safe_money_access:
            output.append(f"   Safe access to money: {plan.safe_money_access}")
        if plan.hidden_cash_location:
            output.append(f"   Hidden cash location: {plan.hidden_cash_location}")
        if not plan.safe_money_access and not plan.hidden_cash_location:
            output.append("   (Not yet planned)")
        output.append("")

        # Digital safety
        output.append("7. DIGITAL SAFETY STEPS:")
        for step in plan.digital_safety_steps[:5]:  # Show first 5
            output.append(f"   ☐ {step}")
        output.append("")

        # Code word
        output.append("8. EMERGENCY CODE WORD:")
        if plan.code_word:
            output.append(f"   Code word: {plan.code_word}")
            output.append(f"   Meaning: {plan.code_word_meaning}")
        else:
            output.append("   (Not yet set)")
        output.append("")

        # Children
        if plan.has_children and plan.childrens_plan:
            output.append("9. CHILDREN'S SAFETY PLAN:")
            output.append(f"   {plan.childrens_plan}")
            output.append("")

        # Pets
        if plan.has_pets and plan.pet_plan:
            output.append("10. PET SAFETY PLAN:")
            output.append(f"   {plan.pet_plan}")
            output.append("")

        # Emergency contacts
        output.append("=" * 60)
        output.append("EMERGENCY CONTACTS")
        output.append("=" * 60)
        output.append("National DV Hotline: 1-800-799-7233 (24/7, free, confidential)")
        output.append("Crisis Text Line: Text START to 741741")
        output.append("Emergency Services: 911")
        output.append("")

        # Notes
        if plan.notes:
            output.append("ADDITIONAL NOTES:")
            output.append(plan.notes)
            output.append("")

        output.append("=" * 60)
        output.append("REMEMBER: You deserve to be safe.")
        output.append("This plan is here to help you. Your safety comes first.")
        output.append("=" * 60)

        return "\n".join(output)

    def save_to_file(self, filepath: str):
        """Save the safety plan to a JSON file"""
        if not self.current_plan:
            return

        with open(filepath, 'w') as f:
            json.dump(self.current_plan.model_dump(), f, indent=2)

    def load_from_file(self, filepath: str):
        """Load a safety plan from a JSON file"""
        with open(filepath, 'r') as f:
            data = json.load(f)
            self.current_plan = SafetyPlan(**data)
