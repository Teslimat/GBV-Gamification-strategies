"""
Utility functions for parsing and processing simulation data
"""

import re
from typing import Tuple, Dict, Any

def parse_character_selection(response: str) -> Tuple[str, str]:
    """Parse character selection from persona response"""

    # Handle None or non-string responses
    if not response or not isinstance(response, str):
        return "Alex Chen", "Default selection due to invalid response"

    # Try to find CHOICE: and REASONING: patterns
    choice_match = re.search(r'CHOICE:\s*(.+?)(?:\n|REASONING|$)', response, re.IGNORECASE)
    reasoning_match = re.search(r'REASONING:\s*(.+?)$', response, re.IGNORECASE | re.DOTALL)

    if choice_match:
        choice = choice_match.group(1).strip()
        # Extract just the character name
        for char_name in ["Alex Chen", "Jordan Williams", "Sam Rivera"]:
            if char_name.lower() in choice.lower():
                choice = char_name
                break
    else:
        # Default if parsing fails
        choice = "Alex Chen"

    reasoning = reasoning_match.group(1).strip() if reasoning_match else "Selected based on background"

    return choice, reasoning

def parse_decision_response(response: str) -> Tuple[str, str]:
    """Parse decision choice from persona response"""

    # Handle None or non-string responses
    if not response or not isinstance(response, str):
        return "A", "Default choice due to invalid response"

    # Try to find CHOICE: and REASONING: patterns
    choice_match = re.search(r'CHOICE:\s*([A-D])', response, re.IGNORECASE)
    reasoning_match = re.search(r'REASONING:\s*(.+?)$', response, re.IGNORECASE | re.DOTALL)
    
    if choice_match:
        choice = choice_match.group(1).upper()
    else:
        # Try to find A, B, C, or D at start of line
        fallback = re.search(r'^([A-D])[\.\):\s]', response, re.MULTILINE)
        choice = fallback.group(1).upper() if fallback else "A"
    
    reasoning = reasoning_match.group(1).strip() if reasoning_match else "Default reasoning"
    
    return choice, reasoning

def parse_feedback_response(response: str) -> Dict[str, Any]:
    """Parse post-test survey feedback from persona response"""

    feedback = {
        "realistic": 3,
        "realistic_explain": "",
        "felt_safe": 3,
        "felt_safe_explain": "",
        "helpful_feedback": 3,
        "helpful_feedback_explain": "",
        "would_recommend": 3,
        "would_recommend_explain": "",
        "confidence": 3,
        "confidence_explain": "",
        "most_valuable_scenario": "",
        "likely_strategy": "",
        "what_worked": "",
        "improvements": "",
        "cultural_relevance": "",
        "raw_response": str(response) if response else ""
    }

    # Handle None or non-string responses
    if not response or not isinstance(response, str):
        return feedback

    # Extract numeric ratings (1-5) - now looking for Rate: pattern more carefully
    ratings_pattern = r'Rate:\s*(\d)'
    ratings = re.findall(ratings_pattern, response, re.IGNORECASE)

    if len(ratings) >= 5:
        feedback["realistic"] = int(ratings[0])
        feedback["felt_safe"] = int(ratings[1])
        feedback["helpful_feedback"] = int(ratings[2])
        feedback["would_recommend"] = int(ratings[3])
        feedback["confidence"] = int(ratings[4])

    # Extract explanations for ratings (questions 1-5)
    # Question 1 - Realism explanation
    realistic_explain = re.search(r'1\..*?Explain:\s*(.+?)(?=\n\d+\.|$)', response, re.DOTALL | re.IGNORECASE)
    if realistic_explain:
        feedback["realistic_explain"] = realistic_explain.group(1).strip()

    # Question 2 - Safety explanation
    safety_explain = re.search(r'2\..*?Explain:\s*(.+?)(?=\n\d+\.|$)', response, re.DOTALL | re.IGNORECASE)
    if safety_explain:
        feedback["felt_safe_explain"] = safety_explain.group(1).strip()

    # Question 3 - Feedback quality explanation
    helpful_explain = re.search(r'3\..*?Explain:\s*(.+?)(?=\n\d+\.|$)', response, re.DOTALL | re.IGNORECASE)
    if helpful_explain:
        feedback["helpful_feedback_explain"] = helpful_explain.group(1).strip()

    # Question 4 - Recommendation explanation
    recommend_explain = re.search(r'4\..*?Explain:\s*(.+?)(?=\n\d+\.|$)', response, re.DOTALL | re.IGNORECASE)
    if recommend_explain:
        feedback["would_recommend_explain"] = recommend_explain.group(1).strip()

    # Question 5 - Confidence explanation
    confidence_explain = re.search(r'5\..*?Explain:\s*(.+?)(?=\n\d+\.|$)', response, re.DOTALL | re.IGNORECASE)
    if confidence_explain:
        feedback["confidence_explain"] = confidence_explain.group(1).strip()

    # Extract text responses for open-ended questions
    # Question 6 - Most valuable scenario
    scenario_match = re.search(r'6\..*?Answer:\s*(.+?)(?=\n\d+\.|$)', response, re.DOTALL | re.IGNORECASE)
    if scenario_match:
        feedback["most_valuable_scenario"] = scenario_match.group(1).strip()

    # Question 7 - Likely strategy
    strategy_match = re.search(r'7\..*?Answer:\s*(.+?)(?=\n\d+\.|$)', response, re.DOTALL | re.IGNORECASE)
    if strategy_match:
        feedback["likely_strategy"] = strategy_match.group(1).strip()

    # Question 8 - What worked
    worked_match = re.search(r'8\..*?Answer:\s*(.+?)(?=\n\d+\.|$)', response, re.DOTALL | re.IGNORECASE)
    if worked_match:
        feedback["what_worked"] = worked_match.group(1).strip()

    # Question 9 - Improvements
    improve_match = re.search(r'9\..*?Answer:\s*(.+?)(?=\n\d+\.|$)', response, re.DOTALL | re.IGNORECASE)
    if improve_match:
        feedback["improvements"] = improve_match.group(1).strip()

    # Question 10 - Cultural relevance (NEW)
    cultural_match = re.search(r'10\..*?Answer:\s*(.+?)(?=\n\d+\.|$)', response, re.DOTALL | re.IGNORECASE)
    if cultural_match:
        feedback["cultural_relevance"] = cultural_match.group(1).strip()

    return feedback

def calculate_completion_rate(results: list) -> float:
    """Calculate completion rate from results"""
    if not results:
        return 0.0
    
    completed = sum(1 for r in results if r.get("completion_status") == "completed")
    return (completed / len(results)) * 100

def format_options(options_dict: Dict) -> str:
    """Format options dictionary for display"""
    return "\n".join([
        f"{key}. {value['text']}"
        for key, value in options_dict.items()
    ])