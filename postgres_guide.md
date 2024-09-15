# Setting up the django project and app 

1. `run the command to start the django project after python3 installation, and venv activation`

``` 
django-admin startproject 'project_name' 
python manage.py runserver
```

2. `create the app inside the your project withiin the same directory`

```
python manage.py startapp 'appname'

```


# PostgreSQL set up for Django

. `First we have to create the DB  to make migrations here we are using the Postgre SQL`

[1.] Install the PostgreSQL on your system and then PostgreSQL Adapter for python 
[2.] Than make the migration for the database

## 1. Setting up the PostgresSQL
```
1. Install PostgreSQL and Dependencies (on linux system)
sudo apt install postgresql postgresql-contrib libpq-dev python3-dev

2. Install psycopg2
pip install psycopg2

3. Create a PostgreSQL Database and User, so Log into PostgreSQL
sudo -u postgres psql

4. Create a new database and user:

CREATE DATABASE mydatabase;
CREATE USER jp WITH PASSWORD 'vcapgenerator';

5. Grant the user access to the database:

GRANT ALL PRIVILEGES ON DATABASE mydatabase TO myuser;

6. logout
\q

7. Update the database in settings.py , use the PostgreSQL engine and username, password , host, and port
```
4.  `Apply Migrations Run the following commands it also create the necessary database tables:`

```
python manage.py makemigrations
python manage.py migrate
```

## 2. Troubleshooting: Permission Denied for Schema Public

If you encounter `permission denied for schema public` when trying to apply migrations in Django, follow these steps:

### Steps to Fix:

- **Connect to PostgreSQL**

```
psql -U postgres
\c your_database_name;

```

- **Grant Permissions to PostgreSQL User:**

  ```sql
  GRANT ALL PRIVILEGES ON SCHEMA public TO your_db_user;
  GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO your_db_user;
  ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO your_db_user;
  ALTER ROLE your_db_user WITH SUPERUSER;

- **Ensure Database Configuration in settings.py:**  

```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'vcapgenerator',
        'USER': 'your_db_user',
        'PASSWORD': 'password',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}
```

```
Note: PostgreSQL does not create a file in the project directory like SQLite does. The database is managed by the PostgreSQL server, and you can access it using PostgreSQL tools like psql.
```


- **2. Viewing All Data in a PostgreSQL Table:**
To view all data from a specific table in PostgreSQL, follow these steps:

1. Log In to PostgreSQL , List All Tables:
```
psql -h 127.0.0.1 -U your_db_user -d vcapgenerator
\dt

```


To Start Redis Manually:
sudo systemctl start redis

To Stop Redis Manually:
sudo systemctl stop redis

To Check Redis Status:
sudo systemctl status redis

By not enabling Redis to start on boot, you can