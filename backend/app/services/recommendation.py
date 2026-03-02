from typing import List


def generate_recommendations(risk_level: str) -> List[dict]:
    """
    Generate personalized recommendations based on calculated risk level.

    Args:
        risk_level (str): One of "low", "medium", or "high".

    Returns:
        List[dict]: A list of recommendation objects containing:
            - category (str): Area of focus (e.g., wellbeing, support, workload)
            - recommendation_text (str): Actionable guidance text
    """

    # High risk: Immediate intervention and workload adjustment
    if risk_level == "high":
        return [
            {
                "category": "support",
                "recommendation_text": "Schedule a 1:1 wellbeing check-in with your manager this week.",
            },
            {
                "category": "workload",
                "recommendation_text": "Review and reduce high-priority workload for the next sprint.",
            },
            {
                "category": "wellbeing",
                "recommendation_text": "Use guided stress management resources for 15 minutes daily.",
            },
        ]

    # Medium risk: Prevent escalation and improve daily resilience
    if risk_level == "medium":
        return [
            {
                "category": "routine",
                "recommendation_text": "Plan short recovery breaks between focused work sessions.",
            },
            {
                "category": "wellbeing",
                "recommendation_text": "Try one mindfulness exercise during your workday.",
            },
            {
                "category": "support",
                "recommendation_text": "Discuss current stressors in your next manager check-in.",
            },
        ]

    # Default (low risk): Maintain healthy habits and monitor trends
    return [
        {
            "category": "maintenance",
            "recommendation_text": "Keep your current work routine and wellbeing habits.",
        },
        {
            "category": "wellbeing",
            "recommendation_text": "Continue weekly check-ins to track trend changes early.",
        },
    ]