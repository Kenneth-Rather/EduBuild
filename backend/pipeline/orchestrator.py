"""
The orchestrator: runs every step of making a game, in order.

Think of it as the head chef. It doesn't do the cooking itself. It hands each
job to the right helper (or AI model), checks the result, and decides what
happens next. Matches our P3 design: Fig 5.1 (the steps in order) and
Fig 5.3 (the build, test, and repair loop).
"""

import json

from pipeline import llm
from pipeline.stages import (
    BUILDING,
    CHECKING,
    DONE,
    FAILED,
    QUEUED,
    READING,
    TESTING,
    WRITING_QUESTIONS,
    can_move,
)

MAX_ATTEMPTS = 3  # how many times the AI gets to try building a working game


def run_pipeline(lesson_text):
    """Turn lesson text into a tested game. Returns a 'run' with the result and history."""
    run = {
        "step": QUEUED,       # the step we are on right now
        "history": [QUEUED],  # every step this run went through, in order
        "attempts": 0,        # how many times the AI has tried to build the game
        "questions": [],
        "game_html": None,
        "error": None,
    }

    # Step 1: read the lesson.
    move_to(run, READING)
    if not lesson_text.strip():
        return fail(run, "The lesson is empty.")

    # Step 2: the writer AI turns the lesson into questions.
    move_to(run, WRITING_QUESTIONS)
    try:
        questions = json.loads(llm.ask("writer", lesson_text))["questions"]
    except (ValueError, KeyError):
        return fail(run, "The writer AI's answer was not in the right format.")

    # Step 3: the verifier AI checks each question against the lesson.
    # Only questions it says are supported by the lesson are kept.
    move_to(run, CHECKING)
    try:
        results = json.loads(llm.ask("verifier", lesson_text))["results"]
    except (ValueError, KeyError):
        return fail(run, "The verifier AI's answer was not in the right format.")
    supported = {r["question_number"] for r in results if r["supported"]}
    run["questions"] = [q for number, q in enumerate(questions, start=1) if number in supported]
    if not run["questions"]:
        return fail(run, "None of the questions matched the lesson.")

    # Steps 4 and 5: the builder AI writes the game, then we play-test it.
    # If the play-test fails, the AI gets the errors and tries again.
    errors = []
    while run["attempts"] < MAX_ATTEMPTS:
        run["attempts"] += 1

        move_to(run, BUILDING)
        prompt = json.dumps(run["questions"])
        if errors:
            prompt += "\nThe last game had these problems. Fix them: " + "; ".join(errors)
        game_html = llm.ask("builder", prompt)

        move_to(run, TESTING)
        passed, errors = play_test(game_html)
        if passed:
            run["game_html"] = game_html
            move_to(run, DONE)
            return run

    return fail(run, f"The game failed its play-test {MAX_ATTEMPTS} times: " + "; ".join(errors))


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


def play_test(game_html):
    """
    Stand-in for the real play-test.

    Later this will use Playwright (a tool that opens the game in a hidden browser
    and plays it). For now it only checks that the AI gave back a web page.
    Returns (passed, list_of_errors).
    """
    if game_html.strip().startswith("<!DOCTYPE html>"):
        return True, []
    return False, ["The game is not a web page."]