import os
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
""",

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
""",

    "quiz_generation": """
You are an educational quiz generation assistant.
Create a JSON with:
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
""",

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
""",

    "content_creation": """
You're an AI assistant helping teachers combine their handwritten or typed notes with AI-generated content.

Generate a JSON with:
- title
- combined_lesson (structured content combining both sources)
- teacher_notes_used (list of quotes or extracted lines from original notes)

Use dialect, grade level, and topic to control tone and vocabulary.
Input:
- Topic: {topic}
- Grade: {grade}
- Dialect: {dialect}
- Notes: {teacher_notes}

Ensure content is original, complete, culturally contextual, and markdown-compatible.
Return ONLY JSON.
"""
}

def get_prompt_template(name: str) -> str:
    """
    Returns the prompt template string for the given prompt name
    from the PROMPT_TEMPLATES dictionary.
    """
    return PROMPT_TEMPLATES.get(name, "")



PROMPT_DIR = os.path.join(os.path.dirname(__file__), '../prompts')

def load_prompt(filename: str) -> str:
    path = os.path.abspath(os.path.join(PROMPT_DIR, filename))
    if not os.path.exists(path):
        raise FileNotFoundError(f"Prompt file not found: {path}")
    with open(path, 'r', encoding='utf-8') as f:
        return f.read().strip()

