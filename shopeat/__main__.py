import click


@click.group()
def CLI():  # pylint: disable=invalid-name
    ...


@CLI.command("api-specs")
@click.option(
    "--no-info", is_flag=True, help="Remove 'info' key from generated openapi spec."
)
@click.option(
    "--pretty", is_flag=True, help="Properly indent JSON to make it human readable"
)
def print_openapi_schema(no_info: bool, pretty: bool):
    import json

    import shopeat.api.asgi

    indent = 4 if pretty else None
    openapi_spec = shopeat.api.asgi.app.openapi()
    if no_info:
        openapi_spec.pop("info")
    print(json.dumps(openapi_spec, indent=indent))


@CLI.command("api-start")
def start_api():
    import uvicorn

    import shopeat.api.asgi
    from shopeat.core.config import Config
    from shopeat.settings import SHOPEAT_API_HOST, SHOPEAT_API_PORT

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
