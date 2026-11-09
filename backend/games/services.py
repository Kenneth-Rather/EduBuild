"""Business logic for turning uploaded lesson text into demo questions."""


def generate_trivia_questions(text):
    """Create the two demo questions returned to the frontend.

    The function receives the lesson text, creates a short preview for the
    first answer, and returns a Python list that Django converts to JSON.
    This is the placeholder where a future Claude API call can be added.
    """
    preview = " ".join(text.split())[:100]
    return [
        {
            "question": "What topic was included in the uploaded lesson?",
            "answer": preview or "No lesson text was provided.",
        },
        {
            "question": "Was the lesson processed by the EduBuild backend?",
            "answer": "Yes",
        },
    ]
