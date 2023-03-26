# Restaurant Reservation API

# Getting started

## Installation

make a new folder for the project and open this folder in the Terminal/Windows (PowerShell) and run this command

```bash
git clone https://github.com/omar-bendary/Shahry_task.git
```

# Pre-requisites and Local Development

# Using Docker and Docker compose

The first step is to sign up for
a free account on [DockerHub](https://hub.docker.com/signup)  and then install the Docker desktop app on your local machine:

* [Docker for Mac](https://docs.docker.com/desktop/install/mac-install/)
* [Docker for Windows](https://docs.docker.com/desktop/install/windows-install/)
  Once Docker is done installing we can confirm the correct version is running by typing the
  command docker --version in the command line shell

```shell
$ docker --version
Docker version 20.10.14, build a224086
```

### Running our container

1- Open the project Code folder in Terminal/Windows (PowerShell).

2- Run this command .

```bash
docker-compose up -d --build
```

### To Stop the currently running container

Control+c (press the “Control” and “c” button at
the same time) and additionally type docker-compose down.

```shell
docker-compose down
```

### Now let’s confirm everything is working

```bash
docker-compose exec web python manage.py  makemigrations 
```

```bash
docker-compose exec web python manage.py  migrate 
```

> Now create the admin user

```bash
 docker-compose exec web python manage.py createsuperuser 
```

The application is run on http://127.0.0.1:8000/

**Open http://127.0.0.1:8000/api/v1 your web browser**

### Set up your RDBMS , open your setting.py

```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "postgres",
        "USER": "postgres",
        "PASSWORD": "postgres",
        "HOST": "db",  # set in docker-compose.yml
        "PORT": 5432,  # default postgres port
    }
}
```

<br/>
 All the extracted data is saved to the database to use it later if needed.
<br/>
<br/>

# Using virtual environment approach.

## To create a virtual environment

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install packages.

1- Open the project Code folder in Terminal/Windows (PowerShell).

2- Run this command .

```bash
# Windows
> python -m venv .venv
> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# macOS
% python3 -m venv .venv
```

### To activate a new virtual environment called .venv:

```bash
# Windows
> .venv\Scripts\Activate.ps1
(.venv) >

# macOS
% source .venv/bin/activate
(.venv) %
```

### To deactivate and leave a virtual environment type deactivate.

```bash
# Windows
(.venv) > deactivate
>

# macOS
(.venv) % deactivate
%
```

### install requirements.txt

Run `pip install requirements.txt`. All required packages are included in the requirements file.

> make sure to activate the virtual environment first

```bash
pip install -r requirements.txt
```

**You might see a WARNING message about updating pip after running these commands. It’s always good to be on the latest version of software and to remove the annoying WARNING message each time you use pip. You can either copy and paste the recommended command or run `python -m pip install --upgrade pip` to be on the latest version.**

```bash
(.venv) > python -m pip install --upgrade pip
```

## Now let’s confirm everything is working by running Django’s internal web server via the runserver command

```bash
(.venv) > python manage.py  makemigrations 
```

```bash
(.venv) > python manage.py  migrate 
```

> Now create the admin user

```bash
(.venv) > python manage.py createsuperuser 
```

Run the surver

```bash
# Windows
(.venv) > python manage.py runserver

# macOS
(.venv) % python3 manage.py runserver
```

## Set up your RDBMS , open your setting.py

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your_database_project_name',
        'USER': 'your_postgres_username',
        'PASSWORD': 'your_postgres_password',
        'HOST': 'localhost',   # Or an IP Address that your DB is hosted on
        'PORT': '5432',
    }
}
```

Or you can stick the default database (sqlite3) but not recommended for Production.

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

<br/>
All the extracted data is saved to the database to use it later if needed.
<br/>
The application is run on http://127.0.0.1:8000/api by default in the backend configuration.


## User Authentication

added user authenticated so if we want to add permissions later id needed.

### GET /auth/users/

* General:
  * Create a new user.
  * Returns user information if it was created successfully.
* Sample: `curl http://127.0.0.1:8000/auth/users/ -X POST -H "Content-Type: application/json" -d '{"employe_number": "1234","password": "MyPassword"}`

```json
{
    "employee_number": 1234,
    "id": 1,
}
```

<br/>

### POST /auth/jwt/create/

* General:
  * Login a user to the system by creating access and refresh tokens.
  * Returns user access and refresh tokens (to use it for logging-in) if it was created successfully.
* `curl http://127.0.0.1:8000/auth/jwt/create/ -X POST -H "Content-Type: application/json" `-d '{"employe_number": "1234","password": "MyPassword"}``

```json
{
  {
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY2NzY5NTY4NiwianRpIjoiZDI0MzkzNmM0MGFkNDcxMmEyNGI5N2M5YjIxNWI1ZjciLCJ1c2VyX2lkIjoxfQ.J_YiVMoPBuRK0qHSoLoOy8FrnPM0FFydztEu3qQ_Wy8",
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjY3Njk1Njg2LCJqdGkiOiI5NTY4MGEyNjkyZDg0ZmJhOTlhNzU1NDhkZjQ5ZDc1NyIsInVzZXJfaWQiOjF9.AsdT7UfJTtXlkgKk3Xmhghz3Arz3yytU024wB25w-Nw"
}
}
```

> To keep your user logged-in , use an extention like [Moheader](https://modheader.com/)
>

This is a REST API that allows restaurants to manage table reservations.

## Endpoints

### Tables

* `GET /api/tables/`: List all tables.
* `POST /api/tables/`: Create a new table.
* `GET /api/tables/{id}/`: Retrieve details for a specific table.
* `PUT /api/tables/{id}/`: Update a specific table.
* `DELETE /api/tables/{id}/`: Delete a specific table.

### Reservations

* `GET /api/reservations/`: List all reservations.
* `POST /api/reservations/`: Create a new reservation.
* `GET /api/reservations/{id}/`: Retrieve details for a specific reservation.
* `PUT /api/reservations/{id}/`: Update a specific reservation.
* `DELETE /api/reservations/{id}/`: Delete a specific reservation.
* `GET /api/reservations/today/`: List all reservations for today.
* `GET /api/reservations/available_time_slots/`: Get available time slots for a given number of seats.

## Table Fields

* `id` (auto-generated): unique identifier for the table.
* `number`: the number of the table.
* `seats`: the number of seats at the table.

## Reservation Fields

* `id` (auto-generated): unique identifier for the reservation.
* `table`: the table for which the reservation is made.
* `start_time`: the start time of the reservation.
* `end_time`: the end time of the reservation.

## Usage

To use the API, you can send HTTP requests to the endpoints listed above. The responses will be returned in JSON format.

Authentication is not implemented, but some endpoints require admin privileges.

The `available_time_slots` endpoint requires the `seats` query parameter to be set to an integer value. It returns a list of time slots that are available for a reservation with the given number of seats.

The `create` method of the `ReservationViewSet` checks if the specified table is available for the requested time slot before creating the reservation. If the table is not available, the reservation is not created and an error message is returned.

The `today` endpoint of the `ReservationViewSet` returns all reservations for today's date.

The `list` method of the `ReservationViewSet` can be used to filter reservations by table or date range. The `table` query parameter can be used to filter by table, and the `start_date` and `end_date` query parameters can be used to filter by date range.
