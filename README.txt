README.txt

This is a simple Flask web service that allows you to clone a Git repository (with Git LFS support) and pin it to IPFS.

STRUCTURE

The service is split into several Python files:

- server.py: This is the main file that runs the Flask server.
- db.py: This file contains functions for interacting with the SQLite database.
- git.py: This file contains functions for cloning Git repositories.
- ipfs.py: This file contains functions for interacting with IPFS.
- tasks.py: This file contains the Celery tasks that perform the actual work.

ENDPOINTS

- POST /clone: Clone a Git repository and pin it to IPFS. The request body should be a JSON object with a 'git_url' property. The response is a JSON object with an 'id' property that you can use to check the status of the job.
- GET /status/<id>: Get the status of a job. The response is a JSON object with a 'status' property (which can be 'pending', 'cloning', 'pinning', 'done', or 'error') and a 'cid' property (which is the IPFS CID of the repository if the job is done).

USAGE

To clone a repository and pin it to IPFS, you can use the following command:

curl -X POST -H "Content-Type: application/json" -d '{"git_url":"https://github.com/huggingface/transformers"}' http://localhost:5000/clone

This will return a job ID that you can use to check the status of the job:

curl http://localhost:5000/status/<id>

Replace <id> with the ID returned by the '/clone' endpoint.

DOCKER

To build and run the Docker image, you can use the following commands:

docker build -t myproject .
docker run -p 5000:5000 myproject

This will make the Flask server available at http://localhost:5000.

DEPENDENCIES

This project uses the following Python libraries:

- Flask
- ipfshttpclient
- Celery
- Redis

