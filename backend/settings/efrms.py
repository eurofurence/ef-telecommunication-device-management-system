"""
Eurofurence Telecommunication Device Management System (EF-TDMS)
Copyright (C) 2025 Niels Gandraß <niels@gandrass.de>

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
"""

"""
Custom EFTDMS settings
"""

import environ
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = environ.Path(__file__) - 3
env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

PROVISION_DIR = BASE_DIR.path('provision')
PROVISION_CONFIG_DIR = PROVISION_DIR.path('cfg')
PROVISION_FIRMWARE_DIR = PROVISION_DIR.path('fw')
PROVISION_PHONEBOOK_DIR = PROVISION_DIR.path('phonebook')
