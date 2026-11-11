"""
Developed by Kenneth Rather (EduBuild team) for CS 425 Project Part 4.

Try the whole pipeline with the REAL AI on a lesson file.

How to run (from the backend folder):
    python try_pipeline.py sample_lesson.txt

Each run costs less than a cent. The answer prints in the terminal.
"""

import json
import sys

from pipeline.orchestrator import run_pipeline

lesson = open(sys.argv[1], encoding="utf-8").read()
run = run_pipeline(lesson)
print(json.dumps(run, indent=2))