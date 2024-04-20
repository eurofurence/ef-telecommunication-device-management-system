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
         * Creates a new radio device via the API.
         *
         * @param templateId ID of the radio template to create the radio from.
         * @param callsign Callsign of the radio device.
         * @param serialnumber Serial number of the radio device.
         * @param notes Notes for the radio device.
         * @return API response. Created structure on success.
         */
        async createRadio(templateId: number, callsign: string = '', serialnumber: string = '', notes: string = '') {
            return APIUtils.post('/radios/', {
                template_id: templateId,
                callsign: callsign,
                serialnumber: serialnumber,
                notes: notes,
            });
        },

        /**
         * Deletes a single radio device via the API.
         *
         * @param radioId ID of the radio device to delete.
         * @return API response. Empty on success.
         */
        async deleteRadio(radioId: number) {
            return APIUtils.delete('/radios/', radioId.toString());
        },

        /**
         * Deletes multiple radio devices via the API.
         *
         * @param radioIds IDs of the radio devices to delete.
         * @return API response. Empty on success.
         */
        async deleteRadios(radioIds: number[]) {
            return APIUtils.delete('/radios/bulk/', radioIds.join(',') + '/');
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
         * Creates a new radio device template via the API.
         *
         * @param name Name of the radio template.
         * @param ownerId ID of the owner of the radio template.
         * @param codingId ID of the coding of the radio template.
         * @param description Description of the radio template.
         * @return API response. Created structure on success.
         */
        async createRadioTemplate(name: string, ownerId: number, codingId: number, description: string = '') {
            return APIUtils.post('/radio_templates/', {
                name: name,
                owner_id: ownerId,
                coding_id: codingId,
                description: description,
            });
        },

        /**
         * Deletes a single radio device template via the API.
         *
         * @param radioId ID of the radio device template to delete.
         * @return API response. Empty on success.
         */
        async deleteRadioTemplate(radioId: number) {
            return APIUtils.delete('/radio_templates/', radioId.toString());
        },

        /**
         * Deletes multiple radio device templates via the API.
         *
         * @param radioTemplateIds IDs of the radio device templates to delete.
         * @return API response. Empty on success.
         */
        async deleteRadioTemplates(radioTemplateIds: number[]) {
            return APIUtils.delete('/radio_templates/bulk/', radioTemplateIds.join(',') + '/');
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

        /**
         * Creates a new radio coding via the API.
         *
         * @param name Name of the radio coding
         * @param color Color of the radio coding in hex format
         * @param description Description of the radio coding
         */
        async createRadioCoding(name: string, color: string, description: string = '') {
            return APIUtils.post('/radio_codings/', {
                name: name,
                color: color,
                description: description,
            });
        },

        /**
         * Deletes a single radio coding via the API.
         *
         * @param radioCodingId ID of the radio coding to delete.
         * @return API response. Empty on success.
         */
        async deleteRadioCoding(radioCodingId: number) {
            return APIUtils.delete('/radio_codings/', radioCodingId.toString());
        },

        /**
         * Deletes multiple radio codings via the API.
         *
         * @param radioCodingIds IDs of the radio codings to delete.
         * @return API response. Empty on success.
         */
        async deleteRadioCodings(radioCodingIds: number[]) {
            return APIUtils.delete('/radio_codings/bulk/', radioCodingIds.join(',') + '/');
        },
    },
})