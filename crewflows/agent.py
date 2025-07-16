# crewflows/agent.py

class Agent:
    def __init__(self, name, role, goal, **kwargs):
        self.name = name
        self.role = role
        self.goal = goal
        # Initialize other attributes as needed
        # Store kwargs or process tools, tasks, memory etc.

    def add_input(self, input_name):
        # store accepted inputs
        pass

    def add_output(self, output_name):
        # store expected outputs
        pass

    async def run(self, *args, **kwargs):
        # agent execution logic here
        pass
