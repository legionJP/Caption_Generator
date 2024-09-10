# PostgreSQL Troubleshooting and Solutions for Django

## 1. Permission Denied for Schema Public

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
2. \dt
