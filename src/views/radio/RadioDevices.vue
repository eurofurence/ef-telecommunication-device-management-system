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
        title="Radios"
        icon="mdi-cellphone-basic"
        :items-table="itemsTable"
        :templates-table="templatesTable"
        @click:create-item="itemFormData = null; showItemEditForm = true"
        @click:edit-item="itemFormData = $event; showItemEditForm = true"
        @click:delete-items="deleteRadios"
        @click:create-item-template="templateFormData = null; showTemplateEditForm = true"
        @click:edit-item-template="templateFormData = $event; showTemplateEditForm = true"
        @click:delete-item-templates="deleteRadioTemplates"
    />

    <v-dialog v-model="showItemEditForm" max-width="560">
        <RadioDeviceForm
            :item="itemFormData"
            @abort="showItemEditForm = false"
            @submit="itemFormData ? updateRadio($event) : createRadio($event)"
        />
    </v-dialog>

    <v-dialog v-model="showTemplateEditForm" max-width="560">
        <RadioDeviceTemplateForm
            :item="templateFormData"
            @abort="showTemplateEditForm = false"
            @submit="templateFormData ? updateRadioTemplate($event) : createRadioTemplate($event)"
        />
    </v-dialog>
</template>

<script lang="ts">
import {useToast} from "vue-toastification";
import {useItemsStore} from "@/store/items";
import ItemOverview from "@/components/ItemOverview.vue";
import RadioDeviceForm from "@/components/forms/RadioDeviceForm.vue";
import RadioDeviceTemplateForm from "@/components/forms/RadioDeviceTemplateForm.vue";
import {APIUtils} from "@/classes/util/APIUtils";

const itemsStore = useItemsStore();
const toast = useToast();

