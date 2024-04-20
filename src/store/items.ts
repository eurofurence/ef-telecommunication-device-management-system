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
         * Creates a new radio accessory templates via the API.
         *
         * @param templateId ID of the radio accessory template to create the radio accessory from.
         * @param serialnumber Serial number of the radio accessory.
         * @param notes Notes for the radio accessory.
         * @param amount Number of radio accessories to create.
         */
        async createRadioAccessories(templateId: number, serialnumber: string = '', notes: string = '', amount: number = 1) {
            return APIUtils.post('/radio_accessories/bulk/'+amount+'/', {
                template_id: templateId,
                serialnumber: serialnumber,
                notes: notes,
            });
        },

        /**
         * Deletes a single radio accessory via the API.
         *
         * @param radioAccessoryId ID of the radio accessory to delete.
         * @return API response. Empty on success.
         */
        async deleteRadioAccessory(radioAccessoryId: number) {
            return APIUtils.delete('/radio_accessories/', radioAccessoryId.toString());
        },

        /**
         * Deletes multiple radio accessories via the API.
         *
         * @param radioAccessoryIds IDs of the radio accessories to delete.
         * @return API response. Empty on success.
         */
        async deleteRadioAccessories(radioAccessoryIds: number[]) {
            return APIUtils.delete('/radio_accessories/bulk/', radioAccessoryIds.join(',') + '/');
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
         * Creates a new radio accessory template via the API.
         *
         * @param name Name of the radio accessory template.
         * @param ownerId ID of the owner of the radio accessory template.
         * @param description Description of the radio accessory template.
         * @param allow_quickadd Whether to allow quick adding of radio accessories.
         * @return API response. Created structure on success.
         */
        async createRadioAccessoryTemplate(name: string, ownerId: number, description: string = '', allow_quickadd: boolean = false) {
            return APIUtils.post('/radio_accessory_templates/', {
                name: name,
                owner_id: ownerId,
                description: description,
                allow_quickadd: allow_quickadd,
            });
        },

        /**
         * Deletes a single radio accessory template via the API.
         *
         * @param radioAccessoryTemplateId ID of the radio accessory template to delete.
         * @return API response. Empty on success.
         */
        async deleteRadioAccessoryTemplate(radioAccessoryTemplateId: number) {
            return APIUtils.delete('/radio_accessory_templates/', radioAccessoryTemplateId.toString());
        },

        /**
         * Deletes multiple radio accessory templates via the API.
         *
         * @param radioAccessoryTemplateIds IDs of the radio accessory templates to delete.
         * @return API response. Empty on success.
         */
        async deleteRadioAccessoryTemplates(radioAccessoryTemplateIds: number[]) {
            return APIUtils.delete('/radio_accessory_templates/bulk/', radioAccessoryTemplateIds.join(',') + '/');
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
         * Creates a new pager via the API.
         *
         * @param templateId ID of the pager template to create the pager from.
         * @param serialnumber Serial number of the pager.
         * @param notes Notes for the pager.
         * @return API response. Created structure on success.
         */
        async createPager(templateId: number, serialnumber: string = '', notes: string = '') {
            return APIUtils.post('/pagers/', {
                template_id: templateId,
                serialnumber: serialnumber,
                notes: notes,
            });
        },

        /**
         * Deletes a single pager via the API.
         *
         * @param pagerId ID of the pager to delete.
         * @return API response. Empty on success.
         */
        async deletePager(pagerId: number) {
            return APIUtils.delete('/pagers/', pagerId.toString());
        },

        /**
         * Deletes multiple pagers via the API.
         *
         * @param pagerIds IDs of the pagers to delete.
         * @return API response. Empty on success.
         */
        async deletePagers(pagerIds: number[]) {
            return APIUtils.delete('/pagers/bulk/', pagerIds.join(',') + '/');
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
         * Creates a new pager template via the API.
         *
         * @param name Name of the pager template.
         * @param ownerId ID of the owner of the pager template.
         * @param description Description of the pager template.
         * @return API response. Created structure on success.
         */
        async createPagerTemplate(name: string, ownerId: number, description: string = '') {
            return APIUtils.post('/pager_templates/', {
                name: name,
                owner_id: ownerId,
                description: description,
            });
        },

        /**
         * Deletes a single pager template via the API.
         *
         * @param pagerTemplateId ID of the pager template to delete.
         * @return API response. Empty on success.
         */
        async deletePagerTemplate(pagerTemplateId: number) {
            return APIUtils.delete('/pager_templates/', pagerTemplateId.toString());
        },

        /**
         * Deletes multiple pager templates via the API.
         *
         * @param pagerTemplateIds IDs of the pager templates to delete.
         * @return API response. Empty on success.
         */
        async deletePagerTemplates(pagerTemplateIds: number[]) {
            return APIUtils.delete('/pager_templates/bulk/', pagerTemplateIds.join(',') + '/');
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