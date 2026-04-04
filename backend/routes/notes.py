"""
Notes routes.

These routes return generated notes for a session.

Notes represent processed learning content derived from a recording,
such as a summary, key topics, and action items. This route allows
the frontend to retrieve that structured output once it becomes
available.
"""

from flask import Blueprint

from utils.responses import success_response, error_response
from services.session_service import fetch_one_session
from services.note_service import fetch_notes_by_session_id

notes_bp = Blueprint("notes", __name__)


@notes_bp.route("/session/<int:session_id>", methods=["GET"])
def get_notes(session_id: int):
    """
    Return generated notes for a single session.

    The route first confirms that the session exists, then checks
    whether notes have been generated for it.

    If notes are not available yet, it still returns a safe response
    so the frontend can show an empty or pending state rather than
    failing.
    """
    session = fetch_one_session(session_id)
    if not session:
        return error_response("Session not found", 404)

    notes = fetch_notes_by_session_id(session_id)

    if not notes:
        return success_response("Notes not generated yet", None)

    return success_response("Notes retrieved successfully", notes)