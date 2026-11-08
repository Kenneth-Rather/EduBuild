"""HTTP views for the EduBuild game-generation flow."""

import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .services import generate_trivia_questions


def _read_text(request):
    """Find lesson text in the incoming HTTP request.

    React can send JSON, a multipart ``.txt`` upload, or a regular form field.
    This helper checks those formats and returns ``(text, error_message)``.
    """
    if request.content_type.startswith("application/json"):
        try:
            payload = json.loads(request.body)
        except json.JSONDecodeError:
            return None, "Request body must contain valid JSON."
        if not isinstance(payload, dict):
            return None, "JSON body must be an object."
        return payload.get("text"), None

    if request.FILES:
        uploaded_file = next(iter(request.FILES.values()))
        if not uploaded_file.name.lower().endswith(".txt"):
            return None, "Uploaded files must use the .txt extension."
        try:
            return uploaded_file.read().decode("utf-8"), None
        except UnicodeDecodeError:
            return None, "Uploaded text files must use UTF-8 encoding."

    return request.POST.get("text"), None


@csrf_exempt
def generate_game(request):
    """Receive lesson content and return generated questions as JSON.

    The endpoint accepts only POST requests, validates the incoming content,
    calls the question-generation service, and sends the result to React.
    """
    if request.method != "POST":
        return JsonResponse(
            {"status": "error", "message": "Only POST requests are supported."},
            status=405,
        )

    uploaded_text, error = _read_text(request)
    if error:
        return JsonResponse({"status": "error", "message": error}, status=400)
    if not isinstance(uploaded_text, str) or not uploaded_text.strip():
        return JsonResponse(
            {"status": "error", "message": "Provide lesson text or a .txt file."},
            status=400,
        )

    return JsonResponse(
        {
            "status": "success",
            "questions": generate_trivia_questions(uploaded_text),
        }
    )
