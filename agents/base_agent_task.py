from abc import ABC, abstractmethod

class BaseAgent(ABC):
    name = "BaseAgent"

    def __init__(self):
        pass

    @abstractmethod
    def process(self, input_data):
        """
        Process method that each agent must implement.
        Args:
            input_data: Input data for the agent to process
        Returns:
            result of processing
        """
        pass

class BaseTask(ABC):
    name = "BaseTask"

    def __init__(self):
        pass

    @abstractmethod
    def run(self, *args, **kwargs):
        """
        Run method that each task must implement.
        """
        pass
