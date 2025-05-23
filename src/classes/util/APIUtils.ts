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

import axios from "@/plugins/axios";
import { AxiosError } from "axios";

interface VuetifyTableSortByEntry {
    key: string;
    order: string;
}

export class APIUtils {

    /**
     * Converts a Vuetify table ordering to a DRF query parameter.
     *
     * @param sortBy Vuetify table ordering.
     *
     * @returns DRF query parameter.
     */
    public static vuetifyTableOrderingToQueryParameter(sortBy: VuetifyTableSortByEntry[]): string {
        let ordering = '';

        sortBy.forEach((item: any) => {
            if (!item || item.key === undefined) {
                return;
            }

            // Translate JS dot notation to Django double underscore notation
            let key = item.key.replaceAll('.', '__');

            // Special case for radio coding objects and others
            if (key === 'template__coding') {
                key = 'template__radiodevicetemplate__coding__name';
            } else if (key === 'coding') {
                key = 'coding__name';
            } else if (key === 'user__pretty_name') {
                key = 'user__nickname';
            } else if (key === 'bound_by__pretty_name') {
                key = 'bound_by__nickname';
            }

            // Add the ordering to the query string
            ordering += (item.order === 'asc') ? key : '-' + key;
        });

        return ordering;
    }

    /**
     * Fetches data from the API using HTTP GET.
     *
     * @param apipath API path to query (e.g. '/users/').
     */
    public static async get(apipath: string) {
        return axios.get(`${import.meta.env.VITE_EFTDMS_API_BASE_URL}${apipath}`);
    }

    /**
     * Posts data to the API using HTTP POST.
     *
     * @param apipath API path to send request to (e.g. '/users/').
     * @param data Data to post.
     */
    public static async post(apipath: string, data: any) {
        return axios.post(`${import.meta.env.VITE_EFTDMS_API_BASE_URL}${apipath}`, data);
    }

    /**
     * Sends a patch request to the API using HTTP PATCH.
     *
     * @param apipath API path to send request to (e.g. '/users/').
     * @param data Data to patch.
     */
    public static async patch(apipath: string, data: any) {
        return axios.patch(`${import.meta.env.VITE_EFTDMS_API_BASE_URL}${apipath}`, data);
    }

    /**
     * Issues a delete call to the given API path, followed by optional the args
     * @param apipath API path to query (e.g. '/users/').
     * @param args Arguments to append to the API path (e.g. '1' for '/users/1').
     */
    public static async delete(apipath: string, args: string) {
        return axios.delete(`${import.meta.env.VITE_EFTDMS_API_BASE_URL}${apipath}${args}`);
    }

    /**
     * Fetches a page of data from the API.
     *
     * @param apipath API path to query (e.g. '/users/').
     * @param page Number of the page to fetch.
     * @param itemsPerPage Number of items per page.
     * @param sortBy Field to sort by.
     * @param search Search string to filter by.
     * @param additionalParams Additional GET parameters to append.
     */
    public static async fetchPage(
        apipath: string,
        page: number,
        itemsPerPage: number,
        sortBy: any[],
        search: string,
        additionalParams: string[] = []
    ) {
        // Determine the offset and limit for the API call (itemsPerPage of -1 means all items)
        const limit = (itemsPerPage === -1) ? 100 : itemsPerPage;
        const ordering = APIUtils.vuetifyTableOrderingToQueryParameter(sortBy);
        let offset = (itemsPerPage === -1) ? 0 : (page - 1) * itemsPerPage;

        // Build query string from additional params
        const params = additionalParams.reduce((res, param) => `${res}&${param}`, '');

        // Prepare the return data structure
        const ret = {
            items: [],
            total: 0,
        };

        // Fetch the data from the API
        let hasMore = true;
        do {
            await axios.get(
                `${import.meta.env.VITE_EFTDMS_API_BASE_URL}${apipath}?limit=${limit}&offset=${offset}&ordering=${ordering}&search=${search}${params}`
            ).then((response) => {
                ret.items = ret.items.concat(response.data.results);
                ret.total = response.data.count;

                offset += response.data.results.length;
                hasMore = response.data.next !== null;
            }).catch((error) => {
                hasMore = false;
            });
        } while (hasMore && (itemsPerPage === -1 || ret.items.length < itemsPerPage));

        // Only return the requested number of items at max
        if (itemsPerPage !== -1) {
            ret.items = ret.items.slice(0, itemsPerPage);
        }

        return ret;
    }

    /**
     * Transforms an AxiosError produced during a create operation into a human
     * readable string.
     *
     * @param error The AxiosError to transform.
     * @return string The human readable error string.
     */
    public static createErrorToString(error: AxiosError): string {
        if (error.response) {
            if (error.response.status == 409) {
                return String(error.response.data);
            }

            if (error.response.status != 400) {
                return error.message;
            }

            return Object.keys((error.response as any).data).reduce((res: string, prop: string) =>
                res + prop + ': ' + (error.response as any).data[prop].join(' ') + '\n'
            , '');
        } else if (error.request) {
            return 'No response received from server.';
        } else {
            return error.message;
        }
    }

}