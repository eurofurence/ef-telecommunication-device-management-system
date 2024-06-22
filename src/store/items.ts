import { defineStore } from 'pinia'
import {APIUtils} from "@/classes/util/APIUtils";

export const useItemsStore = defineStore("item", {
    state: () => ({}),

    actions: {
        /**
         * Fetches a page of item metadata from the API.
         *
         * @param page Number of the page to fetch.
         * @param itemsPerPage Number of items per page.
         * @param sortBy Field to sort by.
         * @param search Search string to filter by.
         */
        async fetchItemMetadataPage(page: number, itemsPerPage: number, sortBy: any[], search: string) {
            return APIUtils.fetchPage('/item_metadata/', page, itemsPerPage, sortBy, search);
        },

        /**
         * Fetches a single item metadata from the API.
         *
         * @param itemId ID of the item metadata to fetch.
         * @return API response. Item metadata structure on success.
         */
        async fetchItemMetadata(itemId: number) {
            return APIUtils.get('/item_metadata/' + itemId.toString() + '/');
        },

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
         * Updates a radio device via the API.
         *
         * @param radioId ID of the radio device to update.
         * @param templateId ID of the radio template to update the radio device to.
         * @param callsign Callsign of the radio device.
         * @param serialnumber Serial number of the radio device.
         * @param notes Notes for the radio device.
         */
        async updateRadio(radioId: number, templateId: number, callsign: string = '', serialnumber: string = '', notes: string = '') {
            return APIUtils.patch('/radios/' + radioId + '/', {
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
         * @param priv Whether the radio template is private.
         * @param description Description of the radio template.
         * @return API response. Created structure on success.
         */
        async createRadioTemplate(name: string, ownerId: number, codingId: number, priv: boolean = false, description: string = '') {
            return APIUtils.post('/radio_templates/', {
                name: name,
                owner_id: ownerId,
                private: priv,
                coding_id: codingId,
                description: description,
            });
        },

        /**
         * Updates a radio device template via the API.
         *
         * @param templateId ID of the radio device template to update.
         * @param name Name of the radio device template.
         * @param ownerId ID of the owner of the radio device template.
         * @param codingId ID of the coding of the radio device template.
         * @param priv Whether the radio device template is private.
         * @param description Description of the radio device template.
         */
        async updateRadioTemplate(templateId: number, name: string, ownerId: number, codingId: number, priv: boolean = false, description: string = '') {
            return APIUtils.patch('/radio_templates/' + templateId + '/', {
                name: name,
                owner_id: ownerId,
                private: priv,
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
         * Updates a radio accessory via the API.
         *
         * @param radioAccessoryId ID of the radio accessory to update.
         * @param templateId ID of the radio accessory template to update the radio accessory to.
         * @param serialnumber Serial number of the radio accessory.
         * @param notes Notes for the radio accessory.
         */
        async updateRadioAccessory(radioAccessoryId: number, templateId: number, serialnumber: string = '', notes: string = '') {
            return APIUtils.patch('/radio_accessories/' + radioAccessoryId + '/', {
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
         * @param priv Whether the radio accessory template is private.
         * @param description Description of the radio accessory template.
         * @param allow_quickadd Whether to allow quick adding of radio accessories.
         * @return API response. Created structure on success.
         */
        async createRadioAccessoryTemplate(name: string, ownerId: number, priv: boolean = false, description: string = '', allow_quickadd: boolean = false) {
            return APIUtils.post('/radio_accessory_templates/', {
                name: name,
                owner_id: ownerId,
                private: priv,
                description: description,
                allow_quickadd: allow_quickadd,
            });
        },

        /**
         * Updates a radio accessory template via the API.
         *
         * @param templateId ID of the radio accessory template to update.
         * @param name Name of the radio accessory template.
         * @param ownerId ID of the owner of the radio accessory template.
         * @param priv Whether the radio accessory template is private.
         * @param description Description of the radio accessory template.
         * @param allow_quickadd Whether to allow quick adding of radio accessories.
         */
        async updateRadioAccessoryTemplate(templateId: number, name: string, ownerId: number, priv: boolean = false, description: string = '', allow_quickadd: boolean = false) {
            return APIUtils.patch('/radio_accessory_templates/' + templateId + '/', {
                name: name,
                owner_id: ownerId,
                private: priv,
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
         * Updates a pager via the API.
         *
         * @param pagerId ID of the pager to update.
         * @param templateId ID of the pager template to update the pager to.
         * @param serialnumber Serial number of the pager.
         * @param notes Notes for the pager.
         */
        async updatePager(pagerId: number, templateId: number, serialnumber: string = '', notes: string = '') {
            return APIUtils.patch('/pagers/' + pagerId + '/', {
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
         * @param priv Whether the pager template is private.
         * @param description Description of the pager template.
         * @return API response. Created structure on success.
         */
        async createPagerTemplate(name: string, ownerId: number, priv: boolean = false, description: string = '') {
            return APIUtils.post('/pager_templates/', {
                name: name,
                owner_id: ownerId,
                private: priv,
                description: description,
            });
        },

        /**
         * Updates a pager template via the API.
         *
         * @param templateId ID of the pager template to update.
         * @param name Name of the pager template.
         * @param ownerId ID of the owner of the pager template.
         * @param priv Whether the pager template is private.
         * @param description Description of the pager template.
         */
        async updatePagerTemplate(templateId: number, name: string, ownerId: number, priv: boolean = false, description: string = '') {
            return APIUtils.patch('/pager_templates/' + templateId + '/', {
                name: name,
                owner_id: ownerId,
                private: priv,
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
         * Creates a new phone via the API.
         *
         * @param templateId ID of the phone template to create the phone from.
         * @param extension Extension of the phone.
         * @param network Network the phone is on.
         * @param dhcp Whether the phone uses DHCP.
         * @param ip_address IP address of the phone.
         * @param mac_address MAC address of the phone.
         * @param location Location of the phone.
         * @param serialnumber Serial number of the phone.
         * @param notes Notes for the phone.
         * @return API response. Created structure on success.
         */
        async createPhone(
            templateId: number,
            extension: string = '',
            network: string = '',
            dhcp: boolean|null = null,
            ip_address: string|null = null,
            mac_address: string|null = null,
            location: string|null = null,
            serialnumber: string|null = null,
            notes: string|null = null
        ) {
            return APIUtils.post('/phones/', {
                template_id: templateId,
                extension: extension,
                network: network,
                dhcp: dhcp,
                ip_address: ip_address || null,
                mac_address: mac_address || null,
                location: location,
                serialnumber: serialnumber,
                notes: notes,
            });
        },

        /**
         * Deletes a single phone via the API.
         *
         * @param phoneId ID of the phone to delete.
         * @return API response. Empty on success.
         */
        async deletePhone(phoneId: number) {
            return APIUtils.delete('/phones/', phoneId.toString());
        },

        /**
         * Deletes multiple phones via the API.
         *
         * @param phoneIds IDs of the phones to delete.
         * @return API response. Empty on success.
         */
        async deletePhones(phoneIds: number[]) {
            return APIUtils.delete('/phones/bulk/', phoneIds.join(',') + '/');
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
         * Creates a new phone template via the API.
         *
         * @param name Name of the phone template.
         * @param ownerId ID of the owner of the phone template.
         * @param description Description of the phone template.
         * @return API response. Created structure on success.
         */
        async createPhoneTemplate(name: string, ownerId: number, priv: boolean = false, description: string = '') {
            return APIUtils.post('/phone_templates/', {
                name: name,
                owner_id: ownerId,
                private: priv,
                description: description,
            });
        },

        /**
         * Deletes a single phone template via the API.
         *
         * @param phoneTemplateId ID of the phone template to delete.
         * @return API response. Empty on success.
         */
        async deletePhoneTemplate(phoneTemplateId: number) {
            return APIUtils.delete('/phone_templates/', phoneTemplateId.toString());
        },

        /**
         * Deletes multiple phone templates via the API.
         *
         * @param phoneTemplateIds IDs of the phone templates to delete.
         * @return API response. Empty on success.
         */
        async deletePhoneTemplates(phoneTemplateIds: number[]) {
            return APIUtils.delete('/phone_templates/bulk/', phoneTemplateIds.join(',') + '/');
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
         * Creates a new callbox via the API.
         *
         * @param templateId ID of the callbox template to create the callbox from.
         * @param extension Extension of the phone.
         * @param network Network the callbox is on.
         * @param dhcp Whether the phone uses DHCP.
         * @param ip_address IP address of the phone.
         * @param mac_address MAC address of the phone.
         * @param location Location of the phone.
         * @param has_camera Whether the phone has a camera.
         * @param camera_network Network the camera is on.
         * @param camera_dhcp Whether the camera uses DHCP.
         * @param camera_ip_address IP address of the camera.
         * @param camera_mac_address MAC address of the camera.
         * @param serialnumber Serial number of the phone.
         * @param notes Notes for the phone.
         * @return API response. Created structure on success.
         */
        async createCallbox(
            templateId: number,
            extension: string = '',
            network: string = '',
            dhcp: boolean|null = null,
            ip_address: string|null = null,
            mac_address: string|null = null,
            location: string|null = null,
            has_camera: boolean|null = null,
            camera_network: string|null = null,
            camera_dhcp: boolean|null = null,
            camera_ip_address: string|null = null,
            camera_mac_address: string|null = null,
            serialnumber: string|null = null,
            notes: string|null = null
        ) {
            return APIUtils.post('/callboxes/', {
                template_id: templateId,
                extension: extension,
                network: network,
                dhcp: dhcp,
                ip_address: ip_address || null,
                mac_address: mac_address || null,
                location: location,
                has_camera: has_camera,
                camera_network: camera_network,
                camera_dhcp: camera_dhcp,
                camera_ip_address: camera_ip_address || null,
                camera_mac_address: camera_mac_address || null,
                serialnumber: serialnumber,
                notes: notes,
            });
        },

        /**
         * Deletes a single callbox via the API.
         *
         * @param callboxId ID of the callbox to delete.
         * @return API response. Empty on success.
         */
        async deleteCallbox(callboxId: number) {
            return APIUtils.delete('/callboxes/', callboxId.toString());
        },

        /**
         * Deletes multiple callboxes via the API.
         *
         * @param callboxIds IDs of the callboxes to delete.
         * @return API response. Empty on success.
         */
        async deleteCallboxes(callboxIds: number[]) {
            return APIUtils.delete('/callboxes/bulk/', callboxIds.join(',') + '/');
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
         * Creates a new callbox template via the API.
         *
         * @param name Name of the callbox template.
         * @param ownerId ID of the owner of the callbox template.
         * @param priv Whether the callbox template is private.
         * @param description Description of the callbox template.
         * @return API response. Created structure on success.
         */
        async createCallboxTemplate(name: string, ownerId: number, priv: boolean = false, description: string = '') {
            return APIUtils.post('/callbox_templates/', {
                name: name,
                owner_id: ownerId,
                private: priv,
                description: description,
            });
        },

        /**
         * Deletes a single callbox template via the API.
         *
         * @param callboxTemplateId ID of the callbox template to delete.
         * @return API response. Empty on success.
         */
        async deleteCallboxTemplate(callboxTemplateId: number) {
            return APIUtils.delete('/callbox_templates/', callboxTemplateId.toString());
        },

        /**
         * Deletes multiple callbox templates via the API.
         *
         * @param callboxTemplateIds IDs of the callbox templates to delete.
         * @return API response. Empty on success.
         */
        async deleteCallboxTemplates(callboxTemplateIds: number[]) {
            return APIUtils.delete('/callbox_templates/bulk/', callboxTemplateIds.join(',') + '/');
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
         * Updates a radio coding via the API.
         *
         * @param radioCodingId ID of the radio coding to update
         * @param name Name of the radio coding
         * @param color Color of the radio coding in hex format
         * @param description Description of the radio coding
         */
        async updateRadioCoding(radioCodingId: number, name: string, color: string, description: string = '') {
            return APIUtils.patch('/radio_codings/' + radioCodingId + '/', {
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

        /**
         * Fetches item coordinates for a given floor.
         *
         * @param floor Floor to fetch item coordinates for.
         * @return Items with their coordinates for the given floor.
         */
        async fetchItemCoordinatesForFloor(floor: number) {
            if (isNaN(floor) || floor < 0 || floor > 99) {
                return [];
            }

            return APIUtils.fetchPage(`/item_coordinates/floor/${floor}`, 1, 9999, [], '');
        }
    },
})