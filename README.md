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
7. Create Django superuser with `docker compose exec -it backend python manage.py createsuperuser`
