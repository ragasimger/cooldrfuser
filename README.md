# CoolDRF User

Custom DRF User Model built on Django with the complete authentication along with OTP functionality, and permissions.

## Pipenv

###### Install pipenv on your machine
`pip install pipenv`

###### Create/Activate virtual env with pipenv
`pipenv shell`

###### Install the packages from Pipfile.lock
`pipenv install`


## .env

Rename the .env.example file to .env


Add the credentials for the Postgres DB, Email, and it's password on .env

## Run Migrations and start the server

`python manage.py makemigrations`

`python manage.py migrate`

`python manage.py runserver`
