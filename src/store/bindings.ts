import { defineStore } from 'pinia'
import {APIUtils} from "@/classes/util/APIUtils";
import {SystemStatistics} from "@/types/SystemStatistics";

export const useBindingsStore = defineStore("bindings", {
    state: () => ({}),

    actions: {
        /**
         * Fetches a page of device bindings from the API.
         *
         * @param page Number of the page to fetch.
         * @param itemsPerPage Number of items per page.
         * @param sortBy Field to sort by.
         * @param search Search string to filter by.
         */
        async fetchBindingsPage(page: number, itemsPerPage: number, sortBy: any[], search: string) {
            return APIUtils.fetchPage('/item_bindings/', page, itemsPerPage, sortBy, search);
        },

        /**
         * Fetches statistical information from the API.
         *
         * @return Object containing statistical information.
         */
        async fetchStatistics(): Promise<SystemStatistics> {
            return await APIUtils.get('/statistics/').then(response => response.data);
        },

        /**
         * Creates new bindings between given items and the given user.
         *
         * @param userid ID of the user to bind the items to
         * @param itemIdsToBind IDs of the items to bind
         * @param itemTemplateIdsToBind IDs of quick add item templates to bind matching items
         *
         * @return API response. Created bindings on success.
         */
        async createBindings(userid: number, itemIdsToBind: number[], itemTemplateIdsToBind: number[]) {
            return APIUtils.post('/item_bindings/', {
                user_id: userid,
                item_ids: itemIdsToBind,
                item_template_ids: itemTemplateIdsToBind,
            });
        }
    },
})