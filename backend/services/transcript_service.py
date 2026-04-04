"""
Transcript service layer.

This module stores and retrieves transcript data associated with
sessions.

For MVP development, transcripts are stored in memory so the route
layer can be tested independently of the database. The interface is
designed to remain stable when real persistence is added later.
"""

from typing import Optional


# In-memory store:
# key   -> session_id
# value -> transcript object
TRANSCRIPTS: dict[int, dict] = {}


def save_transcript(session_id: int, transcript_text: str) -> None:
    """
    Save or overwrite the transcript for a session.

    This function is typically called by the processing pipeline
    after transcription is completed.

    Args:
        session_id: The session this transcript belongs to.
        transcript_text: The full transcript text.
    """
    TRANSCRIPTS[session_id] = {
        "session_id": session_id,
        "text": transcript_text,
    }


def fetch_transcript_by_session_id(session_id: int) -> Optional[dict]:
    """
    Retrieve the transcript for a given session.

    If the transcript has not been generated yet, this returns None.
    The route layer can use that to show a loading or empty state
    instead of failing.

    Args:
        session_id: The session being requested.

    Returns:
        The transcript object if it exists, otherwise None.
    """
    return TRANSCRIPTS.get(session_id)