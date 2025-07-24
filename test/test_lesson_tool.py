# test_lesson_tool.py
from tools.lesson_generation_tool import lesson_tool

inputs = {
    "topic": "Photosynthesis",
    "level": "Medium",
    "dialect": "andhra",
    "context_from_doc": {}
}

output = lesson_tool.run(inputs)
print("Generated lesson output:\n", output)
