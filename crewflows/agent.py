class Agent:
    def __init__(self, name, role, goal, **kwargs):
        # Store the name privately
        self._name = name
        self.role = role
        self.goal = goal
        # Initialize other attributes as needed (tools, tasks, memory)
        # You may want to store kwargs details here, e.g.,
        self.tools = kwargs.get("tools", [])
        self.tasks = kwargs.get("tasks", [])
        self.memory = kwargs.get("memory", False)
        self.memory_handler = kwargs.get("memory_handler", None)
        self.allow_delegation = kwargs.get("allow_delegation", False)
        self.verbose = kwargs.get("verbose", False)
        self.llm = kwargs.get("llm", None)
        self.user_type = kwargs.get("user_type", "teacher")
        # etc.

    @property
    def name(self):
        return self._name

    def add_input(self, input_name):
        # TODO: implement storing accepted inputs
        pass

    def add_output(self, output_name):
        # TODO: implement storing expected outputs
        pass

    async def run(self, *args, **kwargs):
        # TODO: implement agent execution logic
        pass
