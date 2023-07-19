from flask import Flask, request, jsonify
import db
import git
import ipfs
import logging
import os

logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route('/clone', methods=['POST'])
def clone_repo():
    data = request.get_json()
    git_url = data['git_url']

    logger.info(f"Received request to clone and pin git_url {git_url}")
    id = db.create_job(git_url, "pins.db")
    run_job(id, git_url, "pins.db")

    logger.info(f"Job {id} for git_url {git_url} completed successfully")
    return jsonify({"id": id})

@app.route('/status/<int:id>', methods=['GET'])
def status(id):
    logger.info(f"Received request for status of job {id}")
    job = db.get_job(id, "pins.db")
    if job is None:
        logger.error(f"No such job {id}")
        return jsonify({"error": "No such job"}), 404
    logger.info(f"Job {id} status fetched successfully. Status: {job[0]}, CID: {job[1]}")
    return jsonify({"status": job[0], "cid": job[1]})

def run_job(id, git_url, db_path):
    logger.info(f"Running job {id} for git_url {git_url}")
    try:
        logger.info(f"Updating job {id} to 'cloning'")
        db.update_job(id, 'cloning', None, db_path)

        # Extract the git project name from the git_url
        git_project_name = git_url.rstrip("/").split("/")[-1]

        # create a unique directory for the git repo in the /downloads directory
        git_repo_dir = os.path.join("/downloads", git_project_name)
        git.clone_git_repo(git_url, git_repo_dir)

        logger.info(f"Updating job {id} to 'pinning'")
        db.update_job(id, 'pinning', None, db_path)

        # Check storage before pinning and deleting the directory
        if ipfs.check_storage("/downloads") > 0.8:
            ipfs.unpin_old_pins(db_path)

        cid = ipfs.pin_directory_in_ipfs(git_repo_dir, db_path)

        logger.info(f"Updating job {id} to 'done'")
        db.update_job(id, 'done', cid, db_path)
    except Exception as e:
        logger.info(f"Updating job {id} to 'error'")
        db.update_job(id, 'error', None, db_path)
        logger.error(f"Error occurred while running job {id}. Error: {str(e)}")
        raise e

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s')
    db.create_db("pins.db")
    logger.info("Server started successfully.")
    app.run(debug=True)
