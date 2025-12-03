# GBV MVP Simulation - Complete Implementation

## Overview

This package simulates user interactions with the GBV Prevention MVP using TinyTroupe AI personas.

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set Up Environment

Create `.env` file:
```
OPENAI_API_KEY=your-api-key-here
```

### 3. Run Simulation
```bash
python simulate_mvp.py
```

This will:
- Simulate 18 diverse personas
- Generate interaction data
- Save results to `outputs/simulation_results.json`

### 4. Analyze Results
```bash
python analyze_simulation.py
```

This will:
- Generate `interaction_data.csv`
- Generate `feedback_data.csv`
- Create visualizations
- Generate analysis report

## Project Structure
```
gbv-mvp-simulation/
├── config.py              # Configuration settings
├── personas.py            # 18 diverse persona definitions
├── scenarios_map.json     # Scenario structure from Twine
├── simulate_mvp.py        # Main simulation script
├── analyze_simulation.py  # Analysis and reporting
├── utils.py               # Helper functions
├── mapping_template.md    # Twine-to-TinyTroupe mapping
└── outputs/               # Generated results
    ├── simulation_results.json
    ├── interaction_data.csv
    ├── feedback_data.csv
    ├── analysis_report.md
    └── plots/
```

## Outputs

### simulation_results.json
Complete raw data from all persona journeys including:
- Character selections
- Decision paths
- Skills earned
- Feedback responses

### interaction_data.csv
Quantitative metrics for data analysis:
- Completion rates
- Time spent
- Skill development
- User experience ratings

### feedback_data.csv
Qualitative feedback responses:
- What worked
- Improvements needed
- Most valuable scenarios
- Likely strategies

### analysis_report.md
Comprehensive analysis including:
- Executive summary
- Metrics against success criteria
- Recommendations for refinement
- Visualizations

## Customization

### Adding Personas

Edit `personas.py` to add more personas:
```python
new_persona = TinyPerson(
    name="Your Name",
    age=20,
    nationality="Your Nationality",
    personality_traits=[...],
    ...
)
```

### Modifying Scenarios

Edit `scenarios_map.json` to update scenario content, options, or skills.

### Changing Success Criteria

Edit `config.py` to adjust targets for completion rate, user experience, etc.

## Troubleshooting

### "No module named tinytroupe"
```bash
pip install tinytroupe
```

### "OpenAI API key not found"
Add your API key to `.env` file

### Parsing Errors
Check `simulation_results.json` for raw responses and adjust parsing logic in `utils.py`

## Next Steps

1. Review analysis report (`outputs/analysis_report.md`)
2. Identify areas for MVP refinement (Step 5)
3. Prepare for real user pilot test validation
4. Document methodology for thesis

## Support

For questions about:
- Twine MVP: See Twine documentation from previous response
- TinyTroupe simulation: See official TinyTroupe docs
- This implementation: Review code comments and docstrings