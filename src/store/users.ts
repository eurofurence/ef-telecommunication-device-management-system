import { defineStore } from 'pinia'
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
         * @param search Search string to filter by.
         */
        async fetchUsersPage(page: number, itemsPerPage: number, sortBy: any[], search: string) {
            return APIUtils.fetchPage('/users/', page, itemsPerPage, sortBy, search);
        },

        /**
         * Fetches a page of item owners from the API.
         *
         * @param page Number of the page to fetch.
         * @param itemsPerPage Number of items per page.
         * @param sortBy Field to sort by.
         * @param search Search string to filter by.
         */
        async fetchItemOwnersPage(page: number, itemsPerPage: number, sortBy: any[], search: string) {
            return APIUtils.fetchPage('/item_owners/', page, itemsPerPage, sortBy, search);
        }
    },
})