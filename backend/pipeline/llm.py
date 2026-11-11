"""
Developed by Kenneth Rather (EduBuild team) for CS 425 Project Part 4.

The one place where the pipeline talks to AI models.

Every step calls ask(role, prompt). "role" is the job: "writer" writes the
questions and "verifier" checks them. Each job uses its own Claude model, key,
and effort level, all read from the private backend/.env file.

Tests always use the FAKE AI (saved answers), so they are free and repeatable.
"""

import json
import os
from pathlib import Path

import anthropic
from dotenv import load_dotenv

# Load the settings from backend/.env. Keys never go in the code or on GitHub.
load_dotenv(Path(__file__).resolve().parent.parent / ".env")

# For each job: the names of the .env settings that hold its model, key, and effort.
ROLES = {
    "writer": {  # writes the questions
        "model": "SONNET_MODEL",
        "key": "ANTHROPIC_API_KEY_SONNET",
        "effort": "SONNET_EFFORT_DEFAULT",
    },
    "verifier": {  # checks the questions against the lesson
        "model": "HAIKU_MODEL",
        "key": "ANTHROPIC_API_KEY_HAIKU",
        "effort": "HAIKU_EFFORT",
    },
}

# True = use the saved fake answers instead of calling Claude.
# Add USE_FAKE_AI=true to your .env to work without spending money.
USE_FAKE_AI = os.getenv("USE_FAKE_AI", "false").lower() == "true"


def ask(role, prompt):
    """Send a prompt to the AI model for this role and return its reply as text."""
    if role not in ROLES:
        raise ValueError(f"Unknown role: {role}")

    if USE_FAKE_AI:
        return FAKE_ANSWERS[role]

    settings = ROLES[role]
    try:
        client = anthropic.Anthropic(api_key=os.getenv(settings["key"]))
        response = client.messages.create(
            model=os.getenv(settings["model"]),
            max_tokens=4000,
            messages=[{"role": "user", "content": prompt}],
            output_config={"effort": os.getenv(settings["effort"], "medium")},
        )
    except anthropic.APIError as error:
        print(f"AI request failed ({role}): {error}")  # shows the real reason in the terminal
        raise ValueError("Could not get an answer from the AI.") from error

    text = "".join(block.text for block in response.content if block.type == "text")
    return just_the_json(text)


def just_the_json(text):
    """AI models sometimes wrap their JSON in extra words or ``` marks. Keep only the JSON part."""
    start, end = text.find("{"), text.rfind("}")
    return text[start:end + 1] if start != -1 and end != -1 else text


# Fake answers: what a real AI reply looks like.
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
}