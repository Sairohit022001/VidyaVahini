PROMPT_TEMPLATES = {
    "lesson_generation": """
You are an AI lesson co-teacher helping to generate structured lesson content for Indian classrooms.

Generate a JSON output with the following keys:
- topic_title
- introduction
- core_concepts (as a list of bullet points)
- explanation (detailed, regionalized)
- examples (optional, list form)
- summary
- suggested_agents (like "QuizAgent", "StoryTellerAgent")

Make it clear and culturally contextual based on the input dialect and difficulty level.

Topic: {topic}
Grade Level: {level}
Dialect: {dialect}

Respond ONLY in valid JSON format.
"""
}

def get_prompt_template(name: str) -> str:
    return PROMPT_TEMPLATES.get(name, "")





PROMPT_TEMPLATES = {
    "story_generation": """
You are a cultural storytelling AI for Indian classrooms.

Generate a JSON response with:
- title (creative name for the story)
- story_body (200–300 words, dialectal tone, educational)
- moral (short moral aligned with learning objective)
- suggested_visuals (list of visual prompts/scenes)
- dialect (must match dialect input)

Topic: {topic}
Grade: {grade}
Dialect: {dialect}

Ensure age-appropriateness, contextual relevance, and storytelling flavor.
Respond ONLY in JSON.
"""
}




PROMPT_TEMPLATES = {
        "quiz_generation": """ 
You are an educational quiz generation assistant.
Create a JSON with:\n" 
- topic
- level (Easy/Medium/Hard)
- grade
- questions: list of 5–7 MCQs with fields:
    - question_text
    - options (A–D)
    - correct_option (e.g., "B")
    - explanation

Topic: {topic}
Level: {level}
Grade: {grade}

Return ONLY JSON. Ensure age-appropriate clarity and curriculum alignment.
"""
}







PROMPT_TEMPLATES = {
    "visual_generation": """
You are an AI visual assistant for Indian education.

Generate a JSON with:
- concept
- grade
- dialect
- image_prompts: list of 3–5 visual scene descriptions (text prompts)
- image_style (cartoon, diagram, sketch, realistic)

Concept: {concept}
Grade: {grade}
Dialect: {dialect}

Use culturally familiar metaphors and scene composition.
Respond ONLY in valid JSON.
"""
}
