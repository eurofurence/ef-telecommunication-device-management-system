<!--
Eurofurence Telecommunication Device Management System (EF-TDMS)
Copyright (C) 2025 Niels Gandraß <niels@gandrass.de>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
-->

<template>
    <ItemOverview
        ref="itemOverview"
        title="VoIP Phones"
        icon="mdi-phone"
        :items-table="itemsTable"
        :templates-table="templatesTable"
        @click:create-item="itemFormData = null; showItemEditForm = true"
        @click:edit-item="itemFormData = $event; showItemEditForm = true"
        @click:delete-items="deletePhones"
        @click:create-item-template="templateFormData = null; showTemplateEditForm = true"
        @click:edit-item-template="templateFormData = $event; showTemplateEditForm = true"
        @click:delete-item-templates="deletePhoneTemplates"
    />

    <v-dialog v-model="showItemEditForm" max-width="560">
        <VoipPhoneForm
            :item="itemFormData"
            @abort="showItemEditForm = false"
            @submit="itemFormData ? updatePhone($event) : createPhone($event)"
        />
    </v-dialog>

    <v-dialog v-model="showTemplateEditForm" max-width="560">
        <VoipPhoneTemplateForm
            :item="templateFormData"
            @abort="showTemplateEditForm = false"
            @submit="templateFormData ? updatePhoneTemplate($event) : createPhoneTemplate($event)"
        />
    </v-dialog>
</template>

<script lang="ts">
import {useToast} from "vue-toastification";
import {useItemsStore} from "@/store/items";
import ItemOverview from "@/components/ItemOverview.vue";
import VoipPhoneForm from "@/components/forms/VoipPhoneForm.vue";
import VoipPhoneTemplateForm from "@/components/forms/VoipPhoneTemplateForm.vue";
import {APIUtils} from "@/classes/util/APIUtils";

const itemsStore = useItemsStore();
const toast = useToast();

