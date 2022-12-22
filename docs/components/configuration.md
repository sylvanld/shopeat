
To configure ShopEat components, you first need to select a [configuration loader](#configuration-loaders)

## Configuration key format

Configuration key should be lowercased, and nested properties dot-separated.

For example URL of a database could be: `sqlalchemy.database.url`

## Configuration loaders

Configuration loader determines how to get value of a given key. Its role is to provide a pluggable way to change configuration source like environment variables, hashicorp vault, etc...

|Loader|Description|
|-|-|
|EnvironmentConfigLoader|**Default**. Load configuration key from environment variables. A key named `shopeat.amqp_broker.url` will lookup for an environment variable named `SHOPEAT_AMQP_BROKER_URL`|

## Components configuration

Each components defines unique configuration keys and plugins.
Have a look at components configuration page for more details:

- [API configuration](api/configuration.md)
- [Notifier configuration](notifier/configuration.md)
