"""
Main simulation script for GBV MVP using TinyTroupe
Simulates personas going through the Twine module
"""

# Load environment variables FIRST before any TinyTroupe imports
from dotenv import load_dotenv
load_dotenv()

import json
import random
from datetime import datetime, timedelta
from typing import Dict, List, Any
import os

from tinytroupe.agent import TinyPerson
from tinytroupe.environment import TinyWorld

from personas import ALL_PERSONAS
from config import *
from utils import *

class MVPSimulator:
    """Simulates user journeys through the GBV prevention MVP"""
    
    def __init__(self, scenarios_file="scenarios_map.json"):
        """Initialize simulator with scenario data"""
        with open(scenarios_file, 'r') as f:
            self.scenarios_data = json.load(f)
        
        self.results = []
        random.seed(RANDOM_SEED)
    
    def simulate_character_selection(self, persona: TinyPerson) -> Dict[str, Any]:
        """Simulate persona selecting a character"""

        character_prompt = f"""
        You are participating in a bystander intervention training module.

        You see three character options to experience scenarios through:

        1. Alex Chen: {CHARACTERS['Alex Chen']['description']}
           Perspective: {CHARACTERS['Alex Chen']['perspective']}

        2. Jordan Williams: {CHARACTERS['Jordan Williams']['description']}
           Perspective: {CHARACTERS['Jordan Williams']['perspective']}

        3. Sam Rivera: {CHARACTERS['Sam Rivera']['description']}
           Perspective: {CHARACTERS['Sam Rivera']['perspective']}

        Based on your background and personality, which character would you choose?

        Respond in this format:
        CHOICE: [character name]
        REASONING: [your reasoning in 2-3 sentences]
        """

        actions = persona.listen_and_act(character_prompt, return_actions=True)
        response = self._extract_talk_text(actions)
        character, reasoning = parse_character_selection(response)

        return {
            "character_selected": character,
            "reasoning": reasoning,
            "timestamp": datetime.now().isoformat()
        }

    def _extract_talk_text(self, actions: List) -> str:
        """Extract text from TALK actions in the actions list"""
        if not actions:
            return ""

        # Find all TALK actions and combine their content
        talk_texts = []
        for action in actions:
            if isinstance(action, dict) and action.get('action', {}).get('type') == 'TALK':
                content = action.get('action', {}).get('content', '')
                if content:
                    talk_texts.append(content)

        return " ".join(talk_texts)
    
    def simulate_scenario(self, persona: TinyPerson, scenario_data: Dict, 
                         current_skills: Dict[str, int]) -> Dict[str, Any]:
        """Simulate persona going through one scenario"""
        
        scenario_result = {
            "scenario_id": scenario_data["id"],
            "scenario_name": scenario_data["name"],
            "decisions": [],
            "skills_earned": [],
            "time_spent_seconds": random.randint(180, 420)  # 3-7 minutes per scenario
        }
        
        # Go through each decision point
        for decision_point in scenario_data["decision_points"]:
            decision_result = self.simulate_decision_point(
                persona, 
                scenario_data["context"],
                decision_point,
                current_skills
            )
            
            scenario_result["decisions"].append(decision_result)
            
            # Update skills based on choice
            chosen_option = decision_point["options"][decision_result["choice"]]
            for skill in chosen_option["skills"]:
                current_skills[skill] += 1
                if skill not in scenario_result["skills_earned"]:
                    scenario_result["skills_earned"].append(skill)
        
        return scenario_result
    
    def simulate_decision_point(self, persona: TinyPerson, context: str,
                               decision_point: Dict, skills: Dict) -> Dict[str, Any]:
        """Simulate a single decision point"""
        
        # Format options for persona
        options_text = "\n".join([
            f"{key}. {opt['text']}"
            for key, opt in decision_point["options"].items()
        ])
        
        decision_prompt = f"""
        SCENARIO CONTEXT:
        {context}

        {decision_point['prompt']}

        OPTIONS:
        {options_text}

        Based on your personality traits and prior experience, which option would you choose?
        Consider:
        - Your comfort level with confrontation
        - Your intervention style preferences
        - What feels authentic to who you are
        - What you think would be most effective

        Respond in this format:
        CHOICE: [A, B, C, or D]
        REASONING: [Explain your choice in 2-4 sentences, relating it to your personality and values]
        """

        actions = persona.listen_and_act(decision_prompt, return_actions=True)
        response = self._extract_talk_text(actions)
        choice, reasoning = parse_decision_response(response)
        
        # Validate choice
        if choice not in decision_point["options"]:
            choice = random.choice(list(decision_point["options"].keys()))
            reasoning = "Default choice due to parsing error"
        
        return {
            "decision_id": decision_point["id"],
            "choice": choice,
            "choice_text": decision_point["options"][choice]["text"],
            "reasoning": reasoning,
            "feedback_received": decision_point["options"][choice]["feedback"]
        }
    
    def generate_feedback_response(self, persona: TinyPerson,
                                   journey_data: Dict) -> Dict[str, Any]:
        """Generate post-test survey responses"""

        # Calculate some stats for context
        total_time = sum(s["time_spent_seconds"] for s in journey_data["scenarios"]) / 60
        skills_total = sum(journey_data["final_skills"].values())

        # Get persona background for context-aware feedback
        comfort_level = persona._persona.get("preferences", {}).get("comfort_with_confrontation", "moderate")
        intervention_style = persona._persona.get("preferences", {}).get("intervention_style", "thoughtful")

        feedback_prompt = f"""
        You just completed a trauma-informed, gamified bystander intervention training module for preventing gender-based violence on campus.

        YOUR JOURNEY SUMMARY:
        - Character perspective: {journey_data['character_selection']['character_selected']}
        - Total time: {total_time:.1f} minutes
        - Scenarios completed: {len(journey_data['scenarios'])}/5
        - Skills developed: {skills_total} total skill points across 5 intervention areas
        - Your intervention style: {intervention_style}
        - Your comfort with confrontation: {comfort_level}

        Please provide honest, detailed feedback based on your personality, cultural background, and experience.
        Be specific and constructive - this feedback will help improve the training for diverse students.

        1. REALISM: How realistic and relatable were the scenarios? (1=very unrealistic, 5=very realistic)
        Rate: [1-5]
        Explain: Did the scenarios reflect situations you might actually encounter on campus?
        Were the characters and dialogue authentic? [2-3 sentences]

        2. SAFETY & TRAUMA-INFORMED DESIGN: Did you feel emotionally safe and respected throughout? (1=not at all, 5=very much)
        Rate: [1-5]
        Explain: Did the training handle sensitive topics appropriately? Were trigger warnings adequate?
        Did you feel any content was re-traumatizing or insensitive? [2-3 sentences]

        3. FEEDBACK QUALITY: Was the feedback after your choices helpful and instructive? (1=not helpful, 5=very helpful)
        Rate: [1-5]
        Explain: Did the feedback explain WHY your choice worked or what alternatives exist?
        Did it teach you practical strategies? [2-3 sentences]

        4. RECOMMENDATION: Would you recommend this to other students? (1=definitely not, 5=definitely yes)
        Rate: [1-5]
        Explain: Why or why not? What types of students would benefit most?
        Are there students who might find it unhelpful or problematic? [2-3 sentences]

        5. CONFIDENCE CHANGE: How confident do you feel now in intervening as a bystander? (1=not confident, 5=very confident)
        Rate: [1-5]
        Explain: What specific skills or insights increased your confidence?
        What barriers to intervention do you still feel? [2-3 sentences]

        6. MOST VALUABLE SCENARIO: Which scenario was most valuable to you and why?
        Answer: [Name the specific scenario (Party Observation, Friend Disclosure, Group Chat, Consent Conversation, or Campus Response)
        and explain in 3-4 sentences what made it impactful. Consider: Did it teach you something new?
        Did it relate to your experiences? Was the approach practical?]

        7. LIKELY STRATEGY: Which intervention strategy (Direct, Distraction, Delegation, or Delay) are you most likely to actually use in real life?
        Answer: [Name the strategy and explain in 3-4 sentences why it fits your personality and comfort level.
        Give an example of when you might use it.]

        8. WHAT WORKED WELL: What aspects of this training were most effective?
        Answer: [List 3-4 specific things that worked well. Consider: Gamification elements (character choice, skills),
        scenario diversity, cultural relevance, choice feedback, pace, engagement, trauma-informed approach, etc.]

        9. IMPROVEMENTS NEEDED: What could be improved to make this training more effective?
        Answer: [Provide 3-4 specific, constructive suggestions. Consider: More diverse scenarios,
        better representation of different identities, clearer instructions, more nuanced choices,
        additional resources, accessibility concerns, etc.]

        10. CULTURAL RELEVANCE: How well did this training account for diverse cultural perspectives and identities?
        Answer: [2-3 sentences about whether the training felt inclusive of your background and identity.
        Were there cultural considerations that were missing or well-handled?]

        Respond in a structured format with each question number clearly marked.
        """

        actions = persona.listen_and_act(feedback_prompt, return_actions=True)
        response = self._extract_talk_text(actions)
        feedback = parse_feedback_response(response)
        
        return feedback
    
    def simulate_full_journey(self, persona: TinyPerson) -> Dict[str, Any]:
        """Simulate complete journey through MVP for one persona"""
        
        print(f"\n{'='*60}")
        print(f"Simulating: {persona.name}")
        print(f"{'='*60}")
        
        journey = {
            "persona_id": persona.name,
            "persona_background": str(persona._persona.get("nationality", "")) + " - " + str(persona._persona.get("professional_interests", "")),
            "start_time": datetime.now().isoformat(),
            "character_selection": {},
            "scenarios": [],
            "final_skills": {skill: 0 for skill in SKILLS},
            "feedback": {},
            "completion_status": "incomplete"
        }
        
        try:
            # 1. Character Selection
            print("  → Selecting character...")
            journey["character_selection"] = self.simulate_character_selection(persona)
            
            # 2. Go through scenarios
            for scenario_data in self.scenarios_data["scenarios"]:
                print(f"  → Scenario {scenario_data['id']}: {scenario_data['name']}")
                scenario_result = self.simulate_scenario(
                    persona,
                    scenario_data,
                    journey["final_skills"]
                )
                journey["scenarios"].append(scenario_result)
            
            journey["completion_status"] = "completed"
            
            # 3. Generate feedback
            print("  → Generating feedback...")
            journey["feedback"] = self.generate_feedback_response(persona, journey)
            
            journey["end_time"] = datetime.now().isoformat()
            
            print(f"  ✓ Completed! Skills: {journey['final_skills']}")
            
        except Exception as e:
            import traceback
            print(f"  ✗ Error: {str(e)}")
            print(f"  Full traceback:")
            traceback.print_exc()
            journey["completion_status"] = "error"
            journey["error"] = str(e)
            journey["error_traceback"] = traceback.format_exc()
        
        return journey
    
    def run_simulation(self, personas: List[TinyPerson] = None) -> List[Dict]:
        """Run simulation for all personas"""
        
        if personas is None:
            personas = ALL_PERSONAS[:NUM_PERSONAS]
        
        print(f"\n{'#'*60}")
        print(f"# GBV MVP SIMULATION")
        print(f"# Total Personas: {len(personas)}")
        print(f"# Scenarios: {NUM_SCENARIOS}")
        print(f"{'#'*60}\n")
        
        for i, persona in enumerate(personas, 1):
            print(f"\n[{i}/{len(personas)}] ", end="")
            journey = self.simulate_full_journey(persona)
            self.results.append(journey)
        
        # Save results
        self.save_results()
        
        print(f"\n{'#'*60}")
        print(f"# SIMULATION COMPLETE")
        print(f"# Results saved to: {RESULTS_FILE}")
        print(f"{'#'*60}\n")
        
        return self.results
    
    def save_results(self):
        """Save simulation results to file"""
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        
        with open(RESULTS_FILE, 'w') as f:
            json.dump(self.results, f, indent=2)
        
        print(f"\n✓ Results saved to: {RESULTS_FILE}")

def main():
    """Main execution"""
    
    # Initialize simulator
    simulator = MVPSimulator()
    
    # Run simulation
    results = simulator.run_simulation()
    
    # Quick summary
    completed = sum(1 for r in results if r["completion_status"] == "completed")
    print(f"\nSummary:")
    print(f"  Total simulated: {len(results)}")
    print(f"  Completed: {completed}")
    print(f"  Completion rate: {completed/len(results)*100:.1f}%")

if __name__ == "__main__":
    main()