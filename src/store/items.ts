import { defineStore } from 'pinia'
import {APIUtils} from "@/classes/util/APIUtils";

export const useItemsStore = defineStore("item", {
    state: () => ({}),

    actions: {
        /**
         * Fetches a page of radio devices from the API.
         *
         * @param page Number of the page to fetch.
         * @param itemsPerPage Number of items per page.
         * @param sortBy Field to sort by.
         * @param search Search string to filter by.
         */
        async fetchRadiosPage(page: number, itemsPerPage: number, sortBy: any[], search: string) {
            return APIUtils.fetchPage('/radios/', page, itemsPerPage, sortBy, search);
        },

        /**
         * Fetches a page of radio device templates from the API.
         *
         * @param page Number of the page to fetch.
         * @param itemsPerPage Number of items per page.
         * @param sortBy Field to sort by.
         * @param search Search string to filter by.
         */
        async fetchRadioTemplatesPage(page: number, itemsPerPage: number, sortBy: any[], search: string) {
            return APIUtils.fetchPage('/radio_templates/', page, itemsPerPage, sortBy, search);
        },

        /**
         * Fetches a page of radio accessories from the API.
         *
         * @param page Number of the page to fetch.
         * @param itemsPerPage Number of items per page.
         * @param sortBy Field to sort by.
         * @param search Search string to filter by.
         */
        async fetchRadioAccessoriesPage(page: number, itemsPerPage: number, sortBy: any[], search: string) {
            return APIUtils.fetchPage('/radio_accessories/', page, itemsPerPage, sortBy, search);
        },

        /**
         * Fetches a page of radio accessory templates from the API.
         *
         * @param page Number of the page to fetch.
         * @param itemsPerPage Number of items per page.
         * @param sortBy Field to sort by.
         * @param search Search string to filter by.
         */
        async fetchRadioAccessorieTemplatesPage(page: number, itemsPerPage: number, sortBy: any[], search: string) {
            return APIUtils.fetchPage('/radio_accessory_templates/', page, itemsPerPage, sortBy, search);
        },
    },
})