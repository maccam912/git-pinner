import os
from ipfshttpclient2 import connect
import sqlite3
import stat
import shutil
import logging
import time

logger = logging.getLogger(__name__)

def pin_directory_in_ipfs(directory, db_path):
    logger.info(f"Pinning directory {directory} in IPFS")

    # Remove the .git directory
    git_dir = os.path.join(directory, ".git")
    if os.path.exists(git_dir):
        # Change permissions and remove directory
        for root, dirs, files in os.walk(git_dir):
            for momo in dirs:
                os.chmod(os.path.join(root, momo), stat.S_IWUSR)
            for momo in files:
                os.chmod(os.path.join(root, momo), stat.S_IWUSR)
        logger.info(f"Removing .git directory at {git_dir}")
        shutil.rmtree(git_dir)

    with connect('/ip4/127.0.0.1/tcp/5001/http') as client:
        res = client.add(directory, recursive=True, pin=True)
        pin_time = time.time()
        
        # Get the CID of the root directory that was added to IPFS
        cid = res[-1]['Hash']

        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute("INSERT INTO pins (cid, pin_time) VALUES (?, ?)", (cid, pin_time))
        conn.commit()
        conn.close()

    shutil.rmtree(directory)
    logger.info(f"Directory {directory} pinned successfully in IPFS. CID: {cid}")
    return cid

def unpin_old_pins(db_path):
    logger.info(f"Unpinning old pins in IPFS")
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    now = time.time()

    c.execute("SELECT cid FROM pins WHERE ? - pin_time > 86400", (now,))
    old_pins = c.fetchall()

    with connect('/ip4/127.0.0.1/tcp/5001/http') as client:
        for cid in old_pins:
            client.pin.rm(cid[0])
            c.execute("DELETE FROM pins WHERE cid = ?", (cid[0],))

    conn.commit()
    conn.close()
    logger.info(f"Old pins removed successfully in IPFS")

def check_storage(directory):
    logger.info(f"Checking storage in directory {directory}")
    total, used, free = shutil.disk_usage(directory)
    logger.info(f"Storage in directory {directory} checked successfully. Used/Total: {used/total}")
    return used / total
