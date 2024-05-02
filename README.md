# Eurofurence Telecommunication Device Management System (EF-TDMS)

TODO ;)


## Installation

1. Clone the repository
2. Copy the `.env.dist` file to `.env` and adjust the settings
3. Place map assets into `src/assets/deploymentmap/`
4. Create empty SQLite database file
   - `touch db.sqlite3`
   - `chmod 777 db.sqlite3`
   - TODO: This needs to be improved but works for now ... Yes, I know that this is dirty ;)
5. Build with `docker compose build`
6. Run with `docker compose up -d`
7. Setup default permission groups: `docker compose exec -it backend python manage.py setuppermissions`
8. Create Django superuser with `docker compose exec -it backend python manage.py createsuperuser`


### Deploy a test installation using fixtures

1. Create a running instance of the EF-TDMS. Do not set up permissions nor create a superuser yet.
2. Load the desired fixtures into the database
   - `docker compose exec -it backend python manage.py loaddata backend/fixtures/*`
3. Set a password for the superuser
   - `docker compose exec -it backend python manage.py changepassword admin`
