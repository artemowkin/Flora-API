# Flora-API

This is an API for Flora site to store art works

## Installation

### Using Docker

If you want just to run this project (without contributing) you can use
Docker. For this you need the following packages:

* `docker`
* `docker-compose`

And, If they're already installed you can build the docker image:

```
$ docker-compose build 
```

Up this image:

```
$ docker-compose up -d
```

Apply all migrations (only once after building)

```
docker-compose run web python manage.py migrate
```

If you want to create a superuser account you can run the following command:

```
$ docker-compose run web python manage.py createsuperuser
```

And go on http://127.0.0.1:8000/

### Using python and poetry

If you want to contribute this project you need to install the following:

* [Python >= 3.8](https://www.python.org/downloads/release/python-380/)
* [Poetry](https://python-poetry.org/docs/#installation)

Run the dependencies installation

```
$ poetry install
```

Add the django secret key into `.env` file:

```
DJANGO_SECRET_KEY="2$6#ajqdl8n+-6qs6f#))pivv&hku5rj37iy$y@swp6$v)7+9v"
```

Run the poetry shell and exports environment variables:

```
$ poetry shell
$ export $(cat .env | xargs)
```

Run the migrations:

```
$ python manage.py migrate
```

Create a superuser account:

```
$ python manage.py createsuperuser
```

Run the server:

```
$ python manage.py runserver
```

And go on http://127.0.0.1:8000/

## Running the tests

### Unit tests

If you want to run the unit tests you need to do the following command:

```
$ python manage.py test projects categories
```

### Functional tests

If you want to run the functional tests you need to do the following command:

```
$ python manage.py test functional_tests
```

## Authors

* **Artemowkin** (Backend API) - https://github.com/artemowkin/
* **steelWinds** (Frontend App) - https://github.com/steelWinds/

## License

This project is licensed under the GPL-3.0 License - see the
[LICENSE](LICENSE) file for details.
