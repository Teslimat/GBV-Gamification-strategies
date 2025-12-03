"""
Analysis script for GBV MVP simulation results
Generates quantitative metrics and qualitative summaries
"""

import json
import pandas as pd
import numpy as np
from collections import Counter
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, List, Any
import os

from config import *

class SimulationAnalyzer:
    """Analyzes TinyTroupe simulation results"""
    
    def __init__(self, results_file=RESULTS_FILE):
        """Load results from JSON file"""
        with open(results_file, 'r') as f:
            self.results = json.load(f)
        
        print(f"Loaded {len(self.results)} simulation results")
    
    def generate_interaction_data(self) -> pd.DataFrame:
        """Generate interaction data matching your data analysis requirements"""
        
        interaction_data = []
        
        for result in self.results:
            if result["completion_status"] != "completed":
                continue
            
            # Calculate metrics
            total_time_min = sum(s["time_spent_seconds"] for s in result["scenarios"]) / 60
            completion_pct = (len(result["scenarios"]) / NUM_SCENARIOS) * 100
            
            row = {
                "persona_id": result["persona_id"],
                "persona_background": result["persona_background"],
                "character_selected": result["character_selection"]["character_selected"],
                "scenarios_completed": len(result["scenarios"]),
                "completion_pct": completion_pct,
                "total_time_min": round(total_time_min, 1),
                "avg_time_per_scenario_min": round(total_time_min / len(result["scenarios"]), 1),
            }
            
            # Add skill levels
            for skill in SKILLS:
                row[f"skill_{skill}"] = result["final_skills"][skill]
            
            # Add feedback ratings
            feedback = result.get("feedback", {})
            row["realistic_rating"] = feedback.get("realistic", 0)
            row["felt_safe_rating"] = feedback.get("felt_safe", 0)
            row["helpful_feedback_rating"] = feedback.get("helpful_feedback", 0)
            row["would_recommend_rating"] = feedback.get("would_recommend", 0)
            row["confidence_rating"] = feedback.get("confidence", 0)
            
            interaction_data.append(row)
        
        df = pd.DataFrame(interaction_data)
        df.to_csv(INTERACTION_CSV, index=False)
        print(f"✓ Saved interaction data: {INTERACTION_CSV}")
        
        return df
    
    def generate_feedback_data(self) -> pd.DataFrame:
        """Generate qualitative feedback data"""
        
        feedback_data = []
        
        for result in self.results:
            if result["completion_status"] != "completed":
                continue
            
            feedback = result.get("feedback", {})
            
            row = {
                "persona_id": result["persona_id"],
                "character_selected": result["character_selection"]["character_selected"],
                "realistic_rating": feedback.get("realistic", 0),
                "realistic_explain": feedback.get("realistic_explain", ""),
                "felt_safe_rating": feedback.get("felt_safe", 0),
                "felt_safe_explain": feedback.get("felt_safe_explain", ""),
                "helpful_feedback_rating": feedback.get("helpful_feedback", 0),
                "helpful_feedback_explain": feedback.get("helpful_feedback_explain", ""),
                "would_recommend_rating": feedback.get("would_recommend", 0),
                "would_recommend_explain": feedback.get("would_recommend_explain", ""),
                "confidence_rating": feedback.get("confidence", 0),
                "confidence_explain": feedback.get("confidence_explain", ""),
                "most_valuable_scenario": feedback.get("most_valuable_scenario", ""),
                "likely_strategy": feedback.get("likely_strategy", ""),
                "what_worked": feedback.get("what_worked", ""),
                "improvements": feedback.get("improvements", ""),
                "cultural_relevance": feedback.get("cultural_relevance", ""),
            }
            
            feedback_data.append(row)
        
        df = pd.DataFrame(feedback_data)
        df.to_csv(FEEDBACK_CSV, index=False)
        print(f"✓ Saved feedback data: {FEEDBACK_CSV}")
        
        return df
    
    def analyze_completion_metrics(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Analyze completion and engagement metrics"""
        
        metrics = {
            "total_participants": len(self.results),
            "completed": len(df),
            "completion_rate_pct": len(df) / len(self.results) * 100 if self.results else 0,
            "avg_scenarios_completed": df["scenarios_completed"].mean(),
            "avg_total_time_min": df["total_time_min"].mean(),
            "avg_time_per_scenario_min": df["avg_time_per_scenario_min"].mean(),
            "min_time": df["total_time_min"].min(),
            "max_time": df["total_time_min"].max(),
        }
        
        return metrics
    
    def analyze_character_selection(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Analyze character selection patterns"""
        
        character_counts = df["character_selected"].value_counts().to_dict()
        character_pct = (df["character_selected"].value_counts(normalize=True) * 100).to_dict()
        
        return {
            "counts": character_counts,
            "percentages": character_pct
        }
    
    def analyze_skill_development(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Analyze skill acquisition patterns"""
        
        skill_cols = [f"skill_{skill}" for skill in SKILLS]
        
        skill_stats = {}
        for skill in SKILLS:
            col = f"skill_{skill}"
            skill_stats[skill] = {
                "mean": df[col].mean(),
                "median": df[col].median(),
                "std": df[col].std(),
                "min": df[col].min(),
                "max": df[col].max()
            }
        
        return skill_stats
    
    def analyze_decision_patterns(self) -> Dict[str, Any]:
        """Analyze decision-making patterns across scenarios"""
        
        decision_patterns = {}
        
        for scenario_id in [f"scenario_{i}" for i in range(1, NUM_SCENARIOS + 1)]:
            scenario_decisions = {}
            
            for result in self.results:
                if result["completion_status"] != "completed":
                    continue
                
                for scenario in result["scenarios"]:
                    if scenario["scenario_id"] == scenario_id:
                        for decision in scenario["decisions"]:
                            decision_id = decision["decision_id"]
                            choice = decision["choice"]
                            
                            if decision_id not in scenario_decisions:
                                scenario_decisions[decision_id] = Counter()
                            
                            scenario_decisions[decision_id][choice] += 1
            
            decision_patterns[scenario_id] = scenario_decisions
        
        return decision_patterns
    
    def analyze_user_experience(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Analyze user experience ratings"""
        
        ux_metrics = {
            "realistic": {
                "mean": df["realistic_rating"].mean(),
                "median": df["realistic_rating"].median(),
                "pct_4_or_5": (df["realistic_rating"] >= 4).sum() / len(df) * 100
            },
            "felt_safe": {
                "mean": df["felt_safe_rating"].mean(),
                "median": df["felt_safe_rating"].median(),
                "pct_4_or_5": (df["felt_safe_rating"] >= 4).sum() / len(df) * 100
            },
            "helpful_feedback": {
                "mean": df["helpful_feedback_rating"].mean(),
                "median": df["helpful_feedback_rating"].median(),
                "pct_4_or_5": (df["helpful_feedback_rating"] >= 4).sum() / len(df) * 100
            },
            "would_recommend": {
                "mean": df["would_recommend_rating"].mean(),
                "median": df["would_recommend_rating"].median(),
                "pct_4_or_5": (df["would_recommend_rating"] >= 4).sum() / len(df) * 100
            },
            "confidence": {
                "mean": df["confidence_rating"].mean(),
                "median": df["confidence_rating"].median(),
                "pct_4_or_5": (df["confidence_rating"] >= 4).sum() / len(df) * 100
            }
        }
        
        return ux_metrics
    
    def extract_qualitative_themes(self, df: pd.DataFrame) -> Dict[str, List[str]]:
        """Extract qualitative themes from feedback"""
        
        themes = {
            "what_worked": [],
            "improvements": [],
            "most_valuable_scenarios": [],
            "likely_strategies": []
        }
        
        # Collect all responses
        for _, row in df.iterrows():
            if row["what_worked"]:
                themes["what_worked"].append(row["what_worked"])
            if row["improvements"]:
                themes["improvements"].append(row["improvements"])
            if row["most_valuable_scenario"]:
                themes["most_valuable_scenarios"].append(row["most_valuable_scenario"])
            if row["likely_strategy"]:
                themes["likely_strategies"].append(row["likely_strategy"])
        
        return themes

    def analyze_intervention_strategies(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Analyze intervention strategy preferences"""
        strategies = []
        for _, row in df.iterrows():
            strategy_text = row.get("likely_strategy", "")
            if strategy_text:
                # Extract strategy type from response
                if "direct" in strategy_text.lower():
                    strategies.append("Direct")
                elif "distract" in strategy_text.lower():
                    strategies.append("Distraction")
                elif "delegat" in strategy_text.lower():
                    strategies.append("Delegation")
                elif "delay" in strategy_text.lower():
                    strategies.append("Delay")

        if strategies:
            strategy_counts = Counter(strategies)
            return {
                "counts": dict(strategy_counts),
                "percentages": {k: v/len(strategies)*100 for k, v in strategy_counts.items()}
            }
        return {"counts": {}, "percentages": {}}

    def analyze_cultural_relevance(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Analyze cultural relevance feedback"""
        cultural_feedback = []
        for _, row in df.iterrows():
            feedback_text = row.get("cultural_relevance", "")
            if feedback_text:
                cultural_feedback.append(feedback_text)

        # Simple sentiment analysis
        positive_keywords = ["inclusive", "well", "good", "appropriate", "respectful", "diverse", "considered"]
        negative_keywords = ["missing", "lacking", "inadequate", "insensitive", "not", "could", "should"]

        positive_count = 0
        negative_count = 0

        for feedback in cultural_feedback:
            feedback_lower = feedback.lower()
            if any(word in feedback_lower for word in positive_keywords):
                positive_count += 1
            if any(word in feedback_lower for word in negative_keywords):
                negative_count += 1

        return {
            "total_responses": len(cultural_feedback),
            "positive_sentiment": positive_count,
            "concerns_raised": negative_count,
            "sample_feedback": cultural_feedback[:5]
        }

    def analyze_correlations(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Analyze correlations between metrics"""
        rating_cols = ["realistic_rating", "felt_safe_rating", "helpful_feedback_rating",
                      "would_recommend_rating", "confidence_rating"]

        correlation_matrix = df[rating_cols].corr()

        # Find strongest correlations
        correlations = []
        for i, col1 in enumerate(rating_cols):
            for j, col2 in enumerate(rating_cols):
                if i < j:  # Avoid duplicates
                    corr = correlation_matrix.loc[col1, col2]
                    correlations.append({
                        "metric1": col1.replace("_rating", ""),
                        "metric2": col2.replace("_rating", ""),
                        "correlation": corr
                    })

        # Sort by absolute correlation value
        correlations.sort(key=lambda x: abs(x["correlation"]), reverse=True)

        return {
            "correlation_matrix": correlation_matrix.to_dict(),
            "top_correlations": correlations[:5]
        }

    def generate_visualizations(self, df: pd.DataFrame):
        """Generate visualization plots"""
        
        os.makedirs(f"{OUTPUT_DIR}/plots", exist_ok=True)
        
        # Set style
        sns.set_style("whitegrid")
        
        # 1. Character Selection Distribution
        plt.figure(figsize=(10, 6))
        df["character_selected"].value_counts().plot(kind='bar', color='teal')
        plt.title("Character Selection Distribution")
        plt.xlabel("Character")
        plt.ylabel("Count")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(f"{OUTPUT_DIR}/plots/character_selection.png")
        plt.close()
        
        # 2. Skill Development Heatmap
        skill_cols = [f"skill_{skill}" for skill in SKILLS]
        skill_data = df[skill_cols].copy()
        skill_data.columns = SKILLS  # Rename for display
        
        plt.figure(figsize=(10, 8))
        sns.heatmap(skill_data.T, cmap="YlOrRd", annot=False, cbar_kws={'label': 'Skill Level'})
        plt.title("Skill Development Heatmap Across Participants")
        plt.xlabel("Participant")
        plt.ylabel("Skill")
        plt.tight_layout()
        plt.savefig(f"{OUTPUT_DIR}/plots/skill_heatmap.png")
        plt.close()
        
        # 3. User Experience Ratings
        ux_cols = ["realistic_rating", "felt_safe_rating", "helpful_feedback_rating", 
                   "would_recommend_rating", "confidence_rating"]
        ux_means = df[ux_cols].mean()
        ux_means.index = ["Realistic", "Felt Safe", "Helpful Feedback", "Would Recommend", "Confidence"]
        
        plt.figure(figsize=(10, 6))
        ux_means.plot(kind='bar', color='coral')
        plt.title("Average User Experience Ratings (1-5 scale)")
        plt.ylabel("Average Rating")
        plt.ylim(0, 5)
        plt.axhline(y=4, color='green', linestyle='--', label='Target: 4.0')
        plt.legend()
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(f"{OUTPUT_DIR}/plots/ux_ratings.png")
        plt.close()

        # 4. Time Distribution
        plt.figure(figsize=(10, 6))
        plt.hist(df["total_time_min"], bins=10, color='skyblue', edgecolor='black')
        plt.title("Distribution of Time Spent on Training")
        plt.xlabel("Time (minutes)")
        plt.ylabel("Number of Participants")
        plt.axvline(df["total_time_min"].mean(), color='red', linestyle='--', label=f'Mean: {df["total_time_min"].mean():.1f} min')
        plt.legend()
        plt.tight_layout()
        plt.savefig(f"{OUTPUT_DIR}/plots/time_distribution.png")
        plt.close()

        # 5. Skills by Character Selection
        skill_cols = [f"skill_{skill}" for skill in SKILLS]
        char_skill_data = df.groupby("character_selected")[skill_cols].mean()
        char_skill_data.columns = SKILLS

        plt.figure(figsize=(12, 6))
        char_skill_data.T.plot(kind='bar', ax=plt.gca())
        plt.title("Average Skill Development by Character Selection")
        plt.xlabel("Skill")
        plt.ylabel("Average Skill Level")
        plt.legend(title="Character", bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(f"{OUTPUT_DIR}/plots/skills_by_character.png")
        plt.close()

        # 6. Confidence vs Safety Scatter
        plt.figure(figsize=(10, 6))
        plt.scatter(df["felt_safe_rating"], df["confidence_rating"], alpha=0.6, s=100, c='purple')
        plt.title("Relationship Between Safety and Confidence")
        plt.xlabel("Felt Safe Rating")
        plt.ylabel("Confidence in Intervening Rating")
        plt.xlim(0, 6)
        plt.ylim(0, 6)

        # Add trend line
        z = np.polyfit(df["felt_safe_rating"], df["confidence_rating"], 1)
        p = np.poly1d(z)
        plt.plot(df["felt_safe_rating"], p(df["felt_safe_rating"]), "r--", alpha=0.8, label='Trend')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig(f"{OUTPUT_DIR}/plots/safety_vs_confidence.png")
        plt.close()

        # 7. Rating Distribution Box Plot
        rating_cols = ["realistic_rating", "felt_safe_rating", "helpful_feedback_rating",
                      "would_recommend_rating", "confidence_rating"]
        rating_data = df[rating_cols].copy()
        rating_data.columns = ["Realistic", "Felt Safe", "Helpful\nFeedback", "Would\nRecommend", "Confidence"]

        plt.figure(figsize=(12, 6))
        rating_data.boxplot(ax=plt.gca())
        plt.title("Distribution of User Experience Ratings")
        plt.ylabel("Rating (1-5 scale)")
        plt.axhline(y=4, color='green', linestyle='--', alpha=0.5, label='Target: 4.0')
        plt.legend()
        plt.tight_layout()
        plt.savefig(f"{OUTPUT_DIR}/plots/rating_distributions.png")
        plt.close()

        print(f"✓ Saved visualizations to: {OUTPUT_DIR}/plots/")
    
    def generate_report(self, metrics: Dict, ux: Dict, themes: Dict) -> str:
        """Generate markdown analysis report"""
        
        report = f"""# GBV MVP Pilot Test Analysis Report

Generated: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}

---

## Executive Summary

This report presents the analysis of {metrics['total_participants']} simulated users completing the GBV Prevention MVP using TinyTroupe simulation.

### Key Findings:
- ✅ **Completion Rate**: {metrics['completion_rate_pct']:.1f}%
- ✅ **Average Time**: {metrics['avg_total_time_min']:.1f} minutes
- ✅ **User Satisfaction**: {ux['would_recommend']['mean']:.2f}/5.0 would recommend
- ✅ **Safety Rating**: {ux['felt_safe']['mean']:.2f}/5.0 felt safe

---

## 1. Completion & Engagement Metrics

| Metric | Value |
|--------|-------|
| Total Participants | {metrics['total_participants']} |
| Completed All Scenarios | {metrics['completed']} |
| Completion Rate | {metrics['completion_rate_pct']:.1f}% |
| Average Scenarios Completed | {metrics['avg_scenarios_completed']:.1f}/5 |
| Average Total Time | {metrics['avg_total_time_min']:.1f} minutes |
| Average Time Per Scenario | {metrics['avg_time_per_scenario_min']:.1f} minutes |
| Time Range | {metrics['min_time']:.1f} - {metrics['max_time']:.1f} minutes |

**Analysis**: The completion rate of {metrics['completion_rate_pct']:.1f}% {'exceeds' if metrics['completion_rate_pct'] >= 70 else 'is below'} the target threshold of 70%.

---

## 2. User Experience (UES-SF Adapted)

| Dimension | Mean Rating | % Rating 4-5 | Meets Target (≥4.0) |
|-----------|-------------|--------------|---------------------|
| Realistic Scenarios | {ux['realistic']['mean']:.2f} | {ux['realistic']['pct_4_or_5']:.1f}% | {'✅' if ux['realistic']['mean'] >= 4.0 else '⚠️'} |
| Felt Safe & Respected | {ux['felt_safe']['mean']:.2f} | {ux['felt_safe']['pct_4_or_5']:.1f}% | {'✅' if ux['felt_safe']['mean'] >= 4.0 else '⚠️'} |
| Helpful Feedback | {ux['helpful_feedback']['mean']:.2f} | {ux['helpful_feedback']['pct_4_or_5']:.1f}% | {'✅' if ux['helpful_feedback']['mean'] >= 4.0 else '⚠️'} |
| Would Recommend | {ux['would_recommend']['mean']:.2f} | {ux['would_recommend']['pct_4_or_5']:.1f}% | {'✅' if ux['would_recommend']['mean'] >= 4.0 else '⚠️'} |
| Confidence in Intervening | {ux['confidence']['mean']:.2f} | {ux['confidence']['pct_4_or_5']:.1f}% | {'✅' if ux['confidence']['mean'] >= 4.0 else '⚠️'} |

**Key Insight**: The safety rating ({ux['felt_safe']['mean']:.2f}/5.0) is critical for trauma-informed design validation.

---

## 3. Qualitative Feedback Summary

### What Worked Well (Top Themes):

{self._format_theme_list(themes['what_worked'][:5])}

### Areas for Improvement (Top Themes):

{self._format_theme_list(themes['improvements'][:5])}

### Most Valuable Scenarios:

{self._format_theme_list(themes['most_valuable_scenarios'][:5])}

---

## 4. Recommendations for Step 5 (Refinement)

### High Priority:
{self._generate_recommendations(metrics, ux)}

### Additional Considerations:
- Review qualitative feedback for specific pain points
- Consider A/B testing for scenarios with lower engagement
- Expand character options if diversity feedback indicates gaps

---

## 5. Success Criteria Assessment

| Criterion | Target | Actual | Status |
|-----------|--------|--------|--------|
| Completion Rate | ≥70% | {metrics['completion_rate_pct']:.1f}% | {'✅ Pass' if metrics['completion_rate_pct'] >= 70 else '⚠️ Below Target'} |
| Time Spent | 20-30 min | {metrics['avg_total_time_min']:.1f} min | {'✅ Pass' if 20 <= metrics['avg_total_time_min'] <= 30 else '⚠️ Out of Range'} |
| Safety Rating | ≥4.0/5.0 | {ux['felt_safe']['mean']:.2f}/5.0 | {'✅ Pass' if ux['felt_safe']['mean'] >= 4.0 else '⚠️ Below Target'} |
| Would Recommend | ≥75% rate 4-5 | {ux['would_recommend']['pct_4_or_5']:.1f}% | {'✅ Pass' if ux['would_recommend']['pct_4_or_5'] >= 75 else '⚠️ Below Target'} |

---

## Conclusion

{self._generate_conclusion(metrics, ux)}

---

*Data files: `{INTERACTION_CSV}`, `{FEEDBACK_CSV}`*
*Visualizations: `{OUTPUT_DIR}/plots/`*
"""
        
        return report
    
    def _format_theme_list(self, themes: List[str]) -> str:
        """Format theme list for markdown"""
        if not themes:
            return "- No responses collected\n"
        return "\n".join([f"- {theme[:200]}..." if len(theme) > 200 else f"- {theme}" for theme in themes])
    
    def _generate_recommendations(self, metrics: Dict, ux: Dict) -> str:
        """Generate recommendations based on results"""
        recs = []
        
        if metrics['completion_rate_pct'] < 70:
            recs.append("- **Improve completion rate**: Analyze dropout points and simplify navigation")
        
        if ux['felt_safe']['mean'] < 4.0:
            recs.append("- **Enhance safety features**: Review content warnings and add more emotional check-ins")
        
        if ux['realistic']['mean'] < 4.0:
            recs.append("- **Increase scenario realism**: Consult with students to refine scenarios")
        
        if ux['helpful_feedback']['mean'] < 4.0:
            recs.append("- **Improve feedback quality**: Provide more specific, actionable guidance")
        
        if not recs:
            recs.append("- **Maintain current approach**: Metrics meet or exceed all targets")
            recs.append("- **Focus on scaling**: Prepare for broader rollout")
        
        return "\n".join(recs)
    
    def _generate_conclusion(self, metrics: Dict, ux: Dict) -> str:
        """Generate conclusion based on results"""
        
        if metrics['completion_rate_pct'] >= 70 and ux['felt_safe']['mean'] >= 4.0:
            return """The MVP successfully demonstrates trauma-informed gamification principles in action. 
High completion rates and safety ratings validate the design approach. The module is ready for 
refinement based on specific feedback and preparation for broader pilot testing with real users."""
        else:
            return """The MVP shows promise but requires refinement before broader testing. 
Priority should be given to addressing safety concerns and improving completion rates. 
The design principles are sound, but implementation needs adjustment based on user feedback."""
    
    def run_full_analysis(self):
        """Run complete analysis pipeline"""
        
        print("\n" + "="*60)
        print("RUNNING FULL ANALYSIS")
        print("="*60 + "\n")
        
        # 1. Generate data exports
        print("1. Generating data exports...")
        interaction_df = self.generate_interaction_data()
        feedback_df = self.generate_feedback_data()
        
        # 2. Calculate metrics
        print("\n2. Calculating metrics...")
        completion_metrics = self.analyze_completion_metrics(interaction_df)
        character_analysis = self.analyze_character_selection(interaction_df)
        skill_analysis = self.analyze_skill_development(interaction_df)
        decision_patterns = self.analyze_decision_patterns()
        ux_analysis = self.analyze_user_experience(interaction_df)
        strategy_analysis = self.analyze_intervention_strategies(feedback_df)
        cultural_analysis = self.analyze_cultural_relevance(feedback_df)
        correlation_analysis = self.analyze_correlations(interaction_df)

        # 3. Extract themes
        print("\n3. Extracting qualitative themes...")
        themes = self.extract_qualitative_themes(feedback_df)
        
        # 4. Generate visualizations
        print("\n4. Generating visualizations...")
        self.generate_visualizations(interaction_df)
        
        # 5. Generate report
        print("\n5. Generating report...")
        report = self.generate_report(completion_metrics, ux_analysis, themes)
        
        with open(REPORT_FILE, 'w') as f:
            f.write(report)
        
        print(f"✓ Saved report: {REPORT_FILE}")
        
        # 6. Save full analytics
        analytics = {
            "completion_metrics": completion_metrics,
            "character_analysis": character_analysis,
            "skill_analysis": skill_analysis,
            "decision_patterns": decision_patterns,
            "ux_analysis": ux_analysis,
            "strategy_analysis": strategy_analysis,
            "cultural_analysis": cultural_analysis,
            "correlation_analysis": correlation_analysis,
            "qualitative_themes": themes
        }
        
        with open(f"{OUTPUT_DIR}/full_analytics.json", 'w') as f:
            json.dump(analytics, f, indent=2, default=str)
        
        print("\n" + "="*60)
        print("ANALYSIS COMPLETE")
        print("="*60)
        print(f"\nOutputs:")
        print(f"  - Interaction Data: {INTERACTION_CSV}")
        print(f"  - Feedback Data: {FEEDBACK_CSV}")
        print(f"  - Analysis Report: {REPORT_FILE}")
        print(f"  - Visualizations: {OUTPUT_DIR}/plots/")
        print(f"  - Full Analytics: {OUTPUT_DIR}/full_analytics.json")
        
        return analytics

def main():
    """Main execution"""
    analyzer = SimulationAnalyzer()
    analytics = analyzer.run_full_analysis()
    
    # Print quick summary
    print("\n" + "="*60)
    print("QUICK SUMMARY")
    print("="*60)
    print(f"Completion Rate: {analytics['completion_metrics']['completion_rate_pct']:.1f}%")
    print(f"Average Time: {analytics['completion_metrics']['avg_total_time_min']:.1f} minutes")
    print(f"Safety Rating: {analytics['ux_analysis']['felt_safe']['mean']:.2f}/5.0")
    print(f"Would Recommend: {analytics['ux_analysis']['would_recommend']['mean']:.2f}/5.0")

if __name__ == "__main__":
    main()
