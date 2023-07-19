import sqlite3
import logging
from contextlib import contextmanager

logger = logging.getLogger(__name__)

@contextmanager
def get_db(db_path):
    logger.debug(f"Connecting to database at {db_path}")
    conn = sqlite3.connect(db_path)
    try:
        yield conn
    finally:
        logger.debug(f"Closing connection to database at {db_path}")
        conn.close()

def create_db(db_path):
    logger.info(f"Creating database at {db_path}")
    with get_db(db_path) as conn:
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS pins (
                cid TEXT PRIMARY KEY,
                pin_time REAL
            )
        ''')
        c.execute('''
            CREATE TABLE IF NOT EXISTS jobs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                git_url TEXT,
                status TEXT,
                cid TEXT
            )
        ''')
        conn.commit()
        logger.info(f"Database created successfully at {db_path}")

def create_job(git_url, db_path):
    logger.info(f"Creating job for git_url {git_url}")
    with get_db(db_path) as conn:
        c = conn.cursor()
        c.execute("INSERT INTO jobs (git_url, status) VALUES (?, 'pending')", (git_url,))
        conn.commit()
        id = c.lastrowid
        logger.info(f"Job {id} created successfully for git_url {git_url}")
        return id

def update_job(id, status, cid, db_path):
    logger.info(f"Updating job {id} with status {status} and cid {cid}")
    with get_db(db_path) as conn:
        c = conn.cursor()
        c.execute("UPDATE jobs SET status = ?, cid = ? WHERE id = ?", (status, cid, id))
        conn.commit()
        logger.info(f"Job {id} updated successfully with status {status} and cid {cid}")

def get_job(id, db_path):
    logger.info(f"Fetching job {id}")
    with get_db(db_path) as conn:
        c = conn.cursor()
        c.execute("SELECT status, cid FROM jobs WHERE id = ?", (id,))
        row = c.fetchone()
        if row:
            logger.info(f"Job {id} fetched successfully. Status: {row[0]}, CID: {row[1]}")
        return row
