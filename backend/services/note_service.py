"""
Note service layer.

Connects generated notes to the SQLite database.
Notes are stored per session and contain structured output derived
from a transcript, such as a summary, key topics, and action items.
The service layer keeps this storage logic out of the routes so the
rest of the backend can interact with notes through a clean interface.
"""

import json
from datetime import datetime, timezone
from typing import Optional

from forum_ai_notetaker.db import get_connection


def _row_to_dict(row) -> dict:
    return {
        "id": row["id"],
        "session_id": row["session_id"],
        "summary": row["summary"],
        "topics": json.loads(row["topics"]),
        "action_items": json.loads(row["action_items"]),
        "created_at": row["created_at"],
        "updated_at": row["updated_at"],
    }


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
    now = datetime.now(timezone.utc).isoformat()
    encoded_topics = json.dumps(topics)
    encoded_action_items = json.dumps(action_items)

    with get_connection() as conn:
        conn.execute(
            """
            INSERT INTO notes (session_id, summary, topics, action_items, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?)
            ON CONFLICT(session_id) DO UPDATE SET
                summary = excluded.summary,
                topics = excluded.topics,
                action_items = excluded.action_items,
                updated_at = excluded.updated_at
            """,
            (session_id, summary, encoded_topics, encoded_action_items, now, now),
        )
        conn.commit()


def get_notes_by_session(session_id: int) -> Optional[dict]:
    """
    Retrieve the notes for a given session.

    If notes have not been generated yet, this returns None.
    The route layer can use that to show a pending or empty state.

    Args:
        session_id: The session being requested.

    Returns:
        The notes object if it exists, otherwise None.
    """
    with get_connection() as conn:
        row = conn.execute(
            "SELECT * FROM notes WHERE session_id = ?",
            (session_id,),
        ).fetchone()

    return _row_to_dict(row) if row else None


def fetch_notes_by_session_id(session_id: int) -> Optional[dict]:
    """
    Backward-compatible wrapper used by the existing notes route.
    """
    return get_notes_by_session(session_id)