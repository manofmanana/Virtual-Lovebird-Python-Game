import os
import sqlite3
from datetime import datetime


def init_database(db_path, schema_path='schema.sql'):
    """Initialize the SQLite database with schema at db_path."""
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    with open(schema_path, 'r') as f:
        schema = f.read()
        cursor.executescript(schema)

    conn.commit()
    conn.close()


def save_state(db_path, mango_state):
    """Save Mango state dict into the database at db_path."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM mango_state")
    cursor.execute(
        """
        INSERT INTO mango_state
        (hunger, happiness, cleanliness, energy, health, age, last_updated)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            mango_state['hunger'],
            mango_state['happiness'],
            mango_state['cleanliness'],
            mango_state['energy'],
            mango_state['health'],
            mango_state['age'],
            datetime.now().isoformat(),
        ),
    )

    conn.commit()
    conn.close()


def load_state(db_path):
    """Load Mango state from database at db_path, return dict or None."""
    if not os.path.exists(db_path):
        return None
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM mango_state ORDER BY id DESC LIMIT 1")
    result = cursor.fetchone()
    conn.close()

    if result:
        return {
            'hunger': result[1],
            'happiness': result[2],
            'cleanliness': result[3],
            'energy': result[4],
            'health': result[5],
            'age': result[6],
            'last_updated': result[7],
        }
    return None
