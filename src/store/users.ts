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
         * @return Page of users.
         */
        async fetchUsersPage(page: number, itemsPerPage: number, sortBy: any[], search: string) {
            return APIUtils.fetchPage('/users/', page, itemsPerPage, sortBy, search);
        },

        /**
         * Fetches a page of users that have an item bound that matches the
         * given callsign.
         *
         * @param page Number of the page to fetch.
         * @param itemsPerPage Number of items per page.
         * @param sortBy Field to sort by.
         * @param search Search string to filter by.
         * @return Page of users that have an item bound that matches the given callsign.
         */
        async fetchUsersPageByCallsign(page: number, itemsPerPage: number, sortBy: any[], search: string) {
            const ret = {
                items: [],
                total: 0,
            }

            await APIUtils.get('/users/callsign/' + search + '/').then((response) => {
                ret.items = response.data;
                ret.total = response.data.length;
            }).catch((error) => {
                console.error(error);
            });

            return ret;
        },

        /**
         * Fetches a page of item owners from the API.
         *
         * @param page Number of the page to fetch.
         * @param itemsPerPage Number of items per page.
         * @param sortBy Field to sort by.
         * @param search Search string to filter by.
         * @return Page of item owners.
         */
        async fetchItemOwnersPage(page: number, itemsPerPage: number, sortBy: any[], search: string) {
            return APIUtils.fetchPage('/item_owners/', page, itemsPerPage, sortBy, search);
        },

        /**
         * Creates a new item owner via the API.
         *
         * @param name Full name of the item owner
         * @param shortname Short name of the item owner
         */
        async createItemOwner(name: string, shortname: string) {
            return APIUtils.post('/item_owners/', {
                name: name,
                shortname: shortname,
            });
        },

        /**
         * Deletes a single item owner via the API.
         *
         * @param itemOwnerId ID of the item owner to delete.
         * @return API response. Empty on success.
         */
        async deleteItemOwner(itemOwnerId: number) {
            return APIUtils.delete('/item_owners/', itemOwnerId.toString());
        },

        /**
         * Bulk deletes item owners via the API.
         *
         * @param itemOwnerIds List of item owner IDs to delete.
         * @return API response. Empty on success.
         */
        async deleteItemOwners(itemOwnerIds: number[]) {
            return APIUtils.delete('/item_owners/bulk/', itemOwnerIds.join(',') + '/');
        }
    },
})