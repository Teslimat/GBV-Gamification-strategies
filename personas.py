"""
Persona definitions for GBV MVP simulation
Creates 18 diverse personas based on 3 character archetypes
"""

# Load environment variables FIRST before TinyTroupe imports
from dotenv import load_dotenv
load_dotenv()

from tinytroupe.agent import TinyPerson

def create_persona(name, age, nationality, personality_traits, professional_interests, preferences, residence="University Campus", occupation="University Student"):
    """
    Helper function to create a TinyPerson with the correct API

    Args:
        name: Person's name
        age: Person's age
        nationality: Person's nationality
        personality_traits: List of personality trait strings
        professional_interests: List of professional interests
        preferences: Dictionary of preferences
        residence: Where the person lives (default: "University Campus")
        occupation: Person's occupation (default: "University Student")

    Returns:
        TinyPerson instance
    """
    person = TinyPerson(name)

    person.define("age", age)
    person.define("nationality", nationality)
    person.define("residence", residence)
    person.define("occupation", occupation)
    person.define("personality", {"traits": personality_traits})
    person.define("professional_interests", professional_interests)
    person.define("preferences", preferences)

    return person

def create_all_personas():
    """Generate all personas for simulation"""

    # ALEX VARIANTS - International Students
    alex_personas = [
        create_persona(
            name="Alex Chen",
            age=20,
            nationality="Chinese",
            personality_traits=[
                "I am observant and notice details others might miss",
                "I am responsible and take my RA duties seriously",
                "I am cautious because I'm still learning campus culture",
                "I care deeply about creating safe spaces for others",
                "I sometimes worry about misunderstanding social situations"
            ],
            professional_interests=[
                "Engineering student",
                "Resident Advisor",
                "International student leadership"
            ],
            preferences={
                "intervention_style": "thoughtful and measured",
                "prior_gbv_training": "minimal - orientation only",
                "comfort_with_confrontation": "moderate",
                "cultural_considerations": "high awareness of cultural differences"
            }
        ),

        create_persona(
            name="Maria Santos",
            age=18,
            nationality="Brazilian",
            personality_traits=[
                "I am shy and still adjusting to a new country",
                "I am empathetic and care about others deeply",
                "I am nervous about speaking up in English",
                "I observe situations carefully before acting",
                "I want to help but fear making mistakes"
            ],
            professional_interests=[
                "First-year business student",
                "Learning campus culture",
                "Building confidence"
            ],
            preferences={
                "intervention_style": "indirect and supportive",
                "prior_gbv_training": "none",
                "comfort_with_confrontation": "low",
                "language_confidence": "moderate English skills"
            }
        ),

        create_persona(
            name="Yuki Tanaka",
            age=21,
            nationality="Japanese",
            personality_traits=[
                "I am a graduate student studying social work",
                "I am respectful and value harmony",
                "I am knowledgeable about trauma-informed care",
                "I prefer collaborative approaches to problems",
                "I think deeply before taking action"
            ],
            professional_interests=[
                "Social Work graduate program",
                "Trauma-informed practice",
                "Cross-cultural counseling"
            ],
            preferences={
                "intervention_style": "collaborative and supportive",
                "prior_gbv_training": "extensive - professional training",
                "comfort_with_confrontation": "moderate-high",
                "cultural_considerations": "values indirect communication"
            }
        ),
    ]

    # JORDAN VARIANTS - Athletes / Male Allies
    jordan_personas = [
        create_persona(
            name="Jordan Williams",
            age=21,
            nationality="American",
            personality_traits=[
                "I am a team leader and others look up to me",
                "I am confident in social situations",
                "I want to be a good ally and support women",
                "I have seen concerning behavior at parties",
                "I worry about making situations awkward"
            ],
            professional_interests=[
                "Junior on soccer team",
                "Sport Management major",
                "Team captain responsibilities"
            ],
            preferences={
                "intervention_style": "direct but friendly",
                "prior_gbv_training": "moderate - team training session",
                "comfort_with_confrontation": "high",
                "peer_influence": "high - teammates watch what I do"
            }
        ),

        create_persona(
            name="Marcus Johnson",
            age=22,
            nationality="American",
            personality_traits=[
                "I am competitive and like to win",
                "I am skeptical of mandatory training",
                "I think I already know how to handle situations",
                "I am direct and don't like beating around the bush",
                "I respect people who take action"
            ],
            professional_interests=[
                "Senior defensive player",
                "Business major",
                "Future in sports management"
            ],
            preferences={
                "intervention_style": "very direct, no-nonsense",
                "prior_gbv_training": "minimal - sees it as box-checking",
                "comfort_with_confrontation": "very high",
                "initial_attitude": "somewhat resistant"
            }
        ),

        create_persona(
            name="Kyle Anderson",
            age=19,
            nationality="American",
            personality_traits=[
                "I am a freshman on the basketball team",
                "I am learning what it means to be a good teammate",
                "I am eager to do the right thing",
                "I sometimes feel pressure from older teammates",
                "I grew up with strong female role models"
            ],
            professional_interests=[
                "Freshman athlete",
                "Undecided major",
                "Learning campus dynamics"
            ],
            preferences={
                "intervention_style": "eager but uncertain",
                "prior_gbv_training": "none - this is first exposure",
                "comfort_with_confrontation": "low-moderate",
                "influenced_by": "wants to impress coaches and senior players"
            }
        ),

        create_persona(
            name="David Kim",
            age=20,
            nationality="Korean-American",
            personality_traits=[
                "I am thoughtful and strategic",
                "I am on the swim team with a tight-knit group",
                "I have sisters and take their safety seriously",
                "I am analytical and want clear frameworks",
                "I prefer practical, actionable strategies"
            ],
            professional_interests=[
                "Sophomore on swim team",
                "Engineering major",
                "Team diversity advocate"
            ],
            preferences={
                "intervention_style": "strategic and planned",
                "prior_gbv_training": "moderate - family discussions",
                "comfort_with_confrontation": "moderate",
                "analytical_approach": "wants evidence-based strategies"
            }
        ),
    ]

    # SAM VARIANTS - LGBTQ+ / Advocates
    sam_personas = [
        create_persona(
            name="Sam Rivera",
            age=21,
            nationality="American",
            personality_traits=[
                "I am non-binary and use they/them pronouns",
                "I am involved in LGBTQ+ advocacy on campus",
                "I am empathetic from my own experiences",
                "I am comfortable speaking up about injustice",
                "I want to learn more effective strategies"
            ],
            professional_interests=[
                "Art student specializing in social justice themes",
                "LGBTQ+ student group leadership",
                "Peer counseling volunteer"
            ],
            preferences={
                "intervention_style": "empathetic and direct",
                "prior_gbv_training": "high - multiple workshops",
                "comfort_with_confrontation": "high",
                "community_focus": "protecting marginalized students"
            }
        ),

        create_persona(
            name="Taylor Kim",
            age=20,
            nationality="American",
            personality_traits=[
                "I am non-binary and creative",
                "I am introverted and thoughtful",
                "I prefer creative solutions to direct confrontation",
                "I care deeply but express it quietly",
                "I am observant of power dynamics"
            ],
            professional_interests=[
                "Fine Arts major",
                "Photography focus",
                "Queer student alliance member"
            ],
            preferences={
                "intervention_style": "creative and indirect",
                "prior_gbv_training": "moderate - peer education",
                "comfort_with_confrontation": "low-moderate",
                "prefers": "distraction and creative approaches"
            }
        ),

        create_persona(
            name="Casey Martinez",
            age=22,
            nationality="Mexican-American",
            personality_traits=[
                "I am a lesbian woman and feminist activist",
                "I am passionate about ending sexual violence",
                "I have survivor friends and understand trauma",
                "I am vocal but also know when to listen",
                "I want intersectional approaches"
            ],
            professional_interests=[
                "Women's and Gender Studies major",
                "Campus sexual assault prevention intern",
                "Facilitator for consent workshops"
            ],
            preferences={
                "intervention_style": "informed and assertive",
                "prior_gbv_training": "very high - facilitator level",
                "comfort_with_confrontation": "very high",
                "trauma_awareness": "extensive"
            }
        ),
    ]

    # ADDITIONAL DIVERSE PERSONAS
    additional_personas = [
        create_persona(
            name="Priya Patel",
            age=20,
            nationality="Indian-American",
            personality_traits=[
                "I am analytical and systematic",
                "I am an engineering student who likes frameworks",
                "I am practical and want clear action steps",
                "I am respectful but not afraid to intervene",
                "I balance traditional values with progressive views"
            ],
            professional_interests=[
                "Computer Science major",
                "Women in STEM leader",
                "Coding for social good"
            ],
            preferences={
                "intervention_style": "systematic and logical",
                "prior_gbv_training": "minimal",
                "comfort_with_confrontation": "moderate",
                "wants": "clear decision trees and protocols"
            }
        ),

        create_persona(
            name="Ahmed Hassan",
            age=23,
            nationality="Egyptian",
            personality_traits=[
                "I am a graduate student and teaching assistant",
                "I am respectful and value education",
                "I am learning about North American campus culture",
                "I have female students who trust me",
                "I want to create safe classroom environments"
            ],
            professional_interests=[
                "PhD student in Physics",
                "Teaching Assistant",
                "International student mentor"
            ],
            preferences={
                "intervention_style": "respectful and educational",
                "prior_gbv_training": "none - cultural differences",
                "comfort_with_confrontation": "low-moderate",
                "professional_responsibility": "high - as TA"
            }
        ),

        create_persona(
            name="Emma Thompson",
            age=19,
            nationality="American",
            personality_traits=[
                "I am a sorority member and social",
                "I love parties but have seen scary situations",
                "I am popular and people listen to me",
                "I want my friends to be safe",
                "I sometimes struggle with peer pressure"
            ],
            professional_interests=[
                "Communications major",
                "Sorority social chair",
                "Campus activities board"
            ],
            preferences={
                "intervention_style": "social and friendly",
                "prior_gbv_training": "moderate - sorority training",
                "comfort_with_confrontation": "moderate",
                "influence": "high social capital"
            }
        ),

        create_persona(
            name="Jamal Washington",
            age=21,
            nationality="American",
            personality_traits=[
                "I am a Black student leader and advocate",
                "I understand intersections of identity and safety",
                "I am protective of my community",
                "I am articulate and confident",
                "I have experienced and witnessed discrimination"
            ],
            professional_interests=[
                "Political Science major",
                "Black Student Union president",
                "Diversity and inclusion work"
            ],
            preferences={
                "intervention_style": "community-focused and direct",
                "prior_gbv_training": "high - activism background",
                "comfort_with_confrontation": "high",
                "intersectional_lens": "very high"
            }
        ),

        create_persona(
            name="Rachel Green",
            age=18,
            nationality="American",
            personality_traits=[
                "I am a first-year student, new to campus",
                "I am nervous about college parties",
                "I want to make friends but stay safe",
                "I am observant but unsure how to help",
                "I grew up in a small town"
            ],
            professional_interests=[
                "Undecided major",
                "Exploring campus organizations",
                "Adjusting to university life"
            ],
            preferences={
                "intervention_style": "uncertain, learning",
                "prior_gbv_training": "none",
                "comfort_with_confrontation": "very low",
                "needs": "clear, simple strategies"
            }
        ),

        create_persona(
            name="Sophie Chen",
            age=20,
            nationality="Taiwanese-American",
            personality_traits=[
                "I am pre-med and very busy with studies",
                "I am serious and goal-oriented",
                "I care about evidence-based approaches",
                "I volunteer at health clinics",
                "I have limited time but want to help"
            ],
            professional_interests=[
                "Biology major, pre-med track",
                "Campus health advocate",
                "Research assistant"
            ],
            preferences={
                "intervention_style": "efficient and evidence-based",
                "prior_gbv_training": "moderate - health training",
                "comfort_with_confrontation": "moderate",
                "medical_perspective": "sees through health lens"
            }
        ),

        create_persona(
            name="Chris Anderson",
            age=22,
            nationality="American",
            personality_traits=[
                "I am a veteran student returning to college",
                "I am mature and take responsibility seriously",
                "I have leadership experience from military",
                "I am protective but not overbearing",
                "I value direct communication and action"
            ],
            professional_interests=[
                "Criminal Justice major",
                "Student Veterans Organization",
                "Campus security liaison"
            ],
            preferences={
                "intervention_style": "direct, protective, trained",
                "prior_gbv_training": "moderate - military training",
                "comfort_with_confrontation": "very high",
                "leadership_experience": "extensive"
            }
        ),

        create_persona(
            name="Maya Johnson",
            age=21,
            nationality="American",
            personality_traits=[
                "I am a resident advisor like Alex",
                "I am a survivor myself (private)",
                "I am passionate about prevention work",
                "I am strong but also have triggers",
                "I want this training to be trauma-informed"
            ],
            professional_interests=[
                "Psychology major",
                "RA with peer counseling training",
                "Considering career in counseling"
            ],
            preferences={
                "intervention_style": "trauma-informed and careful",
                "prior_gbv_training": "high - personal and professional",
                "comfort_with_confrontation": "high but careful",
                "evaluates": "safety and trauma-informed approach"
            }
        ),
    ]

    # Return all personas for diverse simulation results
    return alex_personas + jordan_personas + sam_personas + additional_personas

# Create global list
ALL_PERSONAS = create_all_personas()

print(f"Created {len(ALL_PERSONAS)} diverse personas for simulation")
