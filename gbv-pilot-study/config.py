"""
Configuration file for GBV MVP Simulation
"""
import os
from dotenv import load_dotenv

load_dotenv()

# OpenAI API Configuration (TinyTroupe uses OpenAI for persona simulation)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

# Simulation Settings
# For quick testing, use 3-5 personas. For full analysis, use 12-18 personas
NUM_PERSONAS = 12  # Number of personas to simulate (18 total available)
RANDOM_SEED = 42  # For reproducibility (change for different simulation runs)

# Scenario Configuration
NUM_SCENARIOS = 5
SKILLS = [
    "warning_signs",
    "direct_intervention", 
    "distraction",
    "support_survivor",
    "know_resources"
]

# Output Paths
OUTPUT_DIR = "outputs"
RESULTS_FILE = f"{OUTPUT_DIR}/simulation_results.json"
INTERACTION_CSV = f"{OUTPUT_DIR}/interaction_data.csv"
FEEDBACK_CSV = f"{OUTPUT_DIR}/feedback_data.csv"
REPORT_FILE = f"{OUTPUT_DIR}/analysis_report.md"

# Character Options (from Twine MVP)
CHARACTERS = {
    "Alex Chen": {
        "description": "International student, engineering major, resident advisor",
        "perspective": "Navigating cultural differences, campus leadership role"
    },
    "Jordan Williams": {
        "description": "Student athlete (soccer team), junior, active in campus life",
        "perspective": "Team dynamics, sports culture, male ally"
    },
    "Sam Rivera": {
        "description": "Art student, non-binary, involved in LGBTQ+ student group",
        "perspective": "Diverse identities, creative communities, advocacy"
    }
}

# Feedback Survey Questions (matching your post-test form)
SURVEY_QUESTIONS = {
    "realistic": "How realistic were the scenarios? (1-5)",
    "felt_safe": "Did you feel safe and respected? (1-5)",
    "helpful_feedback": "Was the feedback helpful? (1-5)",
    "would_recommend": "Would you recommend this? (1-5)",
    "most_valuable": "Which scenario was most valuable and why?",
    "likely_strategy": "Which strategy are you most likely to use?",
    "what_worked": "What worked well?",
    "improvements": "What could be improved?",
    "confidence": "How confident are you now in intervening? (1-5)"
}