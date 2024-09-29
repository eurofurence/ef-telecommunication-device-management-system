/* Eurofurence Telecommunication Device Management System (EF-TDMS)
 * Copyright (C) 2024 Niels Gandraß <niels@gandrass.de>
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.

 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <https://www.gnu.org/licenses/>.
 */

import { defineStore } from 'pinia'
import {APIUtils} from "@/classes/util/APIUtils";

export const useProvisionStore = defineStore("provision", {
    state: () => ({}),

    actions: {
        /**
         * Fetches the provision metadata from the backend.
         *
         * @return Metadata object containing config, firmware, phonebook, and wallpaper metadata.
         */
        async fetchProvisionMetadata() {
            return APIUtils.get('/provision/');
        },

        /**
         * Fetches the phone configuration XML for a given MAC address.
         *
         * @param mac MAC address of the phone (without colons).
         * @return Phone configuration XML.
         */
        async fetchPhoneConfig(mac: string) {
            return APIUtils.get(`/provision/config/${mac}/`);
        },

        /**
         * Fetches a full phonebook XML.
         *
         * @param name Name of the phonebook to fetch (without extension).
         * @return Phonebook XML.
         */
        async fetchPhonebook(name: string) {
            return APIUtils.get(`/provision/phonebook/${name}/`);
        },

    },
})