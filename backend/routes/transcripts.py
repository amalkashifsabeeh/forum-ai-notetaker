"""
Transcript routes.

These routes return transcript data for a session.

A transcript is course-scoped content, so access should be limited
to users who belong to the course that owns the session. This keeps
the transcript flow consistent with the notes flow and prevents users
from accessing course material they are not part of.
"""

from flask import Blueprint, g

from middleware.auth import auth_required
from utils.responses import success_response, error_response
from services.session_service import fetch_one_session
from services.transcript_service import fetch_transcript_by_session_id
from services.course_service import is_course_member

transcripts_bp = Blueprint("transcripts", __name__)


@transcripts_bp.route("/<int:session_id>", methods=["GET"])
@auth_required
def get_transcript(session_id: int):
    """
    Return the transcript for one session if the user is authorized.

    The route first checks that the session exists, then verifies that
    the authenticated user belongs to the course attached to that
    session. If the transcript has not been generated yet, it still
    returns a safe response so the frontend can show an empty or
    loading state instead of failing.
    """
    session = fetch_one_session(session_id)
    if not session:
        return error_response("Session not found", 404)

    if not is_course_member(session["course_id"], g.user["id"]):
        return error_response("You do not have access to this transcript", 403)

    transcript = fetch_transcript_by_session_id(session_id)

    if not transcript:
        return success_response("Transcript not ready yet", None)

    return success_response("Transcript retrieved successfully", transcript)