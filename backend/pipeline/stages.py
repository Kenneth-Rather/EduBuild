"""
Developed by Kenneth Rather (EduBuild team) for CS 425 Project Part 4.

The steps a game generation goes through, and which step can come next.
Matches the game generation state diagram in our P3 design (Fig 5.2).
"""

QUEUED = "queued"
READING = "reading_lesson"
WRITING_QUESTIONS = "writing_questions"
CHECKING = "checking_accuracy"
BUILDING = "building_game"
TESTING = "testing_game"
DONE = "done"
FAILED = "failed"

# For each step, the steps it is allowed to move to next.
ALLOWED_MOVES = {
    QUEUED: [READING, FAILED],
    READING: [WRITING_QUESTIONS, FAILED],
    WRITING_QUESTIONS: [CHECKING, FAILED],
    CHECKING: [BUILDING, DONE, FAILED],  # prototype: stops after checking (DONE)
    BUILDING: [TESTING, FAILED],
    TESTING: [DONE, BUILDING, FAILED],  # back to BUILDING = the AI repairs the game
    DONE: [],                           # finished, nothing comes after
    FAILED: [],                         # gave up, nothing comes after
}


def can_move(current_step, next_step):
    """Return True if the pipeline is allowed to go from current_step to next_step."""
    return next_step in ALLOWED_MOVES[current_step]