# Eurofurence Telecommunication Device Management System (EF-TDMS)

TODO ;)


## Installation

1. Clone the repository
2. Copy the `.env.dist` file to `.env` and adjust the settings
3. Place map assets into `src/assets/deploymentmap/`
4. Create empty SQLite database file
   - `touch db.sqlite3`
   - `chown 1000:1000 db.sqlite3`
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


## License

Eurofurence Telecommunication Device Management System (EF-TDMS)

Copyright (C) 2024 Niels Gandraß <niels@gandrass.de>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
