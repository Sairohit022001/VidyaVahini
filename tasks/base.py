from typing import List, Optional, Any, Dict

class BaseTask:
    def __init__(
        self,
        name: str,
        description: str,
        steps: Optional[List[Any]] = None,
        expected_output: Optional[Any] = None,
        tools: Optional[List[Any]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        output_json: bool = False,
        context_injection: bool = False,
        verbose: bool = False,
        output_file: Optional[str] = None,
        guardrails: Optional[Dict[str, Any]] = None
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
