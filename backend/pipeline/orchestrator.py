"""
The orchestrator: runs every step of making a game, in order.

Think of it as the head chef. It doesn't do the cooking itself. It hands each
job to the right helper (or AI model), checks the result, and decides what
happens next. Matches our P3 design (Fig 5.1, the steps in order).

For the P4 prototype, the steps are: read the lesson, write questions, check
them, done. The React trivia template turns the questions into the game.
Building and play-testing the game with AI (P3 Fig 5.3) come in CS 426.
"""

import json

from pipeline import llm
from pipeline.prompts import VERIFIER_PROMPT, WRITER_PROMPT
from pipeline.stages import (
    CHECKING,
    DONE,
    FAILED,
    QUEUED,
    READING,
    WRITING_QUESTIONS,
    can_move,
)


def run_pipeline(lesson_text, grade="3", difficulty="Easy", num_questions=2):
    """Turn lesson text into checked trivia questions. Returns a 'run' with the result and history."""
    run = {
        "step": QUEUED,       # the step we are on right now
        "history": [QUEUED],  # every step this run went through, in order
        "questions": [],
        "error": None,
    }

    # Step 1: read the lesson.
    move_to(run, READING)
    if not lesson_text.strip():
        return fail(run, "The lesson is empty.")

    # Step 2: the writer AI turns the lesson into questions.
    move_to(run, WRITING_QUESTIONS)
    prompt = WRITER_PROMPT.format(
        lesson=lesson_text, grade=grade, difficulty=difficulty, num_questions=num_questions
    )
    try:
        questions = json.loads(llm.ask("writer", prompt))["questions"]
    except (ValueError, KeyError, TypeError):
        return fail(run, "The writer AI's answer was not in the right format.")
    if not questions or not all(is_good_question(q) for q in questions):
        return fail(run, "The writer AI's questions were missing parts.")

    # Step 3: the verifier AI checks each question against the lesson.
    # Only questions it says are supported by the lesson are kept.
    move_to(run, CHECKING)
    numbered = "\n".join(f"{n}. {json.dumps(q)}" for n, q in enumerate(questions, start=1))
    prompt = VERIFIER_PROMPT.format(lesson=lesson_text, questions=numbered)
    try:
        results = json.loads(llm.ask("verifier", prompt))["results"]
        supported = {r["question_number"] for r in results if r["supported"]}
    except (ValueError, KeyError, TypeError):
        return fail(run, "The verifier AI's answer was not in the right format.")
    run["questions"] = [q for n, q in enumerate(questions, start=1) if n in supported]
    if not run["questions"]:
        return fail(run, "None of the questions matched the lesson.")

    move_to(run, DONE)
    return run


def is_good_question(q):
    """A question needs all four parts, and its answer must be one of its choices."""
    parts = ("question", "choices", "answer", "source")
    return isinstance(q, dict) and all(q.get(p) for p in parts) and q["answer"] in q["choices"]


def move_to(run, next_step):
    """Move the run to its next step, but only if stages.py says that move is allowed."""
    if not can_move(run["step"], next_step):
        raise ValueError(f"Not allowed to go from {run['step']} to {next_step}")
    run["step"] = next_step
    run["history"].append(next_step)


def fail(run, message):
    """Stop the run, mark it FAILED, and save the reason."""
    run["error"] = message
    move_to(run, FAILED)
    return run