export default {
    name: "VoipPhones",

    components: {
        VoipPhoneTemplateForm,
        VoipPhoneForm,
        ItemOverview
    },

    data: () => ({
        itemsTable: {
            headers: [
                {key: 'id', title: 'ID', align: 'start', sortable: true},
                {key: 'template.name', title: 'Type', align: 'start', sortable: true},
                {key: 'extension', title: 'Extension', align: 'start', sortable: true},
                {key: 'notes', title: 'Notes', align: 'start', sortable: false},
                {key: 'location', title: 'Location', align: 'start', sortable: true},
                {key: 'template.owner.shortname', title: 'Owner', align: 'start', sortable: true},
                {key: 'handed_out', title: 'Status', align: 'start', sortable: false},
            ],
            expandedRowProps: [
                {key: 'template.owner.name', title: 'Owner'},
                {key: 'network', title: 'Network'},
                {key: 'dhcp', title: 'DHCP'},
                {key: 'ip_address', title: 'IP Address'},
                {key: 'mac_address', title: 'MAC Address'},
                {key: 'created_at', title: 'Created at'},
                {key: 'updated_at', title: 'Updated at'},
            ],
            fetchFunction: itemsStore.fetchPhonesPage,
            alwaysShowMapButton: true,
        },
        templatesTable: {
            headers: [
                {key: 'id', title: 'ID', align: 'start', sortable: true},
                {key: 'name', title: 'Name', align: 'start', sortable: true},
                {key: 'description', title: 'Description', align: 'start', sortable: true},
                {key: 'owner.name', title: 'Owner', align: 'start', sortable: true},
                {key: 'private', title: 'Private', align: 'start', sortable: true},
            ],
            fetchFunction: itemsStore.fetchPhoneTemplatesPage,
        },
        itemFormData: null as any,
        showItemEditForm: false,
        templateFormData: null as any,
        showTemplateEditForm: false,
    }),

    methods: {
        deletePhones(phoneIds: number[]) {
            // TODO: Replace with proper dialog
            if (confirm("Are you sure you want to delete the selected phones?")) {
                itemsStore.deletePhones(phoneIds)
                    .then((resp) => {
                        toast.success("Deleted " + phoneIds.length + " phone(s)");
                    })
                    .catch((error) => {
                        toast.error("Failed to delete phone(s).\r\n" + APIUtils.createErrorToString(error));
                        console.error("Failed to delete phone(s):", error);
                    });

                // Deselect deleted items and force re-render of table
                (this.$refs.itemOverview as InstanceType<typeof ItemOverview>).deselectItemsByKey(phoneIds);
                (this.$refs.itemOverview as InstanceType<typeof ItemOverview>).reloadItems();
            }
        },

        createPhone(data: any) {
            // Check received data
            if (data === null) {
                console.error("Received null data from VoipPhoneForm.");
                toast.error("Failed to create phone.\r\nReceived no data.");
                return;
            }

            if (!data.template || !data.template.id || !data.extension || !data.network || data.dhcp === null ||
                (data.has_coordinates && (data.coordinates.floor < 0 || data.coordinates.latitude < 0 || data.coordinates.longitude < 0)))
            {
                console.error("Received incomplete data from VoipPhoneForm:", data);
                toast.error("Failed to create phone.\r\nReceived incomplete data.");
                return;
            }

            // Create phone
            itemsStore.createPhone(
                data.template.id,
                data.extension,
                data.network,
                data.dhcp,
                data.ip_address,
                data.mac_address,
                data.location,
                data.serialnumber,
                data.notes,
                data.has_coordinates ? data.coordinates : null
            )
                .then((resp) => {
                    toast.success("Created new phone:\r\n" + resp.data.pretty_name);
                    this.showItemEditForm = false;
                    (this.$refs.itemOverview as InstanceType<typeof ItemOverview>).reloadItems();
                })
                .catch((error) => {
                    console.error("Failed to create phone:", error);
                    toast.error("Failed to create phone.\r\n" + APIUtils.createErrorToString(error));
                });
        },

        updatePhone(data: any) {
            // Check received data
            if (data === null) {
                console.error("Received null data from VoipPhoneForm.");
                toast.error("Failed to update phone.\r\nReceived no data.");
                return;
            }

            if (!data.id) {
                console.error("Received incomplete data from VoipPhoneForm:", data);
                toast.error("Failed to update phone.\r\nMissing ID.");
                return;
            }

            if (!data.template || !data.template.id || !data.extension || !data.network || data.dhcp === null ||
                (data.has_coordinates && (data.coordinates.floor < 0 || data.coordinates.latitude < 0 || data.coordinates.longitude < 0)))
            {
                console.error("Received incomplete data from VoipPhoneForm:", data);
                toast.error("Failed to update phone.\r\nReceived incomplete data.");
                return;
            }

            // Update phone
            itemsStore.updatePhone(
                data.id,
                data.template.id,
                data.extension,
                data.network,
                data.dhcp,
                data.ip_address,
                data.mac_address,
                data.location,
                data.serialnumber,
                data.notes,
                data.has_coordinates ? data.coordinates : null
            )
                .then((resp) => {
                    toast.success("Updated phone:\r\n" + resp.data.pretty_name);
                    this.showItemEditForm = false;
                    (this.$refs.itemOverview as InstanceType<typeof ItemOverview>).reloadItems();
                })
                .catch((error) => {
                    console.error("Failed to update phone:", error);
                    toast.error("Failed to update phone.\r\n" + APIUtils.createErrorToString(error));
                });
        },

        deletePhoneTemplates(phoneTemplateIds: number[]) {
            // TODO: Replace with proper dialog
            if (confirm("Are you sure you want to delete the selected phone template(s)?")) {
                itemsStore.deletePhoneTemplates(phoneTemplateIds)
                    .then((resp) => {
                        toast.success("Deleted " + phoneTemplateIds.length + " phone template(s)");
                    })
                    .catch((error) => {
                        toast.error("Failed to delete phone template(s).\r\n" + APIUtils.createErrorToString(error));
                        console.error("Failed to delete phone template(s):", error);
                    });

                // Deselect deleted items and force re-render of table
                (this.$refs.itemOverview as InstanceType<typeof ItemOverview>).deselectTemplatesByKey(phoneTemplateIds);
                (this.$refs.itemOverview as InstanceType<typeof ItemOverview>).reloadTemplates();
            }
        },

        createPhoneTemplate(data: any) {
            // Check received data
            if (data === null) {
                console.error("Received null data from VoipPhoneTemplateForm.");
                toast.error("Failed to create phone template.\r\nReceived no data.");
                return;
            }

            if (!data.name || data.name.length < 1 || !data.owner || !data.owner.id || data.private === undefined) {
                console.error("Received incomplete data from VoipPhoneTemplateForm:", data);
                toast.error("Failed to create phone template.\r\nReceived incomplete data.");
                return;
            }

            // Create phone template
            itemsStore.createPhoneTemplate(data.name, data.owner.id, data.private, data.description)
                .then((resp) => {
                    toast.success("Created new phone template:\r\n" + resp.data.pretty_name);
                    this.showTemplateEditForm = false;
                    (this.$refs.itemOverview as InstanceType<typeof ItemOverview>).reloadTemplates();
                })
                .catch((error) => {
                    console.error("Failed to create phone template:", error);
                    toast.error("Failed to create phone template.\r\n" + APIUtils.createErrorToString(error));
                });
        },

        updatePhoneTemplate(data: any) {
            // Check received data
            if (data === null) {
                console.error("Received null data from VoipPhoneTemplateForm.");
                toast.error("Failed to update phone template.\r\nReceived no data.");
                return;
            }

            if (!data.id) {
                console.error("Received incomplete data from VoipPhoneTemplateForm:", data);
                toast.error("Failed to update phone template.\r\nMissing ID.");
                return;
            }

            if (!data.name || data.name.length < 1 || !data.owner || !data.owner.id || data.private === undefined) {
                console.error("Received incomplete data from VoipPhoneTemplateForm:", data);
                toast.error("Failed to update phone template.\r\nReceived incomplete data.");
                return;
            }

            // Update phone template
            itemsStore.updatePhoneTemplate(data.id, data.name, data.owner.id, data.private, data.description)
                .then((resp) => {
                    toast.success("Updated phone template:\r\n" + resp.data.pretty_name);
                    this.showTemplateEditForm = false;
                    (this.$refs.itemOverview as InstanceType<typeof ItemOverview>).reloadTemplates();
                })
                .catch((error) => {
                    console.error("Failed to update phone template:", error);
                    toast.error("Failed to update phone template.\r\n" + APIUtils.createErrorToString(error));
                });
        },
    },
}
</script>
