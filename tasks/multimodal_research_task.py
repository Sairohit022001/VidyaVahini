from tasks import Task


generate_multimodal_references_task = Task(
    name="GenerateMultimodalReferences",
    description=(
        "Given a topic/chapter or a pdf corresponding to topic and grade level, search for and return references from research papers, video links, and websites "
        "that help in understanding the topic in depth. Tailor recommendations for grades 1-10, 11-12, and undergraduate studies."
        "Ensure resources are credible and relevant, covering academic papers, educational videos, and trusted websites."
    ),
    inputs=["topic", "grade"],
    expected_output=["references"],
    tool="multimodal_research_tool",
    verbose=True,
    output_json=True,
    
)