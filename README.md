# Pytarpit

Simple tarpit for SSH and HTTP connections.

What's a tarpit? Think of a honeypot, but very slow. It listens for incoming connections and tries to make the handshake
infinitely slow without expending a lot of resources hoping to waste resources from malicious people scanning the entire
internet for open ports.

Put it to listen on your public HTTP and SSH ports, and move your services to other ports.

Based on [nullprogram.com/blog/2019/03/22/](https://nullprogram.com/blog/2019/03/22/)

## Basic setup

Running this natively depends on [Python 3.11](https://www.python.org/downloads/)
and [Poetry](https://python-poetry.org/docs/#installation), so make sure those are set up. Then clone the repository and
run:

```shell
poetry install
poetry run python main.py
```

## Docker

You can also run the tool in Docker with the pre-built containers
at [ghcr.io/lietu/pytarpit](https://ghcr.io/lietu/pytarpit). Supporting both linux/amd64 and linux/arm64 platforms.

```shell
docker run -p 10080:10080 -p 10022:10022 ghcr.io/lietu/pytarpit
```

You might want to add `--restart unless-stopped` or similar.

## Configuration

Defaults to `SSH_PORT=10022` and `HTTP_PORT=10080`, and you can forward whatever ports you want into them. If you really
want to override these, you can set up environment variables for the ports.

```shell
SSH_PORT=1222 HTTP_PORT=1280 poetry run python main.py
```

```shell
docker run -e SSH_PORT=1222 -e HTTP_PORT=1280 -p 1280:1280 -p 1222:1222 ghcr.io/lietu/pytarpit
```

If running natively, you can of course just edit the defaults in `settings.py`

## Development

You will need:

- [pre-commit](https://pre-commit.com/#install)
- [Python 3.11](https://www.python.org/downloads/)
- [Poetry](https://python-poetry.org/docs/#installation)

```shell
pre-commit install
poetry install
poetry run python main.py
```

## License

[BSD 3-clause](./LICENSE)
