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
         */
        async fetchEventLogsPage(page: number, itemsPerPage: number, sortBy: any[], search: string) {
            return APIUtils.fetchPage('/eventlog/', page, itemsPerPage, sortBy, search);
        },
    },
})