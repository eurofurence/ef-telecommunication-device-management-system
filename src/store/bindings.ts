import { defineStore } from 'pinia'
import {APIUtils} from "@/classes/util/APIUtils";

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
    },
})