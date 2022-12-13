# Deploy with Docker

## ShopEat official image

ShopEat is distributed as a single docker image with multiple entrypoints. So in order to run multiple components:

* Start by downloading ShopEat docker image

```
docker pull sylvanld/shopeat:{imageTag}
```

Have a look at dockerhub to find [available image tags](https://hub.docker.com/r/sylvanld/shopeat/tags).


* Then deploy choosen component by specifying a command to the entrypoint

```
docker run sylvanld/shopeat api-start
```


## Usage with docker-compose

```yaml
version: "3.6"

services:
  shopeat-api:
    image: sylvanld/shopeat
    command: api-start
    environment:
      SHOPEAT_API_HOST: "0.0.0.0"
      SHOPEAT_API_PORT: 8000
      SHOPEAT_AMQP_BROKER_URL: amqp://rabbit:password@rabbitmq
      SHOPEAT_JWT_SECRET: tartampion
      SHOPEAT_DATABASE_URL: "postgresql+asyncpg://postgres:password@database/shopeat"
    ports:
      - 8000:8000
    
  shopeat-notifier:
    image: sylvanld/shopeat
    command: notifier-start
    environment:
      SHOPEAT_NOTIFIER_HOST: 0.0.0.0
      SHOPEAT_NOTIFIER_PORT: 7000
      SHOPEAT_JWT_SECRET: tartampion
      SHOPEAT_AMQP_BROKER_URL: amqp://rabbit:password@rabbitmq
    ports:
      - 7000:7000
    restart: always

  database:
    image: postgres:alpine3.17
    ports:
      - 5432:5432
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: password
    restart: always
  
  rabbitmq:
    image: rabbitmq:3-management
    ports:
      - 5672:5672
      - 15672:15672
    environment:
      RABBITMQ_DEFAULT_USER: rabbit
      RABBITMQ_DEFAULT_PASS: password
    restart: always
```