export default {
    name: "RadioDevices",

    components: {
        RadioDeviceForm,
        RadioDeviceTemplateForm,
        ItemOverview
    },

    data: () => ({
        itemsTable: {
            headers: [
                {key: 'id', title: 'ID', align: 'start', sortable: true},
                {key: 'template.name', title: 'Type', align: 'start', sortable: true},
                {key: 'template.coding', title: 'Coding', align: 'start', sortable: true},
                {key: 'template.owner.shortname', title: 'Owner', align: 'start', sortable: true},
                {key: 'callsign', title: 'Callsign', align: 'start', sortable: true},
                {key: 'serialnumber', title: 'S/N', align: 'start', sortable: true},
                {key: 'notes', title: 'Notes', align: 'start', sortable: false},
                {key: 'handed_out', title: 'Status', align: 'start', sortable: false},
            ],
            expandedRowProps: [
                {key: 'template.owner.name', title: 'Owner'},
                {key: 'created_at', title: 'Created at'},
                {key: 'updated_at', title: 'Updated at'},
            ],
            fetchFunction: itemsStore.fetchRadiosPage,
        },
        templatesTable: {
            headers: [
                {key: 'id', title: 'ID', align: 'start', sortable: true},
                {key: 'name', title: 'Template Name', align: 'start', sortable: true},
                {key: 'coding', title: 'Coding', align: 'start', sortable: true},
                {key: 'description', title: 'Description', align: 'start', sortable: true},
                {key: 'owner.name', title: 'Owner', align: 'start', sortable: true},
                {key: 'private', title: 'Private', align: 'start', sortable: true},
            ],
            fetchFunction: itemsStore.fetchRadioTemplatesPage,
        },
        itemFormData: null as any,
        showItemEditForm: false,
        templateFormData: null as any,
        showTemplateEditForm: false,
    }),

    methods: {
        deleteRadios(radioDeviceIds: number[]) {
            // TODO: Replace with proper dialog
            if (confirm("Are you sure you want to delete the selected radio devices?")) {
                itemsStore.deleteRadios(radioDeviceIds)
                    .then((resp) => {
                        toast.success("Deleted " + radioDeviceIds.length + " radio device(s)");
                    })
                    .catch((error) => {
                        toast.error("Failed to delete radio device(s).\r\n" + APIUtils.createErrorToString(error));
                        console.error("Failed to delete radio device(s):", error);
                    });

                // Deselect deleted items and force re-render of table
                (this.$refs.itemOverview as InstanceType<typeof ItemOverview>).deselectItemsByKey(radioDeviceIds);
                (this.$refs.itemOverview as InstanceType<typeof ItemOverview>).reloadItems();
            }
        },

        createRadio(data: any) {
            // Check received data
            if (data === null) {
                console.error("Received null data from RadioDeviceForm.");
                toast.error("Failed to create radio device.\r\nReceived no data.");
                return;
            }

            if (!data.template || !data.template.id || (data.has_coordinates && (data.coordinates.floor < 0 || data.coordinates.latitude < 0 || data.coordinates.longitude < 0))) {
                console.error("Received incomplete data from RadioDeviceForm:", data);
                toast.error("Failed to create radio device.\r\nReceived incomplete data.");
                return;
            }

            // Create radio
            itemsStore.createRadio(
                data.template.id,
                data.callsign,
                data.serialnumber,
                data.notes,
                data.has_coordinates ? data.coordinates : null,
            )
                .then((resp) => {
                    toast.success("Created new radio device:\r\n" + resp.data.pretty_name);
                    this.showItemEditForm = false;
                    (this.$refs.itemOverview as InstanceType<typeof ItemOverview>).reloadItems();
                })
                .catch((error) => {
                    console.error("Failed to create radio device:", error);
                    toast.error("Failed to create radio device.\r\n" + APIUtils.createErrorToString(error));
                });
        },

        updateRadio(data: any) {
            // Check received data
            if (data === null) {
                console.error("Received null data from RadioDeviceForm.");
                toast.error("Failed to edit radio device.\r\nReceived no data.");
                return;
            }

            if (!data.id) {
                console.error("Missing ID in received data from RadioDeviceForm:", data);
                toast.error("Failed to edit radio device.\r\nID is missing.");
            }

            if (!data.template || !data.template.id || (data.has_coordinates && (data.coordinates.floor < 0 || data.coordinates.latitude < 0 || data.coordinates.longitude < 0))) {
                console.error("Received incomplete data from RadioDeviceForm:", data);
                toast.error("Failed to edit radio device.\r\nReceived incomplete data.");
                return;
            }

            // Edit radio
            itemsStore.updateRadio(
                data.id,
                data.template.id,
                data.callsign,
                data.serialnumber,
                data.notes,
                data.has_coordinates ? data.coordinates : null,
            )
                .then((resp) => {
                    toast.success("Updated radio device:\r\n" + resp.data.pretty_name);
                    this.showItemEditForm = false;
                    (this.$refs.itemOverview as InstanceType<typeof ItemOverview>).reloadItems();
                })
                .catch((error) => {
                    console.error("Failed to edit radio device:", error);
                    toast.error("Failed to edit radio device.\r\n" + APIUtils.createErrorToString(error));
                });
        },

        deleteRadioTemplates(radioDeviceTemplateIds: number[]) {
            // TODO: Replace with proper dialog
            if (confirm("Are you sure you want to delete the selected radio device template(s)?")) {
                itemsStore.deleteRadioTemplates(radioDeviceTemplateIds)
                    .then((resp) => {
                        toast.success("Deleted " + radioDeviceTemplateIds.length + " radio device template(s)");
                    })
                    .catch((error) => {
                        toast.error("Failed to delete radio device template(s).\r\n" + APIUtils.createErrorToString(error));
                        console.error("Failed to delete radio device template(s):", error);
                    });

                // Deselect deleted items and force re-render of table
                (this.$refs.itemOverview as InstanceType<typeof ItemOverview>).deselectTemplatesByKey(radioDeviceTemplateIds);
                (this.$refs.itemOverview as InstanceType<typeof ItemOverview>).reloadTemplates();
            }
        },

        createRadioTemplate(data: any) {
            // Check received data
            if (data === null) {
                console.error("Received null data from RadioDeviceTemplateForm.");
                toast.error("Failed to create radio device template.\r\nReceived no data.");
                return;
            }

            if (!data.name || data.name.length < 1 || !data.owner || !data.owner.id || !data.coding || !data.coding.id || data.private === undefined) {
                console.error("Received incomplete data from RadioDeviceTemplateForm:", data);
                toast.error("Failed to create radio device template.\r\nReceived incomplete data.");
                return;
            }

            // Create radio template
            itemsStore.createRadioTemplate(data.name, data.owner.id, data.coding.id, data.private, data.description)
                .then((resp) => {
                    toast.success("Created new radio device template:\r\n" + resp.data.pretty_name);
                    this.showTemplateEditForm = false;
                    (this.$refs.itemOverview as InstanceType<typeof ItemOverview>).reloadTemplates();
                })
                .catch((error) => {
                    console.error("Failed to create radio device template:", error);
                    toast.error("Failed to create radio device template.\r\n" + APIUtils.createErrorToString(error));
                });
        },

        updateRadioTemplate(data: any) {
            // Check received data
            if (data === null) {
                console.error("Received null data from RadioDeviceTemplateForm.");
                toast.error("Failed to edit radio device template.\r\nReceived no data.");
                return;
            }

            if (!data.id) {
                console.error("Missing ID in received data from RadioDeviceTemplateForm:", data);
                toast.error("Failed to edit radio device template.\r\nID is missing.");
            }

            if (!data.name || data.name.length < 1 || !data.owner || !data.owner.id || !data.coding || !data.coding.id || data.private === undefined) {
                console.error("Received incomplete data from RadioDeviceTemplateForm:", data);
                toast.error("Failed to edit radio device template.\r\nReceived incomplete data.");
                return;
            }

            // Edit radio template
            itemsStore.updateRadioTemplate(data.id, data.name, data.owner.id, data.coding.id, data.private, data.description)
                .then((resp) => {
                    toast.success("Updated radio device template:\r\n" + resp.data.pretty_name);
                    this.showTemplateEditForm = false;
                    (this.$refs.itemOverview as InstanceType<typeof ItemOverview>).reloadTemplates();
                })
                .catch((error) => {
                    console.error("Failed to edit radio device template:", error);
                    toast.error("Failed to edit radio device template.\r\n" + APIUtils.createErrorToString(error));
                });
        },
    },
}
</script>
