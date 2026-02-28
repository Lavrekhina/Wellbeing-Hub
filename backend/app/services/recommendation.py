from typing import List


def generate_recommendations(risk_level: str) -> List[dict]:
    if risk_level == "high":
        return [
            {"category": "support", "recommendation_text": "Schedule a 1:1 wellbeing check-in with your manager this week."},
            {"category": "workload", "recommendation_text": "Review and reduce high-priority workload for the next sprint."},
            {"category": "wellbeing", "recommendation_text": "Use guided stress management resources for 15 minutes daily."},
        ]

    if risk_level == "medium":
        return [
            {"category": "routine", "recommendation_text": "Plan short recovery breaks between focused work sessions."},
            {"category": "wellbeing", "recommendation_text": "Try one mindfulness exercise during your workday."},
            {"category": "support", "recommendation_text": "Discuss current stressors in your next manager check-in."},
        ]

    return [
        {"category": "maintenance", "recommendation_text": "Keep your current work routine and wellbeing habits."},
        {"category": "wellbeing", "recommendation_text": "Continue weekly check-ins to track trend changes early."},
    ]
