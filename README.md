# Flora API

It's a simple blog api

## Run project

### Docker

First of all, you need to [install Docker](https://docs.docker.com/engine/install/ubuntu/#install-using-the-repository) if it's not installed. And don't forget to install `docker-compose`

```
$ sudo -H pip3 install docker-compose
```

### .env

And then you need to create `.env` file with follow code:

```
# Security
ENVIRONMENT=development
SECRET_KEY=l6fht0!$0xmca@4sz*2er9-3&k^27dyrol-@va8n8k%*v2&wmb
DEBUG=1

# Database
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
```

### Build Image

If you run this project for the first time you need to build Docker image

```
$ docker build .
```

### Up Container

Now you can up container with this project:

```
$ docker-compose up -d
```
