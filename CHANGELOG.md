# Changelog

## Version X.Y.Z (YYYY-MM-DD)

- [Maintenance] Update JavaScript dependencies


## Version 1.12.1 (2025-08-28)

- [Maintenance] Update public on-site information on home page


## Version 1.12.0 (2025-07-27)

- [Feature] Add serial number and MAC address to admin overview of voip phones


## Version 1.11.2 (2025-07-24)

- [Maintenance] Update Python dependencies
- [Maintenance] Update JavaScript dependencies


## Version 1.11.1 (2025-07-16)

- [Bugfix] Fix loading of pins on deployment map after layer change
- [Bugfix] Hide map pins from previous layer instantly upon layer change
- [Maintenance] Update JavaScript dependencies


## Version 1.11.0 (2025-07-15)

- [Feature] Add intermediate floor between ground and first floor to deployment map
- [Maintenance] Update Python dependencies
- [Maintenance] Update JavaScript dependencies


## Version 1.10.0 (2025-07-11)

- [Feature] Add basement (floor -1) to deployment map
- [Feature] Improve layout of sub-navigation items if sidebar is collapsed
- [Bugfix] Fix item table reloading upon change
- [Bugfix] Hide "Show on deployment map" button for items without coordinates if not forced to display
- [Maintenance] Update Python dependencies
- [Maintenance] Update JavaScript dependencies


## Version 1.9.0 (2025-05-25)

- [Feature] Add management command for cleaning up the database between events
- [Bugfix] Display log entries with missing user information as "Unknown user"


## Version 1.8.5 (2025-05-25)

- [Bugfix] Revert `djangorestframework-simplejwt` to v5.4.0 to fix token refresh endpoint issues


## Version 1.8.4 (2025-04-27)

- [Bugfix] Fix Poetry environment installation in Docker backend image
- [Maintenance] Update copyright year
 

## Version 1.8.3 (2025-04-27)

- [Maintenance] Update Python dependencies
- [Maintenance] Update Python runtime to v3.13
- [Maintenance] Update JavaScript dependencies
- [Maintenance] Update Docker base images


## Version 1.8.2 (2024-09-30)

- [Bugfix] Remove duplicate "Account" label from phone MPK inspection dialog


## Version 1.8.1 (2024-09-30)

- [Bugfix] Fix backend Docker container provisioning file access


## Version 1.8.0 (2024-09-30)

- [Feature] Allow to search for radios by their codings name during hand out and inside the device overview table
- [Feature] Allow to filter items by their status ('Available', 'Handed out', 'Private')
- [Feature] Prepare backend for advanced filter options
- [Feature] Read phone provisioning files from disk into backend and expose via API
- [Feature] Display phone provisioning files (configs, phonebooks, firmwares, wallpapers) in frontend
- [Feature] Parse phone config files for key information (e.g., MPK mappings, ...)
- [Bugfix] Fix sorting of nested columns in item overview tables
- [Bugfix] Sort items in server-side search results lexicographically, based on their title
- [Bugfix] Event log: Binding deletion user always same as binding creation user
- [Misc] Optimize frontend item table refresh logic
- [Maintenance] Update Python dependencies
- [Maintenance] Update JavaScript dependencies


## Version 1.7.0 (2024-09-14)

- [Feature] Add radio usage guide to home page
- [Feature] Add on-site service information to home page
- [Feature] Add contact information / support chat to home page
- [Bugfix] Fix name of `provisioning.htpasswd.dist` file template
- [Bugfix] Declare provision folder mounting in `docker-compose.yml`
- [Docs] Create screenshots and add them to `README.md`


## Version 1.6.1 (2024-09-10)

- [Feature] Create protected directory to serve VoIP provisioning files
- [Maintenance] Update Python dependencies
- [Maintenance] Update JavaScript dependencies


## Version 1.6.0 (2024-08-17)

- [Feature] Django management command to synchronize local user data with the Eurofurence registration system
- [Misc] Make EF registration ID optional within `User` forms
- [Maintenance] Update Python dependencies
- [Maintenance] Update JavaScript dependencies


## Version 1.5.2 (2024-08-07)

- [Maintenance] Update Python dependencies
   - Fix CVE-2024-42005
   - Fix CVE-2024-41991
   - Fix CVE-2024-41990
   - Fix CVE-2024-41989
- [Maintenance] Update JavaScript dependencies


## Version 1.5.1 (2024-07-28)

- [Feature] Make main navigation drawer collapsible (default on mobile)
- [Feature] Improve mobile layout
- [Maintenance] Update Python dependencies
- [Maintenance] Update JavaScript dependencies


## Version 1.5.0 (2024-07-24)

- [Feature] Integrate item coordinates in CRUD forms for Phones, Callboxes, RadioDevices, and Pagers
- [Feature] Add button to show / highlight items on deployment map from ItemOverview pages
- [Bugfix] Fix Dockerfile `FROM ... AS ...` keyword case sensitivity
- [Misc] Update metadata in package manager files
- [Misc] Improve code readability in API abstraction layer
- [Maintenance] Update Python dependencies
- [Maintenance] Update JavaScript dependencies
