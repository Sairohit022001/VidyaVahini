class Task:
    def __init__(
        self,
        name: str,
        description: str,
        agent=None,  # optional, to avoid circular import
        tool=None,
        inputs=None,
        expected_output=None,
        output_json=False,
        context_injection=False,
        verbose=False,
        output_file=None,
        guardrails=None,
        metadata=None,
    ):
        self.name = name
        self.description = description
        self.agent = agent
        self.tool = tool
        self.inputs = inputs or []
        self.expected_output = expected_output
        self.output_json = output_json
        self.context_injection = context_injection
        self.verbose = verbose
        self.output_file = output_file
        self.guardrails = guardrails or {}
        self.metadata = metadata or {}

    def set_agent(self, agent):
        self.agent = agent

    # Add other methods like run(), validate(), etc. if needed
