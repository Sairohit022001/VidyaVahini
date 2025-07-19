# tools/base.py

class BaseTool:
    """
    Base class for all tools in the VidyaVāhinī project.
    Provides a common interface and shared functionality.
    """

    def __init__(self, name: str = "UnnamedTool"):
        self.name = name

    def run(self, inputs: dict) -> dict:
        """
        Override this method in subclasses to implement tool functionality.

        Args:
            inputs (dict): Input data for the tool.

        Returns:
            dict: Output data after tool execution.
        """
        raise NotImplementedError(f"{self.__class__.__name__}.run() not implemented.")

    def validate_inputs(self, inputs: dict) -> bool:
        """
        Optionally validate inputs before running the tool.

        Args:
            inputs (dict): Input data.

        Returns:
            bool: True if inputs are valid, False otherwise.
        """
        return True

    def __repr__(self):
        return f"<Tool name={self.name}>"
