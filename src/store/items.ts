import { defineStore } from 'pinia'
import {APIUtils} from "@/classes/util/APIUtils";

// TODO: Implement creation and deletion of items
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
         * @param availableOnly Whether to only fetch available radios.
         */
        async fetchRadiosPage(page: number, itemsPerPage: number, sortBy: any[], search: string, availableOnly: boolean = false) {
            return APIUtils.fetchPage('/radios/'+(availableOnly ? 'available/' : ''), page, itemsPerPage, sortBy, search);
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
         * @param availableOnly Whether to only fetch available radio accessories.
         */
        async fetchRadioAccessoriesPage(page: number, itemsPerPage: number, sortBy: any[], search: string, availableOnly: boolean = false) {
            return APIUtils.fetchPage('/radio_accessories/'+(availableOnly ? 'available/' : ''), page, itemsPerPage, sortBy, search);
        },

        /**
         * Deletes a radio accessory item via the API.
         *
         * @param id ID of the radio accessory to delete.
         */
        async deleteRadioAccessory(id: number) {
            return APIUtils.delete('/radio_accessories/', id.toString());
        },

        /**
         * Fetches a page of radio accessory templates from the API.
         *
         * @param page Number of the page to fetch.
         * @param itemsPerPage Number of items per page.
         * @param sortBy Field to sort by.
         * @param search Search string to filter by.
         */
        async fetchRadioAccessoryTemplatesPage(page: number, itemsPerPage: number, sortBy: any[], search: string) {
            return APIUtils.fetchPage('/radio_accessory_templates/', page, itemsPerPage, sortBy, search);
        },

        /**
         * Fetches a page of pagers from the API.
         *
         * @param page Number of the page to fetch.
         * @param itemsPerPage Number of items per page.
         * @param sortBy Field to sort by.
         * @param search Search string to filter by.
         * @param availableOnly Whether to only fetch available pagers.
         */
        async fetchPagersPage(page: number, itemsPerPage: number, sortBy: any[], search: string, availableOnly: boolean = false) {
            return APIUtils.fetchPage('/pagers/'+(availableOnly ? 'available/' : ''), page, itemsPerPage, sortBy, search);
        },

        /**
         * Fetches a page of pager templates from the API.
         *
         * @param page Number of the page to fetch.
         * @param itemsPerPage Number of items per page.
         * @param sortBy Field to sort by.
         * @param search Search string to filter by.
         */
        async fetchPagerTemplatesPage(page: number, itemsPerPage: number, sortBy: any[], search: string) {
            return APIUtils.fetchPage('/pager_templates/', page, itemsPerPage, sortBy, search);
        },

        /**
         * Fetches a page of phones from the API.
         *
         * @param page Number of the page to fetch.
         * @param itemsPerPage Number of items per page.
         * @param sortBy Field to sort by.
         * @param search Search string to filter by.
         * @param availableOnly Whether to only fetch available phones.
         */
        async fetchPhonesPage(page: number, itemsPerPage: number, sortBy: any[], search: string, availableOnly: boolean = false) {
            return APIUtils.fetchPage('/phones/'+(availableOnly ? 'available/' : ''), page, itemsPerPage, sortBy, search);
        },

        /**
         * Fetches a page of phone templates from the API.
         *
         * @param page Number of the page to fetch.
         * @param itemsPerPage Number of items per page.
         * @param sortBy Field to sort by.
         * @param search Search string to filter by.
         */
        async fetchPhoneTemplatesPage(page: number, itemsPerPage: number, sortBy: any[], search: string) {
            return APIUtils.fetchPage('/phone_templates/', page, itemsPerPage, sortBy, search);
        },

        /**
         * Fetches a page of callboxes from the API.
         *
         * @param page Number of the page to fetch.
         * @param itemsPerPage Number of items per page.
         * @param sortBy Field to sort by.
         * @param search Search string to filter by.
         * @param availableOnly Whether to only fetch available callboxes.
         */
        async fetchCallboxesPage(page: number, itemsPerPage: number, sortBy: any[], search: string, availableOnly: boolean = false) {
            return APIUtils.fetchPage('/callboxes/'+(availableOnly ? 'available/' : ''), page, itemsPerPage, sortBy, search);
        },

        /**
         * Fetches a page of callbox templates from the API.
         *
         * @param page Number of the page to fetch.
         * @param itemsPerPage Number of items per page.
         * @param sortBy Field to sort by.
         * @param search Search string to filter by.
         */
        async fetchCallboxTemplatesPage(page: number, itemsPerPage: number, sortBy: any[], search: string) {
            return APIUtils.fetchPage('/callbox_templates/', page, itemsPerPage, sortBy, search);
        },

        /**
         * Fetches all quick add templates from the API.
         */
        async fetchQuickAddTemplates() {
            return APIUtils.fetchPage('/quickadd_templates/', 1, 9999, [], '');
        },

        /**
         * Fetches a page of radio codings from the API.
         *
         * @param page Number of the page to fetch.
         * @param itemsPerPage Number of items per page.
         * @param sortBy Field to sort by.
         * @param search Search string to filter by.
         */
        async fetchRadioCodingsPage(page: number, itemsPerPage: number, sortBy: any[], search: string) {
            return APIUtils.fetchPage('/radio_codings/', page, itemsPerPage, sortBy, search);
        },
    },
})