import { defineStore } from 'pinia'
import axios from '@/plugins/axios'
import {APIUtils} from "@/classes/util/APIUtils";

export const useUsersStore = defineStore("user", {
    state: () => ({}),

    actions: {
        /**
         * Fetches a page of users from the API.
         *
         * @param page Number of the page to fetch.
         * @param itemsPerPage Number of items per page.
         * @param sortBy Field to sort by.
         */
        async fetchUsersPage(page: number, itemsPerPage: number, sortBy: any[]) {
            // Determine the offset and limit for the API call (itemsPerPage of -1 means all items)
            const limit = (itemsPerPage === -1) ? 100 : itemsPerPage;
            const ordering = APIUtils.vuetifyTableOrderingToQueryParameter(sortBy);
            let offset = (itemsPerPage === -1) ? 0 : (page - 1) * itemsPerPage;

            // Prepare the return data structure
            let ret = {
                items: [],
                total: 0,
            };

            // Fetch the data from the API
            let hasMore = true;
            do {
                await axios.get(
                    `${import.meta.env.VITE_EFRMS_API_BASE_URL}/users/?limit=${limit}&offset=${offset}&ordering=${ordering}`
                ).then((response) => {
                    ret.items = ret.items.concat(response.data.results);
                    ret.total = response.data.count;

                    offset += response.data.results.length;
                    hasMore = response.data.next !== null;
                }).catch((error) => {
                    hasMore = false;
                    console.log(error);
                });
            } while (hasMore && (itemsPerPage === -1 || ret.items.length < itemsPerPage));

            // Only return the requested number of items at max
            if (itemsPerPage !== -1) {
                ret.items = ret.items.slice(0, itemsPerPage);
            }

            return ret;
        }
    },
})