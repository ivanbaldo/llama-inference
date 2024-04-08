# syntax=docker/dockerfile:1

# From the parent directory (main directory of this repo) run:
#
# docker build --build-arg USERID=$(id -u) -t localhost/openai-bench openai
#
# docker run --rm -it --name openai-bench -e OPENAI_API_KEY='secret' \
#   -v"$PWD":/home/user/llama-inference localhost/openai-bench \
#   --baseurl https://api.openai.com:443/v1 --model gpt-3.5-turbo \
#   --filename gpt-3.5-turbo.bench.csv --note "gpt-3.5-turbo"
#
# The container isn't self contained but designed to be used with the repo.

# Look for newer tags here https://hub.docker.com/_/python:
FROM docker.io/python:3.12-bookworm
ARG USERID=1000
COPY requirements.txt /tmp
RUN pip3 install --no-cache-dir -r /tmp/requirements.txt
RUN adduser --disabled-password --gecos '' -u $USERID user
USER user
WORKDIR /home/user/llama-inference/openai/
ENTRYPOINT ["python3", "bench.py"]
CMD [ \
    "--baseurl", "https://api.openai.com:443/v1", \
    "--model", "gpt-3.5-turbo", \
    "--filename", "/dev/stdout", \
    "--note", "gpt-3.5-turbo" \
]
