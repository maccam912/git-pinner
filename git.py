import subprocess
import logging

logger = logging.getLogger(__name__)

def clone_git_repo(git_url, destination):
    logger.info(f"Cloning git repo {git_url} to {destination}")
    subprocess.check_call(["git", "lfs", "install"])
    subprocess.check_call(["git", "clone", "--depth", "1", git_url, destination])
    logger.info(f"Git repo {git_url} cloned successfully to {destination}")
