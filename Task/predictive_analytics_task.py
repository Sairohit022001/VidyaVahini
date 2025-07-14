from crewai import Task

generate_class_analytics_task = Task(
    name="GenerateClassAnalytics",
    description="Analyze quiz results and generate class-level analytics for each quiz including average score, top performers" \
    ", weak areas, and recommendations for each student and also help in planning future lessons.Provide" \
    "analysis for each quiz for each student and overall class performance." \
    "Compare performance across different quizzes and identify trends. and suggest the chapters that should " \
    "be focused and also sometimes  help in identifying the concepts that" \
    "should be reexplained",
    inputs=["quiz_results"],
    outputs=["average_score", "top_performers", "weak_areas", "recommendations"],
    tool="predictive_analytics_tool"
)