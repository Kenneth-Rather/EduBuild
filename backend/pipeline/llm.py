"""
The one place where the pipeline talks to AI models.

Every step calls ask(role, prompt). "role" is the job, like "writer" or "verifier".
Right now this uses a FAKE AI that gives back saved answers, so we can build and
test the whole pipeline for free. Later we swap in the real Claude calls here,
and nothing else in the pipeline has to change.
"""

import json

# Which AI model does each job (our P3 design: one model per role).
MODELS = {
    "writer": "claude-sonnet-5-5",    # writes the questions
    "verifier": "claude-haiku-5-5",   # checks questions against the lesson
    "builder": "claude-sonnet-5-5",   # writes the game code
}

# Turn this off once we have the API key.
USE_FAKE_AI = True


def ask(role, prompt):
    """Send a prompt to the AI model for this role and return its reply as text."""
    if role not in MODELS:
        raise ValueError(f"Unknown role: {role}")

    if USE_FAKE_AI:
        return FAKE_ANSWERS[role]

    raise NotImplementedError("Real AI calls come later, once we have the API key.")


# Fake answers: what a real AI reply would look like.
FAKE_ANSWERS = {
    "writer": json.dumps({
        "questions": [
            {
                "question": "What does water turn into when it freezes?",
                "choices": ["Ice", "Steam", "Sand"],
                "answer": "Ice",
                "source": "When water gets very cold, it freezes into ice.",
            },
            {
                "question": "What does water turn into when it boils?",
                "choices": ["Ice", "Steam", "Mud"],
                "answer": "Steam",
                "source": "When water gets very hot, it boils and turns into steam.",
            },
        ]
    }),
    "verifier": json.dumps({
        "results": [
            {"question_number": 1, "supported": True},
            {"question_number": 2, "supported": True},
        ]
    }),
    "builder": "<!DOCTYPE html><html><body><h1>Fake game</h1></body></html>",
}