from abc import ABC, abstractmethod
from crewflows import Agent

class CrewBaseAgent(Agent, ABC):
    """
    Base class for all crewflows Agents in VidyaVāhinī.
    Handles required 'goal' parameter and enforces process() implementation.
    """

    def __init__(self, *args, goal=None, **kwargs):
        if goal is None:
            raise ValueError(f"Missing required 'goal' argument for {self.__class__.__name__}")
        super().__init__(*args, goal=goal, **kwargs)

    @abstractmethod
    async def process(self, inputs: dict) -> dict:
        """
        Abstract process method that all agents must implement.

        Args:
            inputs (dict): Input data for the agent.

        Returns:
            dict: Result of agent processing.
        """
        pass

class BaseTask(ABC):
    """
    Abstract base class for all task classes used by agents.
    """

    @abstractmethod
    async def run(self, *args, **kwargs) -> dict:
        """
        Abstract run method to be implemented by task classes.

        Returns:
            dict: Task execution result.
        """
        pass
