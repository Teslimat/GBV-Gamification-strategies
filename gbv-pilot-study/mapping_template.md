# Twine to TinyTroupe Mapping Template

## Purpose
This document maps your Twine MVP structure to the TinyTroupe simulation format, ensuring accurate simulation of user journeys.

---

## Character Mapping

| Twine Character | Description | Target Persona Types |
|----------------|-------------|---------------------|
| Alex Chen | International student, RA | Personas with international background, cautious, culturally aware |
| Jordan Williams | Student athlete, male ally | Personas who are confident, team-oriented, direct |
| Sam Rivera | Non-binary artist, LGBTQ+ advocate | Personas who are empathetic, experienced advocates |

---

## Scenario Structure

### Scenario 1: Party Observation

**Twine Passage Names:**
- `Scenario1 Setup`
- `Scenario1 Decision1`
- Decision paths: `S1 Direct Intervention`, `S1 Distraction`, `S1 Get Help`, `S1 Observe`
- `S1 Followup`
- Resolution: `S1 Get Home`, `S1 Stay With`, `S1 Find Friends`
- `S1 Reflection`

**Skills Earned:**
- Option A (Direct): `direct_intervention +1`, `warning_signs +1`
- Option B (Distraction): `distraction +1`, `warning_signs +1`
- Option C (Get Help): `direct_intervention +1`, `warning_signs +1`
- Option D (Observe): `warning_signs +1`
- Follow-up options: `support_survivor +1`

**TinyTroupe Mapping:**
See `scenarios_map.json` - `scenario_1`

---

### Scenario 2-5: [Repeat Format]

[Map each scenario following the same template]

---

## Dashboard Skill Tracking

**Twine Variables:**
```
$skills.warning_signs
$skills.direct_intervention
$skills.distraction
$skills.support_survivor
$skills.know_resources
```

**TinyTroupe Equivalent:**
```python
journey["final_skills"] = {
    "warning_signs": 0,
    "direct_intervention": 0,
    "distraction": 0,
    "support_survivor": 0,
    "know_resources": 0
}
```

---

## Feedback Questions Alignment

**Twine Safety Features:**
- Content warning before module
- Pause buttons throughout
- Emotional check-ins after scenarios
- Resources page accessible

**TinyTroupe Survey Questions:**
Match exactly to your Google Forms post-test questions (see `config.py` SURVEY_QUESTIONS)

---

## Quality Assurance Checklist

- [ ] All Twine scenario passages are documented in `scenarios_map.json`
- [ ] Skill increments match between Twine and TinyTroupe
- [ ] Character descriptions align
- [ ] Decision options are identical
- [ ] Feedback text is captured
- [ ] Survey questions match Google Forms

---

## Notes for Future Updates

When you add or modify Twine content:

1. Update `scenarios_map.json` with new decision points
2. Verify skill tracking logic matches
3. Re-run simulation to test changes
4. Document any new passages or branches here