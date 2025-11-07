"""
Resource Database
Comprehensive resources for domestic violence survivors
"""

from typing import List, Dict, Optional
from pydantic import BaseModel
from enum import Enum


class ResourceType(Enum):
    """Types of resources available"""
    HOTLINE = "hotline"
    SHELTER = "shelter"
    LEGAL = "legal"
    COUNSELING = "counseling"
    FINANCIAL = "financial"
    MEDICAL = "medical"
    ADVOCACY = "advocacy"
    SUPPORT_GROUP = "support_group"
    HOUSING = "housing"
    CHILDREN = "children"
    PETS = "pets"
    EMPLOYMENT = "employment"
    IMMIGRATION = "immigration"


class Resource(BaseModel):
    """A single resource"""
    name: str
    resource_type: ResourceType
    description: str
    phone: Optional[str] = None
    text: Optional[str] = None
    website: Optional[str] = None
    email: Optional[str] = None
    hours: str = "Call for hours"
    available_247: bool = False
    confidential: bool = True
    free: bool = True
    languages: List[str] = ["English"]
    national: bool = False
    state: Optional[str] = None
    city: Optional[str] = None
    services: List[str] = []
    notes: Optional[str] = None


class ResourceDatabase:
    """Database of resources for domestic violence survivors"""

    def __init__(self):
        self.resources: List[Resource] = []
        self._load_default_resources()

    def _load_default_resources(self):
        """Load default national resources"""

        # National Hotlines
        self.resources.append(Resource(
            name="National Domestic Violence Hotline",
            resource_type=ResourceType.HOTLINE,
            description="24/7 confidential support, crisis intervention, and referrals",
            phone="1-800-799-7233",
            text="Text START to 22522",
            website="https://www.thehotline.org",
            hours="24/7",
            available_247=True,
            national=True,
            languages=["English", "Spanish", "200+ languages via interpreter"],
            services=[
                "Crisis intervention",
                "Safety planning",
                "Referrals to local services",
                "Emotional support",
                "Information about domestic violence"
            ],
            notes="Available via phone, text, and online chat. Completely confidential."
        ))

        self.resources.append(Resource(
            name="Crisis Text Line",
            resource_type=ResourceType.HOTLINE,
            description="24/7 crisis support via text message",
            text="Text START to 741741",
            website="https://www.crisistextline.org",
            hours="24/7",
            available_247=True,
            national=True,
            languages=["English", "Spanish"],
            services=[
                "Crisis counseling via text",
                "Emotional support",
                "De-escalation",
                "Resource connection"
            ],
            notes="Free, confidential support via text message"
        ))

        self.resources.append(Resource(
            name="RAINN (Rape, Abuse & Incest National Network)",
            resource_type=ResourceType.HOTLINE,
            description="Sexual assault hotline and support",
            phone="1-800-656-4673",
            website="https://www.rainn.org",
            hours="24/7",
            available_247=True,
            national=True,
            services=[
                "Sexual assault support",
                "Crisis counseling",
                "Local referrals",
                "Information about sexual violence"
            ]
        ))

        self.resources.append(Resource(
            name="National Teen Dating Abuse Helpline",
            resource_type=ResourceType.HOTLINE,
            description="Support for teens experiencing dating abuse",
            phone="1-866-331-9474",
            text="Text LOVEIS to 22522",
            website="https://www.loveisrespect.org",
            hours="24/7",
            available_247=True,
            national=True,
            services=[
                "Support for teens and young adults",
                "Dating abuse resources",
                "Healthy relationship information"
            ]
        ))

        self.resources.append(Resource(
            name="National Suicide Prevention Lifeline",
            resource_type=ResourceType.HOTLINE,
            description="24/7 suicide prevention and crisis support",
            phone="988",
            website="https://988lifeline.org",
            hours="24/7",
            available_247=True,
            national=True,
            services=[
                "Suicide prevention",
                "Crisis counseling",
                "Emotional support"
            ]
        ))

        # Legal Resources
        self.resources.append(Resource(
            name="Legal Services Corporation",
            resource_type=ResourceType.LEGAL,
            description="Free legal aid for low-income individuals",
            website="https://www.lsc.gov/find-legal-aid",
            national=True,
            services=[
                "Free legal assistance",
                "Protection order help",
                "Family law",
                "Housing issues"
            ],
            notes="Find free legal aid in your area through their website"
        ))

        self.resources.append(Resource(
            name="WomensLaw.org",
            resource_type=ResourceType.LEGAL,
            description="Legal information for domestic violence survivors",
            website="https://www.womenslaw.org",
            email="info@womenslaw.org",
            national=True,
            services=[
                "Legal information by state",
                "Protection order information",
                "Custody and divorce information",
                "Email support"
            ],
            notes="Comprehensive legal information, not legal advice"
        ))

        # Immigration Resources
        self.resources.append(Resource(
            name="National Immigrant Women's Advocacy Project (NIWAP)",
            resource_type=ResourceType.IMMIGRATION,
            description="Legal help for immigrant survivors of domestic violence",
            website="https://niwaplibrary.wcl.american.edu",
            national=True,
            services=[
                "VAWA (Violence Against Women Act) information",
                "U-Visa information",
                "Legal resources for immigrants",
                "Technical assistance"
            ]
        ))

        # Financial Resources
        self.resources.append(Resource(
            name="Benefits.gov",
            resource_type=ResourceType.FINANCIAL,
            description="Find government benefits you may qualify for",
            website="https://www.benefits.gov",
            national=True,
            services=[
                "SNAP (food assistance)",
                "TANF (cash assistance)",
                "Housing assistance",
                "Healthcare assistance"
            ]
        ))

        self.resources.append(Resource(
            name="Modest Needs",
            resource_type=ResourceType.FINANCIAL,
            description="Emergency financial assistance for self-sufficiency",
            website="https://www.modestneeds.org",
            national=True,
            free=False,
            services=[
                "Emergency grants",
                "Financial assistance",
                "Bill payment help"
            ],
            notes="Application process required"
        ))

        # Children's Resources
        self.resources.append(Resource(
            name="Childhelp National Child Abuse Hotline",
            resource_type=ResourceType.CHILDREN,
            description="Support for child abuse issues",
            phone="1-800-422-4453",
            website="https://www.childhelp.org",
            hours="24/7",
            available_247=True,
            national=True,
            services=[
                "Child abuse reporting",
                "Crisis counseling",
                "Resources for children"
            ]
        ))

        # Pet Resources
        self.resources.append(Resource(
            name="Safe Havens Mapping Project",
            resource_type=ResourceType.PETS,
            description="Find shelters that accommodate pets",
            website="https://www.sheltersafe.org",
            national=True,
            services=[
                "Pet-friendly shelters",
                "Foster care for pets",
                "Resources for pet safety"
            ],
            notes="Many DV survivors stay in dangerous situations because of pets"
        ))

        self.resources.append(Resource(
            name="RedRover Relief",
            resource_type=ResourceType.PETS,
            description="Emergency pet sheltering for domestic violence survivors",
            phone="1-800-767-1511",
            website="https://redrover.org",
            national=True,
            services=[
                "Emergency pet boarding",
                "Financial assistance for pet care",
                "Safe housing for pets"
            ]
        ))

        # Employment
        self.resources.append(Resource(
            name="Dress for Success",
            resource_type=ResourceType.EMPLOYMENT,
            description="Professional clothing and career support",
            website="https://dressforsuccess.org",
            national=True,
            services=[
                "Professional clothing",
                "Career counseling",
                "Job search support",
                "Interview preparation"
            ],
            notes="Locations nationwide, helping women achieve economic independence"
        ))

        # Medical
        self.resources.append(Resource(
            name="National Health Care for the Homeless Council",
            resource_type=ResourceType.MEDICAL,
            description="Healthcare resources for those experiencing homelessness",
            website="https://nhchc.org",
            national=True,
            services=[
                "Medical care",
                "Mental health services",
                "Substance abuse treatment"
            ]
        ))

    def get_all_resources(self) -> List[Resource]:
        """Get all resources"""
        return self.resources

    def get_by_type(self, resource_type: ResourceType) -> List[Resource]:
        """Get resources by type"""
        return [r for r in self.resources if r.resource_type == resource_type]

    def get_national_resources(self) -> List[Resource]:
        """Get national resources"""
        return [r for r in self.resources if r.national]

    def get_24_7_resources(self) -> List[Resource]:
        """Get resources available 24/7"""
        return [r for r in self.resources if r.available_247]

    def get_crisis_resources(self) -> List[Resource]:
        """Get crisis/emergency resources (24/7 hotlines)"""
        return [r for r in self.resources if r.available_247 and r.resource_type == ResourceType.HOTLINE]

    def search(self, query: str) -> List[Resource]:
        """Search resources by keyword"""
        query_lower = query.lower()
        results = []

        for resource in self.resources:
            # Search in name, description, and services
            if (query_lower in resource.name.lower() or
                query_lower in resource.description.lower() or
                any(query_lower in service.lower() for service in resource.services)):
                results.append(resource)

        return results

    def add_resource(self, resource: Resource):
        """Add a custom resource"""
        self.resources.append(resource)

    def format_resource(self, resource: Resource) -> str:
        """Format a resource for display"""
        output = []
        output.append(f"**{resource.name}**")
        output.append(f"{resource.description}")
        output.append("")

        if resource.phone:
            output.append(f"📞 Phone: {resource.phone}")
        if resource.text:
            output.append(f"💬 Text: {resource.text}")
        if resource.website:
            output.append(f"🌐 Website: {resource.website}")
        if resource.email:
            output.append(f"📧 Email: {resource.email}")

        output.append(f"⏰ Hours: {resource.hours}")

        if resource.available_247:
            output.append("🕐 Available 24/7")
        if resource.confidential:
            output.append("🔒 Confidential")
        if resource.free:
            output.append("💵 Free")

        if len(resource.languages) > 1 or resource.languages[0] != "English":
            output.append(f"🌍 Languages: {', '.join(resource.languages)}")

        if resource.services:
            output.append("")
            output.append("Services:")
            for service in resource.services:
                output.append(f"  • {service}")

        if resource.notes:
            output.append("")
            output.append(f"ℹ️ Note: {resource.notes}")

        return "\n".join(output)

    def get_emergency_card(self) -> str:
        """Get a quick reference emergency card"""
        return """
🚨 EMERGENCY RESOURCES - KEEP SAFE 🚨

IMMEDIATE DANGER:
🆘 Call 911

24/7 HOTLINES:
📞 National DV Hotline: 1-800-799-7233
💬 Text START to 22522
📞 Crisis Text Line: Text START to 741741
📞 Sexual Assault Hotline: 1-800-656-4673
📞 Suicide Prevention: 988

ONLINE:
🌐 TheHotline.org (chat available)
🌐 RAINN.org (chat available)

SAFETY REMINDERS:
• Clear browser history if needed
• Use private/incognito mode
• Have a code word with trusted people
• Trust your instincts
• You are not alone
• You deserve safety

All services are FREE and CONFIDENTIAL.
Help is available 24/7.
"""

    def get_resources_by_need(self, need: str) -> str:
        """Get formatted resources based on specific needs"""

        need_lower = need.lower()
        output = []

        if "crisis" in need_lower or "emergency" in need_lower or "danger" in need_lower:
            output.append("🚨 CRISIS RESOURCES\n")
            output.append("If you're in immediate danger, call 911\n")
            for resource in self.get_crisis_resources():
                output.append(self.format_resource(resource))
                output.append("\n" + "="*60 + "\n")

        elif "shelter" in need_lower or "housing" in need_lower or "place to stay" in need_lower:
            output.append("🏠 SHELTER & HOUSING RESOURCES\n")
            output.append("Call the National DV Hotline for local shelter referrals:")
            output.append("📞 1-800-799-7233 (24/7)\n")
            for resource in self.get_by_type(ResourceType.SHELTER):
                output.append(self.format_resource(resource))
                output.append("\n" + "="*60 + "\n")

        elif "legal" in need_lower or "lawyer" in need_lower or "restraining order" in need_lower or "protection order" in need_lower:
            output.append("⚖️ LEGAL RESOURCES\n")
            for resource in self.get_by_type(ResourceType.LEGAL):
                output.append(self.format_resource(resource))
                output.append("\n" + "="*60 + "\n")

        elif "money" in need_lower or "financial" in need_lower or "assistance" in need_lower:
            output.append("💰 FINANCIAL RESOURCES\n")
            for resource in self.get_by_type(ResourceType.FINANCIAL):
                output.append(self.format_resource(resource))
                output.append("\n" + "="*60 + "\n")

        elif "counsel" in need_lower or "therap" in need_lower or "mental health" in need_lower:
            output.append("🧠 COUNSELING & MENTAL HEALTH RESOURCES\n")
            for resource in self.get_by_type(ResourceType.COUNSELING):
                output.append(self.format_resource(resource))
                output.append("\n" + "="*60 + "\n")

        elif "child" in need_lower or "kid" in need_lower:
            output.append("👶 CHILDREN'S RESOURCES\n")
            for resource in self.get_by_type(ResourceType.CHILDREN):
                output.append(self.format_resource(resource))
                output.append("\n" + "="*60 + "\n")

        elif "pet" in need_lower or "animal" in need_lower:
            output.append("🐾 PET SAFETY RESOURCES\n")
            for resource in self.get_by_type(ResourceType.PETS):
                output.append(self.format_resource(resource))
                output.append("\n" + "="*60 + "\n")

        elif "immig" in need_lower or "visa" in need_lower or "undocumented" in need_lower:
            output.append("🗽 IMMIGRATION RESOURCES\n")
            for resource in self.get_by_type(ResourceType.IMMIGRATION):
                output.append(self.format_resource(resource))
                output.append("\n" + "="*60 + "\n")

        elif "job" in need_lower or "employ" in need_lower or "work" in need_lower:
            output.append("💼 EMPLOYMENT RESOURCES\n")
            for resource in self.get_by_type(ResourceType.EMPLOYMENT):
                output.append(self.format_resource(resource))
                output.append("\n" + "="*60 + "\n")

        else:
            # General search
            results = self.search(need)
            if results:
                output.append(f"🔍 RESOURCES FOR: {need}\n")
                for resource in results[:5]:  # Top 5 results
                    output.append(self.format_resource(resource))
                    output.append("\n" + "="*60 + "\n")
            else:
                output.append("I couldn't find specific resources for that need.\n")
                output.append("Here are the National crisis resources that can help:\n\n")
                for resource in self.get_crisis_resources():
                    output.append(self.format_resource(resource))
                    output.append("\n" + "="*60 + "\n")

        return "\n".join(output)
