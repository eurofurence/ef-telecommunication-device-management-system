/* Eurofurence Telecommunication Device Management System (EF-TDMS)
 * Copyright (C) 2025 Niels Gandraß <niels@gandrass.de>
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

export const useEventLogStore = defineStore("eventlog", {
    state: () => ({}),

    actions: {
        /**
         * Fetches a page of event log entries from the API.
         *
         * @param page Number of the page to fetch.
         * @param itemsPerPage Number of items per page.
         * @param sortBy Field to sort by.
         * @param search Search string to filter by.
         * @param actions List of actions to filter for.
         */
        async fetchEventLogsPage(page: number, itemsPerPage: number, sortBy: any[], search: string, actions: string[] = []) {
            return APIUtils.fetchPage(
                '/eventlog/',
                page,
                itemsPerPage,
                sortBy,
                search,
                actions.map(val => `action=${val}`)
            );
        },
    },
})