"""Business logic for turning uploaded lesson text into trivia questions.

This connects Django to the AI pipeline (the orchestrator in backend/pipeline).
"""

from pipeline.orchestrator import run_pipeline


def generate_trivia_questions(text, grade="3", difficulty="Easy"):
    """Run the AI pipeline on the lesson text.

    Returns (questions, error). On success, error is None. If the pipeline
    fails (for example, the AI's answer was in the wrong format), questions
    is an empty list and error explains what went wrong.
    """
    run = run_pipeline(text, grade=grade, difficulty=difficulty)
    return run["questions"], run["error"]