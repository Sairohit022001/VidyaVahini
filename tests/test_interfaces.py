import pytest
import inspect
from typing import get_origin, get_args

# Import your task and tool classes here
from tasks.base import BaseTask
from tasks.lesson_planner_tasks import LessonPlannerTask # Assuming you have a class for this now
from tasks.story_teller_tasks import StoryTellerTask
from tasks.quiz_tasks import QuizTask
# from tasks.gamification_tasks import GamificationTask # Uncomment if you create a class for this
from tasks.multimodal_research_task import MultimodalResearchTask
from tasks.predictive_analytics_task import PredictiveAnalyticsTask
from tasks.visual_generation_task import VisualGenerationTask
# Import your tool classes here
from tools.lesson_generation_tool import LessonGenerationTool
from tools.story_generation_tool import StoryGenerationTool
from tools.quiz_generation_tool import QuizGenerationTool
from tools.multimodal_research_tool import MultimodalResearchTool
from tools.predictive_analytics_tool import PredictiveAnalyticsTool
from tools.visual_generation_tool import VisualGenerationTool
from tools.voice_tutor_tool import VoiceTutorTool # Assuming you have a class for this
# from tools.gamification_tool import GamificationTool # Uncomment if you create a class for this

# List of task classes to test
task_classes = [
    LessonPlannerTask,
    StoryTellerTask,
    QuizTask,
    # GamificationTask, # Uncomment if you create a class for this
    MultimodalResearchTask,
    PredictiveAnalyticsTask,
    VisualGenerationTask,
]

# List of tool classes to test (only those with a 'run' or similar primary method)
tool_classes_with_run = [
    LessonGenerationTool,
    StoryGenerationTool,
    QuizGenerationTool,
    MultimodalResearchTool,
    PredictiveAnalyticsTool,
    VisualGenerationTool,
    VoiceTutorTool, # Assuming VoiceTutorTool has a 'run' or similar method
    # GamificationTool, # Uncomment if you create a class for this
]

# --- Test for Task Classes ---

@pytest.mark.parametrize("task_class", task_classes)
def test_task_has_async_run_method(task_class):
    """Tests that each task class has an async run method."""
    assert hasattr(task_class, "run"), f"Task class {task_class.__name__} is missing 'run' method"
    assert (inspect.isfunction(task_class.run) or inspect.ismethod(task_class.run)), 
        (f"Task class {task_class.__name__}'s 'run' is not a function or method")
    assert inspect.iscoroutinefunction(task_class.run), f"Task class {task_class.__name__}'s 'run' method is not async"

# --- Test for Tool Classes ---

# Note: Tool classes might have different primary methods (e.e., 'run', 'generate', 'process')
# This test assumes a 'run' method, adjust if your tools use different names.
@pytest.mark.parametrize("tool_class", tool_classes_with_run)
def test_tool_has_run_method(tool_class):
    """Tests that each tool class has a run or similar primary method."""
    # This test just checks for existence, not async nature,
    # as tools might have sync methods calling external async APIs.
    assert hasattr(tool_class, "run"), f"Tool class {tool_class.__name__} is missing 'run' method"
    assert (inspect.isfunction(tool_class.run) or inspect.ismethod(tool_class.run)), 
        (f"Tool class {tool_class.__name__}'s 'run' is not a function or method")

# Example of how you might test for specific async methods in tools if needed:
# @pytest.mark.parametrize("tool_class", [VoiceTutorTool]) # Example: only test VoiceTutorTool here
# def test_async_tool_methods(tool_class):
#     """Tests specific methods in tool classes that are expected to be async."""
#     # Adjust this based on the actual async methods in your tools
#     async_methods_to_check = {
#         VoiceTutorTool: ['generate_voice_tutor'], # Example async method name
#         # Add other tool classes and their async method names
#     }
#     if tool_class in async_methods_to_check:
#         for method_name in async_methods_to_check[tool_class]:
#             assert hasattr(tool_class, method_name),
#                 f"Tool class {tool_class.__name__} is missing async method '{method_name}'"
#             method = getattr(tool_class, method_name)
#             assert inspect.isfunction(method) or inspect.ismethod(method),
#                 f"Method {tool_class.__name__}.{method_name} is not a function or method"
#             assert inspect.iscoroutinefunction(method),
#                 f"Method {tool_class.__name__}.{method_name} is not async"

# You would need to create fixtures for tool instances if testing instance methods
# @pytest.fixture
# def voice_tutor_tool_instance():
#     return VoiceTutorTool()

# Add more specific tests for tool methods as needed based on your tool implementations.

# Example test for checking return types (requires more detailed schema handling)
# @pytest.mark.parametrize("task_class", task_classes)
# def test_task_run_returns_expected_type(task_class):
#     """Tests that task run methods are annotated to return a dictionary or Pydantic model."""
#     # This is a basic check and might need refinement based on your actual return types.
#     return_annotation = inspect.getfullargspec(task_class.run).annotations.get('return')
#     assert return_annotation is not inspect.Signature.empty,
#         f"Task class {task_class.__name__}'s run method is missing return type annotation"
#     # More sophisticated checks for Dict or Pydantic models would be needed here
#     # For example, checking if the return annotation is typing.Dict or a subclass of BaseModel
