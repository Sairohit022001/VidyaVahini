# VidyaVahini/base/agent_base.py

class BaseAgent:
    def __init__(self, name: str, goal: str = ""):
        self.name = name
        self.goal = goal

    def run(self, *args, **kwargs):
        raise NotImplementedError("Subclasses must implement this method.")
