"""
Session service layer.

A session represents one uploaded class recording tied to a course.
"""

from typing import Optional

SESSIONS = []
NEXT_SESSION_ID = 1


def create_session_record(
    title: str,
    filename: str,
    recording_path: str,
    status: str,
    course_id: int
) -> dict:
    """
    Create a session record tied to a course.
    """
    global NEXT_SESSION_ID

    session = {
        "id": NEXT_SESSION_ID,
        "title": title,
        "filename": filename,
        "recording_path": recording_path,
        "status": status,
        "course_id": course_id
    }

    SESSIONS.append(session)
    NEXT_SESSION_ID += 1
    return session


def fetch_all_sessions() -> list[dict]:
    """
    Return all sessions.
    """
    return SESSIONS


def fetch_one_session(session_id: int) -> Optional[dict]:
    """
    Return one session by ID.
    """
    return next((session for session in SESSIONS if session["id"] == session_id), None)


def fetch_sessions_for_course(course_id: int) -> list[dict]:
    """
    Return all sessions for one course.
    """
    return [session for session in SESSIONS if session["course_id"] == course_id]


def update_session_status(session_id: int, new_status: str) -> None:
    """
    Update the status of a session.
    """
    session = fetch_one_session(session_id)
    if session:
        session["status"] = new_status