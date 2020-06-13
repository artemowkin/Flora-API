# Flora API

It's a simple blog api

## Run project

### Docker

First of all, you need to [install Docker](https://docs.docker.com/engine/install/ubuntu/#install-using-the-repository) if it's not installed. And don't forget to install `docker-compose`

```
$ sudo -H pip3 install docker-compose
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

### Superuser

To access the API you need to create a superuser who can use it

```
$ docker-compose exec web python manage.py createsuperuser
```
