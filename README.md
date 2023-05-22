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
   \q
   ```
4. Apply migrations
   ```bash
   python3 manage.py makemigrations
   python3 manage.py migrate
   ```

## Run
   ```bash
   python3 manage.py runserver
   ```
