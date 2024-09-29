"""
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
"""

import os
import xml.etree.ElementTree as ET

from backend.settings import PROVISION_CONFIG_DIR, PROVISION_FIRMWARE_DIR, PROVISION_PHONEBOOK_DIR, PROVISION_DIR


def provision_generate_config_metadata() -> list[dict]:
    """
    Generates metadata object for all provision config files
    :return dict: of metadata objects for all provision config files
    """

    # List all files in the provision config directory and build metadata object
    files = os.listdir(PROVISION_CONFIG_DIR)
    ret = []

    for f in files:
        if f.endswith('.xml'):
            # Parse and validate XML file
            tree = ET.parse(os.path.join(PROVISION_CONFIG_DIR, f))
            if tree.getroot().tag != 'gs_provision':
                continue

            # Extract simple data
            accountname = tree.find('.//item[@name="account.1.name"]').text
            extension = tree.find('.//item[@name="account.1.sip.userid"]').text

            # Extract MPK mappings
            mpk = {}
            for idx in range(1, 20):
                mode = tree.find(f'.//item[@name="pks.mpk.{idx}.keyMode"]')
                if mode is None:
                    break

                mpk[idx] = {
                    'keyMode': mode.text,
                    'account': tree.find(f'.//item[@name="pks.mpk.{idx}.account"]').text,
                    'value': tree.find(f'.//item[@name="pks.mpk.{idx}.value"]').text,
                    'description': tree.find(f'.//item[@name="pks.mpk.{idx}.description"]').text
                }

            # Store metadata
            ret.append({
                'filename': f,
                'filesize': os.path.getsize(os.path.join(PROVISION_CONFIG_DIR, f)),
                'mac': f.split('.')[0].replace('cfg', ''),
                'accountname': accountname,
                'extension': extension,
                'mpk': mpk
            })

    return ret

def provision_generate_phonebook_metadata() -> list[dict]:
    """
    Generates metadata object for all provision phonebook files
    :return dict: of metadata objects for all provision phonebook files
    """

    files = os.listdir(PROVISION_PHONEBOOK_DIR)
    ret = []

    for f in files:
        if f.endswith('.xml'):
            tree = ET.parse(os.path.join(PROVISION_PHONEBOOK_DIR, f))
            if tree.getroot().tag != 'AddressBook':
                continue

            entries = []
            for contact in tree.iter('Contact'):
                firstname = contact.find('FirstName')
                lastname = contact.find('LastName')
                phone = contact.find('Phone/phonenumber')

                entries.append({
                    'firstname': firstname.text if firstname is not None else None,
                    'lastname': lastname.text if lastname is not None else None,
                    'phone': phone.text if phone is not None else None
                })

            ret.append({
                'filename': f,
                'filesize': os.path.getsize(os.path.join(PROVISION_PHONEBOOK_DIR, f)),
                'entries': entries
            })

    return ret

def provision_generate_firmware_metadata() -> list[dict]:
    """
    Generates metadata object for all provision firmware files
    :return dict: of metadata objects for all provision firmware files
    """

    files = os.listdir(PROVISION_FIRMWARE_DIR)
    ret = []

    for f in files:
        if f.endswith('.bin'):
            ret.append({
                'filename': f,
                'filesize': os.path.getsize(os.path.join(PROVISION_FIRMWARE_DIR, f))
            })

    return ret

def provision_generate_wallpaper_metadata() -> dict | None:
    """
    Generates metadata object for the wallpaper file
    :return dict: metadata object for the wallpaper file or None if no wallpaper is present
    """

    # Check if wallpaper.jpg exists
    if not os.path.exists(os.path.join(PROVISION_DIR, 'wallpaper.jpg')):
        return None
    else:
        return {
            'filename': 'wallpaper.jpg',
            'filesize': os.path.getsize(os.path.join(PROVISION_DIR, 'wallpaper.jpg'))
        }

def provision_retrieve_config(mac: str) -> str | None:
    """
    Retrieves the config file for a specific MAC address
    :param str mac: MAC address to retrieve config for
    :return str: content of the config file or None if the file does not exist
    """
    # Validate mac address
    if not len(mac) == 12 or not mac.isalnum():
        return None

    # Check if the file exists
    if not os.path.exists(os.path.join(PROVISION_CONFIG_DIR, f"cfg{mac}.xml")):
        return None

    # Read and return the file
    with open(os.path.join(PROVISION_CONFIG_DIR, f"cfg{mac}.xml"), 'r') as f:
        return f.read()

def provision_retrieve_phonebook(name: str) -> str | None:
    """
    Retrieves the phonebook file for a specific name
    :param str name: name of the phonebook file to retrieve
    :return str: content of the phonebook file or None if the file does not exist
    """
    # Validate name
    if not name.isalnum():
        return None

    # Check if the file exists
    if not os.path.exists(os.path.join(PROVISION_PHONEBOOK_DIR, f"{name}.xml")):
        return None

    # Read and return the file
    with open(os.path.join(PROVISION_PHONEBOOK_DIR, f"{name}.xml"), 'r') as f:
        return f.read()
