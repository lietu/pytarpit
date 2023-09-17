FROM ghcr.io/lietu/python-base:ubuntu-python3.11

WORKDIR /src/

ADD poetry.lock pyproject.toml .
RUN : \
 && set -exu \
 && poetry install \
 && :

ADD *.py .

ENTRYPOINT ["poetry", "run", "python", "main.py"]
