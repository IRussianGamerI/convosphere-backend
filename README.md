# convosphere-backend

Backend repository for course work on Networking

```json
{
  "name": "Convosphere",
  "description": "topical forum service",
  "team": {
    "name": "LAD",
    "participants": [
      "Romashko Daria",
      "Svechnikova Anna",
      "Barabanshchikov Lev"
    ]
  },
  "parts": {
    "backend": "Barabanshchikov Lev",
    "frontend": "Romashko Daria",
    "integration": "Svechnikova Anna"
  }
}
```

### Python 3.11 is recommended.

## Install

1. Create virtual environment
    ```bash
    python3 -m venv venv
    
    source venv/bin/activate
    
    pip install -r requirements.txt
    ```

2. Install PostgreSQL
    ```bash
    sudo apt update
    sudo apt install python3-dev libpq-dev postgresql postgresql-contrib
    ```
3. Create database
   ```bash
   sudo -u postgres psql
   ```
   ```sql
   CREATE DATABASE convosphere;
   CREATE USER cs_admin WITH PASSWORD 'cs_admin';
   ALTER ROLE cs_admin SET client_encoding TO 'utf8';
   ALTER ROLE cs_admin SET default_transaction_isolation TO 'read committed';
   ALTER ROLE cs_admin SET timezone TO 'UTC';
   
   GRANT ALL PRIVILEGES ON DATABASE convosphere TO cs_admin;
   ALTER DATABASE convosphere OWNER TO cs_admin;

   \q
   ```
4. Apply migrations
   ```bash
   python3 manage.py makemigrations convosphere_backend
   python3 manage.py migrate
   ```

## Run
   ```bash
   python3 manage.py runserver
   ```

## Manually test gRPC server
1. Create Django superuser
   ```bash
   python manage.py createsuperuser
   ```
   Then fill all the credentials
2. Somehow create another user (e.g. `POST /api/users/ ...` or `INSERT INTO auth_user ...`)
3. Run the script
    ```bash
    python manual_test.py
    ```
   While the gRPC server is running:
   ```bash
   python manage.py grpcrunserver
   ```