# test/test_lesson_planner.py

import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tools.lesson_generation_tool import LessonGenerationTool

def test_lesson_generation():
    tool = LessonGenerationTool()
    inputs = {
        "topic": "Photosynthesis",
        "level": "Medium",
        "dialect": "Telangana Telugu"
    }
    print("📌 Inputs received:", inputs)
    output = tool.run(inputs)
    print("🔍 Final Output:")
    print(output)

if __name__ == "__main__":
    test_lesson_generation()
