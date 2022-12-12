import click


@click.group()
def CLI():
    ...


@CLI.command("api-start")
def start_api():
    import uvicorn

    import shopeat.api.asgi
    from shopeat.config import SHOPEAT_API_HOST, SHOPEAT_API_PORT, Config

    uvicorn.run(
        shopeat.api.asgi.app,
        host=Config.get(SHOPEAT_API_HOST, default="127.0.0.1"),
        port=Config.get(SHOPEAT_API_PORT, default=8000, type=int),
    )


@CLI.command("notifier-start")
def start_notifier():
    import asyncio

    from shopeat.notifier.server import WSNotificationServer

    server = WSNotificationServer.from_config()
    asyncio.run(server.run())


if __name__ == "__main__":
    CLI()
