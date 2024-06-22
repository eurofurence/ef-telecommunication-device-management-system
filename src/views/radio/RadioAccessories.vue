<!--
Eurofurence Telecommunication Device Management System (EF-TDMS)
Copyright (C) 2024 Niels Gandraß <niels@gandrass.de>

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
        title="Radio Accessories"
        icon="mdi-headset"
        :items-table="itemsTable"
        :templates-table="templatesTable"
        @click:create-item="itemFormData = null; showItemEditForm = true"
        @click:edit-item="itemFormData = $event; showItemEditForm = true"
        @click:delete-items="deleteRadioAccessories"
        @click:create-item-template="templateFormData = null; showTemplateEditForm = true"
        @click:edit-item-template="templateFormData = $event; showTemplateEditForm = true"
        @click:delete-item-templates="deleteRadioAccessoryTemplates"
    />

    <v-dialog v-model="showItemEditForm" max-width="560">
        <RadioAccessoriesForm
            :item="itemFormData"
            @abort="showItemEditForm = false"
            @submit="itemFormData ? updateRadioAccessory($event) : createRadioAccessories($event)"
        />
    </v-dialog>

    <v-dialog v-model="showTemplateEditForm" max-width="560">
        <RadioAccessoryTemplateForm
            :item="templateFormData"
            @abort="showTemplateEditForm = false"
            @submit="templateFormData ? updateRadioAccessoryTemplate($event) : createRadioAccessoryTemplate($event)"
        />
    </v-dialog>
</template>

<script lang="ts">
import {useToast} from "vue-toastification";
import {useItemsStore} from "@/store/items";
import ItemOverview from "@/components/ItemOverview.vue";
import RadioAccessoriesForm from "@/components/forms/RadioAccessoriesForm.vue";
import RadioAccessoryTemplateForm from "@/components/forms/RadioAccessoryTemplateForm.vue";
import {APIUtils} from "@/classes/util/APIUtils";

const itemsStore = useItemsStore();
const toast = useToast();

