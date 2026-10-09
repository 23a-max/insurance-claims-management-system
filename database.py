

from contextlib import contextmanager
import sqlite3

DATABASE_NAME = "insurance.db"


@contextmanager
def get_connection():
    connection = sqlite3.connect(DATABASE_NAME)
    connection.row_factory = sqlite3.Row

    try:
        yield connection
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()



def create_tables():
    """Create the claims table if it doesn't exist."""
    with get_connection() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS claims (
                claim_id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_name TEXT NOT NULL,
                policy_number TEXT NOT NULL,
                claim_amount REAL NOT NULL CHECK (claim_amount > 0),
                description TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'Submitted'
                    CHECK (status IN (
                        'Submitted',
                        'Under Review',
                        'Approved',
                        'Rejected'
                    ))
            )
        """)


if __name__ == "__main__":
    create_tables()
    print("Database initialized successfully!")
