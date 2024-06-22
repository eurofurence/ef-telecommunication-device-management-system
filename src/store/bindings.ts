/* Eurofurence Telecommunication Device Management System (EF-TDMS)
 * Copyright (C) 2024 Niels Gandraß <niels@gandrass.de>
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
         * Fetches a bindings metadata by the given item id.
         *
         * @param itemId ID of the item to fetch the binding for.
         * @return Binding metadata (HTTP 200) for the given item or empty object
         * (HTTP 404) if no binding exists.
         */
        async fetchBindingByItemId(itemId: number) {
            return APIUtils.get('/item_bindings/item/' + itemId + '/');
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

        /**
         * Creates a new order via the API.
         *
         * @param userId ID of the user to create this order for.
         * @param type Type of the ordered item.
         * @param title Title of the order.
         * @param itemId Optional ID of an exact item to order.
         * @param itemTemplateId Optional ID of an item template the ordered
         * item should belong to.
         */
        async createOrder(userId: number, type: string, title: string, itemId: number|null = null, itemTemplateId: number|null = null) {
            return APIUtils.post('/orders/', {
                user_id: userId,
                type: type,
                title: title,
                item_id: itemId,
                item_template_id: itemTemplateId,
            });
        },

        /**
         * Updates an existing order via the API.
         *
         * @param orderId ID of the order to update.
         * @param userId ID of the user this order is for.
         * @param type Type of the ordered item.
         * @param title Title of the order.
         * @param itemId Optional ID of an exact item to order.
         * @param itemTemplateId Optional ID of an item template the ordered
         */
        async updateOrder(orderId: number, userId: number, type: string, title: string, itemId: number|null = null, itemTemplateId: number|null = null) {
            return APIUtils.patch('/orders/' + orderId + '/', {
                user_id: userId,
                type: type,
                title: title,
                item_id: itemId,
                item_template_id: itemTemplateId,
            });
        },

        /**
         * Deletes a single order via the API.
         *
         * @param orderId ID of the order to delete.
         * @return API response. Empty on success.
         */
        async deleteOrder(orderId: number) {
            return APIUtils.delete('/orders/', orderId.toString());
        },

        /**
         * Bulk deletes orders via the API.
         *
         * @param orderIds List of order IDs to delete.
         * @return API response. Empty on success.
         */
        async deleteOrders(orderIds: number[]) {
            return APIUtils.delete('/orders/bulk/', orderIds.join(',') + '/');
        },
    },
})