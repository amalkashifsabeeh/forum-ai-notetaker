"""
Note service layer.

This module stores and retrieves generated notes associated with
sessions.

For now, notes are kept in memory so the backend flow can be tested
before full database integration. The route layer can still rely on
a stable interface while the persistence layer evolves later.
"""

from typing import Optional


# In-memory store:
# key   -> session_id
# value -> notes object
NOTES: dict[int, dict] = {}


def save_notes(session_id: int, summary: str, topics: list[str], action_items: list[str]) -> None:
    """
    Save or overwrite generated notes for a session.

    This function is typically called after the transcript has been
    processed into a more structured summary.

    Args:
        session_id: The session these notes belong to.
        summary: A concise summary of the session.
        topics: A list of key topics covered.
        action_items: A list of extracted action items.
    """
    NOTES[session_id] = {
        "session_id": session_id,
        "summary": summary,
        "topics": topics,
        "action_items": action_items,
    }


def fetch_notes_by_session_id(session_id: int) -> Optional[dict]:
    """
    Retrieve the notes for a given session.

    If notes have not been generated yet, this returns None.
    The route layer can use that to show a pending or empty state.

    Args:
        session_id: The session being requested.

    Returns:
        The notes object if it exists, otherwise None.
    """
    return NOTES.get(session_id)