export default {
    name: "RadioAccessories",

    components: {
        ItemOverview,
        RadioAccessoriesForm,
        RadioAccessoryTemplateForm
    },

    data: () => ({
        itemsTable: {
            headers: [
                {key: 'id', title: 'ID', align: 'start', sortable: true},
                {key: 'template.name', title: 'Type', align: 'start', sortable: true},
                {key: 'template.owner.shortname', title: 'Owner', align: 'start', sortable: true},
                {key: 'serialnumber', title: 'S/N', align: 'start', sortable: true},
                {key: 'notes', title: 'Notes', align: 'start', sortable: false},
                {key: 'handed_out', title: 'Status', align: 'start', sortable: true},
            ],
            expandedRowProps: [
                {key: 'template.owner.name', title: 'Owner'},
                {key: 'created_at', title: 'Created at'},
                {key: 'updated_at', title: 'Updated at'},
            ],
            fetchFunction: itemsStore.fetchRadioAccessoriesPage,
        },
        templatesTable: {
            headers: [
                {key: 'id', title: 'ID', align: 'start', sortable: true},
                {key: 'name', title: 'Template Name', align: 'start', sortable: true},
                {key: 'description', title: 'Description', align: 'start', sortable: true},
                {key: 'owner.name', title: 'Owner', align: 'start', sortable: true},
                {key: 'private', title: 'Private', align: 'start', sortable: true},
                {key: 'allow_quickadd', title: 'Quickadd', align: 'start', sortable: true},
            ],
            expandedRowProps: [
                {key: 'compatible_with', title: 'Compatible with'},
            ],
            fetchFunction: itemsStore.fetchRadioAccessoryTemplatesPage,
        },
        itemFormData: null as any,
        showItemEditForm: false,
        templateFormData: null as any,
        showTemplateEditForm: false,
    }),

    methods: {
        deleteRadioAccessories(radioAccessoryIds: number[]) {
            // TODO: Replace with proper dialog
            if (confirm("Are you sure you want to delete the selected radio accessories?")) {
                itemsStore.deleteRadioAccessories(radioAccessoryIds)
                    .then((resp) => {
                        toast.success("Deleted " + radioAccessoryIds.length + " radio accessories");
                    })
                    .catch((error) => {
                        toast.error("Failed to delete radio accessories.\r\n" + APIUtils.createErrorToString(error));
                        console.error("Failed to delete radio accessories:", error);
                    });

                // Deselect deleted items and force re-render of table
                (this.$refs.itemOverview as InstanceType<typeof ItemOverview>).deselectItemsByKey(radioAccessoryIds);
                (this.$refs.itemOverview as InstanceType<typeof ItemOverview>).reloadItems();
            }
        },

        createRadioAccessories(data: any) {
            // Check received data
            if (data === null) {
                console.error("Received null data from RadioAccessoriesForm.");
                toast.error("Failed to create radio accessories.\r\nReceived no data.");
                return;
            }

            if (!data.template || !data.template.id || !data.amount) {
                console.error("Received incomplete data from RadioAccessoriesForm:", data);
                toast.error("Failed to create radio accessories.\r\nReceived incomplete data.");
                return;
            }

            // Create radio accessories
            itemsStore.createRadioAccessories(data.template.id, data.serialnumber, data.notes, data.amount)
                .then((resp) => {
                    toast.success(`Created ${resp.data.length} new radio accessories:\r\n` + resp.data[0].pretty_name + ' ...');
                    this.showItemEditForm = false;
                    (this.$refs.itemOverview as InstanceType<typeof ItemOverview>).reloadItems();
                })
                .catch((error) => {
                    console.error("Failed to create radio accessories:", error);
                    toast.error("Failed to create radio accessories.\r\n" + APIUtils.createErrorToString(error));
                });
        },

        updateRadioAccessory(data: any) {
            // Check received data
            if (data === null) {
                console.error("Received null data from RadioAccessoriesForm.");
                toast.error("Failed to update radio accessory.\r\nReceived no data.");
                return;
            }

            if (!data.id) {
                console.error("Received incomplete data from RadioAccessoriesForm:", data);
                toast.error("Failed to update radio accessory.\r\nMissing ID.");
                return;
            }

            if (!data.template || !data.template.id) {
                console.error("Received incomplete data from RadioAccessoriesForm:", data);
                toast.error("Failed to update radio accessory.\r\nReceived incomplete data.");
                return;
            }

            // Update radio accessory
            itemsStore.updateRadioAccessory(data.id, data.template.id, data.serialnumber, data.notes)
                .then((resp) => {
                    toast.success("Updated radio accessory:\r\n" + resp.data.pretty_name);
                    this.showItemEditForm = false;
                    (this.$refs.itemOverview as InstanceType<typeof ItemOverview>).reloadItems();
                })
                .catch((error) => {
                    console.error("Failed to update radio accessory:", error);
                    toast.error("Failed to update radio accessory.\r\n" + APIUtils.createErrorToString(error));
                });
        },

        deleteRadioAccessoryTemplates(radioAccessoryTemplateIds: number[]) {
            // TODO: Replace with proper dialog
            if (confirm("Are you sure you want to delete the selected radio accessory template(s)?")) {
                itemsStore.deleteRadioAccessoryTemplates(radioAccessoryTemplateIds)
                    .then((resp) => {
                        toast.success("Deleted " + radioAccessoryTemplateIds.length + " radio accessory template(s)");
                    })
                    .catch((error) => {
                        toast.error("Failed to delete radio accessory template(s).\r\n" + APIUtils.createErrorToString(error));
                        console.error("Failed to delete radio accessory template(s):", error);
                    });

                // Deselect deleted items and force re-render of table
                (this.$refs.itemOverview as InstanceType<typeof ItemOverview>).deselectTemplatesByKey(radioAccessoryTemplateIds);
                (this.$refs.itemOverview as InstanceType<typeof ItemOverview>).reloadTemplates();
            }
        },

        createRadioAccessoryTemplate(data: any) {
            // Check received data
            if (data === null) {
                console.error("Received null data from RadioAccessoryTemplateForm.");
                toast.error("Failed to create radio accessory template.\r\nReceived no data.");
                return;
            }

            if (!data.name || data.name.length < 1 || !data.owner || !data.owner.id || data.private === undefined || data.allow_quickadd === undefined) {
                console.error("Received incomplete data from RadioAccessoryTemplateForm:", data);
                toast.error("Failed to create radio accessory template.\r\nReceived incomplete data.");
                return;
            }

            // Create radio accessory template
            itemsStore.createRadioAccessoryTemplate(data.name, data.owner.id, data.private, data.description, data.allow_quickadd)
                .then((resp) => {
                    toast.success("Created new radio accessory template:\r\n" + resp.data.pretty_name);
                    this.showTemplateEditForm = false;
                    (this.$refs.itemOverview as InstanceType<typeof ItemOverview>).reloadTemplates();
                })
                .catch((error) => {
                    console.error("Failed to create radio accessory template:", error);
                    toast.error("Failed to create radio accessory template.\r\n" + APIUtils.createErrorToString(error));
                });
        },

        updateRadioAccessoryTemplate(data: any) {
            // Check received data
            if (data === null) {
                console.error("Received null data from RadioAccessoryTemplateForm.");
                toast.error("Failed to update radio accessory template.\r\nReceived no data.");
                return;
            }

            if (!data.id) {
                console.error("Received incomplete data from RadioAccessoryTemplateForm:", data);
                toast.error("Failed to update radio accessory template.\r\nMissing ID.");
                return;
            }

            if (!data.name || data.name.length < 1 || !data.owner || !data.owner.id || data.private === undefined || data.allow_quickadd === undefined) {
                console.error("Received incomplete data from RadioAccessoryTemplateForm:", data);
                toast.error("Failed to update radio accessory template.\r\nReceived incomplete data.");
                return;
            }

            // Update radio accessory template
            itemsStore.updateRadioAccessoryTemplate(data.id, data.name, data.owner.id, data.private, data.description, data.allow_quickadd)
                .then((resp) => {
                    toast.success("Updated radio accessory template:\r\n" + resp.data.pretty_name);
                    this.showTemplateEditForm = false;
                    (this.$refs.itemOverview as InstanceType<typeof ItemOverview>).reloadTemplates();
                })
                .catch((error) => {
                    console.error("Failed to update radio accessory template:", error);
                    toast.error("Failed to update radio accessory template.\r\n" + APIUtils.createErrorToString(error));
                });
        },
    }
}
</script>
