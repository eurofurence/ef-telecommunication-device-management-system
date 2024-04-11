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
         * Fetches all bindings for a given user from the API.
         *
         * @param userid ID of the user to fetch the bindings for.
         * @return List of item bindings for the given user.
         */
        async fetchBindingsForUser(userid: number) {
            return APIUtils.get('/item_bindings/user/' + userid + '/');
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
        },

        /**
         * Deletes a single item binding via the API.
         *
         * @param bindingId ID of the binding to delete.
         * @return API response. Empty on success.
         */
        async deleteBinding(bindingId: number) {
            return APIUtils.delete('/item_bindings/', bindingId.toString());
        },

        /**
         * Bulk deletes bindings via the API.
         *
         * @param bindingIds List of binding IDs to delete.
         * @return API response. Empty on success.
         */
        async deleteBindings(bindingIds: number[]) {
            return APIUtils.delete('/item_bindings/bulk/', bindingIds.join(',') + '/');
        },

        /**
         * Fetches a page of orders from the API.
         *
         * @param page Number of the page to fetch.
         * @param itemsPerPage Number of items per page.
         * @param sortBy Field to sort by.
         * @param search Search string to filter by.
         */
        async fetchOrdersPage(page: number, itemsPerPage: number, sortBy: any[], search: string) {
            return APIUtils.fetchPage('/orders/', page, itemsPerPage, sortBy, search);
        },

        /**
         * Fetches all orders for a given user from the API.
         *
         * @param userid ID of the user to fetch the orders for.
         */
        async fetchOrdersForUser(userid: number) {
            return APIUtils.get('/orders/user/' + userid + '/');
        },
    },
})