# Changelog

## Version X.X.X (XXXX-XX-XX)

- [Feature] Allow to search for radios by their codings name during hand out and inside the device overview table
- [Bugfix] Event log: Binding deletion user always same as binding creation user


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
