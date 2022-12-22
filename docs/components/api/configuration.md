# API Configuration

Have a look at general [configuration](../../configuration) section to understand how to set configuration key, and select a configuration source.

## Mandatory configuration

| Key                     | Description                                                                                      |
| ----------------------- | ------------------------------------------------------------------------------------------------ |
| shopeat.amqp_broker.url | URL of the AMQP broker (generally rabbitmq) that handle queuing of notifications coming from API |
| shopeat.database.url    | SQL database connection URL, as used by SQLAlchemy                                               |
| shopeat.jwt.secret      | Secret string used to encode JWT using                                                           |

## Plugins

Coming soon...
