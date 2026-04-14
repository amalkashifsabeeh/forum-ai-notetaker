"""
Transcript routes.

These routes return transcript data for a session.

A transcript is course-related learning content, so this route should
eventually follow the same access-control model as notes and sessions.
For now, it returns transcript state safely so the frontend can render
either the transcript itself or an empty/loading state.
"""

from flask import Blueprint

from utils.responses import success_response, error_response
from services.session_service import fetch_one_session
from services.transcript_service import fetch_transcript_by_session_id

transcripts_bp = Blueprint("transcripts", __name__)


@transcripts_bp.route("/<int:session_id>", methods=["GET"])
def get_transcript(session_id: int):
    """
    Return the transcript for a single session.

    This route first checks that the session exists, then attempts
    to retrieve the transcript associated with it.

    If the transcript has not been generated yet, the route still
    returns a safe response so the frontend can show a loading or
    empty state instead of breaking.
    """
    session = fetch_one_session(session_id)
    if not session:
        return error_response("Session not found", 404)

    transcript = fetch_transcript_by_session_id(session_id)

    if not transcript:
        return success_response("Transcript not ready yet", None)

    return success_response("Transcript retrieved successfully", transcript)