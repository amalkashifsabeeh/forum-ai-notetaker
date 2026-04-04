"""
Session service layer.

This module connects the route layer to the underlying database.

It provides a stable interface for creating and retrieving session
records without exposing SQL logic to the rest of the application.

A session represents one uploaded recording along with metadata
used to track its lifecycle (uploaded → processing → completed).
"""

from typing import Optional
from forum_ai_notetaker.db import get_connection


def _row_to_dict(row) -> dict:
    """
    Convert a SQLite row into a plain dictionary.

    Keeping this small helper here avoids repeating `dict(row)`
    throughout the service functions and keeps the return format
    consistent across the module.
    """
    return dict(row)


def create_session_record(
    title: str,
    original_filename: str,
    stored_path: str,
    status: str,
) -> dict:
    """
    Create and store a new session record.

    This function is called immediately after a file is uploaded.
    It persists the session metadata so the system can track the
    recording through the processing pipeline.

    Note:
    The session is currently stored without a course reference,
    as the schema does not yet support linking sessions to courses.

    Returns:
        A dictionary representing the created session.
    """
    with get_connection() as conn:
        cursor = conn.execute(
            """
            INSERT INTO sessions (
                title,
                original_filename,
                stored_path,
                status,
                created_at,
                updated_at
            )
            VALUES (?, ?, ?, ?, datetime('now'), datetime('now'))
            """,
            (title, original_filename, stored_path, status),
        )
        conn.commit()

        row = conn.execute(
            """
            SELECT id, title, original_filename, stored_path, status, created_at, updated_at
            FROM sessions
            WHERE id = ?
            """,
            (cursor.lastrowid,),
        ).fetchone()

    return _row_to_dict(row)


def fetch_all_sessions() -> list[dict]:
    """
    Retrieve all sessions from the database.

    Sessions are returned in reverse chronological order so the
    most recent uploads appear first in the UI.
    """
    with get_connection() as conn:
        rows = conn.execute(
            """
            SELECT id, title, original_filename, stored_path, status, created_at, updated_at
            FROM sessions
            ORDER BY id DESC
            """
        ).fetchall()

    return [_row_to_dict(row) for row in rows]


def fetch_one_session(session_id: int) -> Optional[dict]:
    """
    Retrieve a single session by its ID.

    Returns:
        A session dictionary if found, otherwise None.

    This allows routes to safely check for existence before
    attempting to access session-related resources.
    """
    with get_connection() as conn:
        row = conn.execute(
            """
            SELECT id, title, original_filename, stored_path, status, created_at, updated_at
            FROM sessions
            WHERE id = ?
            """,
            (session_id,),
        ).fetchone()

    return _row_to_dict(row) if row else None


def update_session_status(session_id: int, new_status: str) -> None:
    """
    Update the processing status of a session.

    This is typically called by the pipeline as the recording
    moves through different stages (e.g. uploaded → transcribed).

    Keeping this logic in the service layer ensures that status
    changes remain consistent across the system.
    """
    with get_connection() as conn:
        conn.execute(
            """
            UPDATE sessions
            SET status = ?, updated_at = datetime('now')
            WHERE id = ?
            """,
            (new_status, session_id),
        )
        conn.commit()