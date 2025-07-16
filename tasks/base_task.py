class Task:
    def __init__(
        self,
        name: str,
        description: str,
        steps: list = None,
        expected_output=None,
        tools: list = None,
        metadata: dict = None,
        output_json: bool = False,
        context_injection: bool = False,
        verbose: bool = False,
        output_file: str = None,
        guardrails: dict = None
    ):
        self.name = name
        self.description = description
        self.steps = steps or []
        self.expected_output = expected_output
        self.tools = tools or []
        self.metadata = metadata or {}
        self.output_json = output_json
        self.context_injection = context_injection
        self.verbose = verbose
        self.output_file = output_file
        self.guardrails = guardrails or {}
