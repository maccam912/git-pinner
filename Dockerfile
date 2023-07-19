# Dockerfile
FROM python:3.11

RUN wget https://dist.ipfs.tech/kubo/v0.21.0/kubo_v0.21.0_linux-amd64.tar.gz
RUN tar -xvf kubo_v0.21.0_linux-amd64.tar.gz
RUN rm -rf kubo_v0.21.0_linux-amd64.tar.gz
RUN bash /kubo/install.sh

# Set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /code

# Install dependencies
COPY requirements.txt /code/
RUN pip install -r requirements.txt

# Copy project
COPY . /code/

# Expose the Flask port
EXPOSE 5000

RUN curl -s https://packagecloud.io/install/repositories/github/git-lfs/script.deb.sh | bash
RUN apt-get install -y git-lfs

CMD ["bash", "startup.sh"]
