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
        title="Pagers"
        icon="mdi-bell-ring-outline"
        :items-table="itemsTable"
        :templates-table="templatesTable"
        @click:create-item="itemFormData = null; showItemEditForm = true"
        @click:edit-item="itemFormData = $event; showItemEditForm = true"
        @click:delete-items="deletePagers"
        @click:create-item-template="templateFormData = null; showTemplateEditForm = true"
        @click:edit-item-template="templateFormData = $event; showTemplateEditForm = true"
        @click:delete-item-templates="deletePagerTemplates"
    />

    <v-dialog v-model="showItemEditForm" max-width="560">
        <PagerForm
            :item="itemFormData"
            @abort="showItemEditForm = false"
            @submit="itemFormData ? updatePager($event) : createPager($event)"
        />
    </v-dialog>

    <v-dialog v-model="showTemplateEditForm" max-width="560">
        <PagerTemplateForm
            :item="templateFormData"
            @abort="showTemplateEditForm = false"
            @submit="templateFormData ? updatePagerTemplate($event) : createPagerTemplate($event)"
        />
    </v-dialog>
</template>

<script lang="ts">
import {useToast} from "vue-toastification";
import {useItemsStore} from "@/store/items";
import ItemOverview from "@/components/ItemOverview.vue";
import PagerForm from "@/components/forms/PagerForm.vue";
import PagerTemplateForm from "@/components/forms/PagerTemplateForm.vue";
import {APIUtils} from "@/classes/util/APIUtils";

const itemsStore = useItemsStore();
const toast = useToast();

export default {
    name: "RadioPagers",

    components: {PagerTemplateForm, PagerForm, ItemOverview},

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
            fetchFunction: itemsStore.fetchPagersPage,
            search: '',
            loading: true,
            itemsPerPage: 25,
            serverItems: [],
            totalItems: 0,
        },
        templatesTable: {
            headers: [
                {key: 'id', title: 'ID', align: 'start', sortable: true},
                {key: 'name', title: 'Template Name', align: 'start', sortable: true},
                {key: 'description', title: 'Description', align: 'start', sortable: true},
                {key: 'owner.name', title: 'Owner', align: 'start', sortable: true},
                {key: 'private', title: 'Private', align: 'start', sortable: true},
            ],
            fetchFunction: itemsStore.fetchPagerTemplatesPage,
            search: '',
            loading: true,
            itemsPerPage: 25,
            serverItems: [],
            totalItems: 0,
        },
        itemFormData: null as any,
        showItemEditForm: false,
        templateFormData: null as any,
        showTemplateEditForm: false,
    }),

    methods: {
        deletePagers(pagerIds: number[]) {
            // TODO: Replace with proper dialog
            if (confirm("Are you sure you want to delete the selected pagers?")) {
                itemsStore.deletePagers(pagerIds)
                    .then((resp) => {
                        toast.success("Deleted " + pagerIds.length + " pager(s)");
                    })
                    .catch((error) => {
                        toast.error("Failed to delete pager(s).\r\n" + APIUtils.createErrorToString(error));
                        console.error("Failed to delete pager(s):", error);
                    });

                // Deselect deleted items and force re-render of table
                (this.$refs.itemOverview as InstanceType<typeof ItemOverview>).deselectItemsByKey(pagerIds);
                (this.$refs.itemOverview as InstanceType<typeof ItemOverview>).reloadItems();
            }
        },

        createPager(data: any) {
            // Check received data
            if (data === null) {
                console.error("Received null data from PagerForm.");
                toast.error("Failed to create pager.\r\nReceived no data.");
                return;
            }

            if (!data.template || !data.template.id || (data.has_coordinates && (data.coordinates.floor < 0 || data.coordinates.latitude < 0 || data.coordinates.longitude < 0))) {
                console.error("Received incomplete data from PagerForm:", data);
                toast.error("Failed to create pager.\r\nReceived incomplete data.");
                return;
            }

            // Create pager
            itemsStore.createPager(
                data.template.id,
                data.serialnumber,
                data.notes,
                data.has_coordinates ? data.coordinates : null
            )
                .then((resp) => {
                    toast.success("Created new pager:\r\n" + resp.data.pretty_name);
                    this.showItemEditForm = false;
                    (this.$refs.itemOverview as InstanceType<typeof ItemOverview>).reloadItems();
                })
                .catch((error) => {
                    console.error("Failed to create pager:", error);
                    toast.error("Failed to create pager.\r\n" + APIUtils.createErrorToString(error));
                });
        },

        updatePager(data: any) {
            // Check received data
            if (data === null) {
                console.error("Received null data from PagerForm.");
                toast.error("Failed to update pager.\r\nReceived no data.");
                return;
            }

            if (!data.id) {
                console.error("Received incomplete data from PagerForm:", data);
                toast.error("Failed to update pager.\r\nMissing ID.");
                return;
            }

            if (!data.template || !data.template.id || (data.has_coordinates && (data.coordinates.floor < 0 || data.coordinates.latitude < 0 || data.coordinates.longitude < 0))) {
                console.error("Received incomplete data from PagerForm:", data);
                toast.error("Failed to update pager.\r\nReceived incomplete data.");
                return;
            }

            // Update pager
            itemsStore.updatePager(
                data.id,
                data.template.id,
                data.serialnumber,
                data.notes,
                data.has_coordinates ? data.coordinates : null
            )
                .then((resp) => {
                    toast.success("Updated pager:\r\n" + resp.data.pretty_name);
                    this.showItemEditForm = false;
                    (this.$refs.itemOverview as InstanceType<typeof ItemOverview>).reloadItems();
                })
                .catch((error) => {
                    console.error("Failed to update pager:", error);
                    toast.error("Failed to update pager.\r\n" + APIUtils.createErrorToString(error));
                });
        },

        deletePagerTemplates(pagerTemplateIds: number[]) {
            // TODO: Replace with proper dialog
            if (confirm("Are you sure you want to delete the selected pager template(s)?")) {
                itemsStore.deletePagerTemplates(pagerTemplateIds)
                    .then((resp) => {
                        toast.success("Deleted " + pagerTemplateIds.length + " pager template(s)");
                    })
                    .catch((error) => {
                        toast.error("Failed to delete pager template(s).\r\n" + APIUtils.createErrorToString(error));
                        console.error("Failed to delete pager template(s):", error);
                    });

                // Deselect deleted items and force re-render of table
                (this.$refs.itemOverview as InstanceType<typeof ItemOverview>).deselectTemplatesByKey(pagerTemplateIds);
                (this.$refs.itemOverview as InstanceType<typeof ItemOverview>).reloadTemplates();
            }
        },

        createPagerTemplate(data: any) {
            // Check received data
            if (data === null) {
                console.error("Received null data from PagerTemplateForm.");
                toast.error("Failed to create pager template.\r\nReceived no data.");
                return;
            }

            if (!data.name || data.name.length < 1 || !data.owner || !data.owner.id || data.private === undefined) {
                console.error("Received incomplete data from PagerTemplateForm:", data);
                toast.error("Failed to create pager template.\r\nReceived incomplete data.");
                return;
            }

            // Create pager template
            itemsStore.createPagerTemplate(data.name, data.owner.id, data.private, data.description)
                .then((resp) => {
                    toast.success("Created new pager template:\r\n" + resp.data.pretty_name);
                    this.showTemplateEditForm = false;
                    (this.$refs.itemOverview as InstanceType<typeof ItemOverview>).reloadTemplates();
                })
                .catch((error) => {
                    console.error("Failed to create pager template:", error);
                    toast.error("Failed to create pager template.\r\n" + APIUtils.createErrorToString(error));
                });
        },

        updatePagerTemplate(data: any) {
            // Check received data
            if (data === null) {
                console.error("Received null data from PagerTemplateForm.");
                toast.error("Failed to update pager template.\r\nReceived no data.");
                return;
            }

            if (!data.id) {
                console.error("Received incomplete data from PagerTemplateForm:", data);
                toast.error("Failed to update pager template.\r\nMissing ID.");
                return;
            }

            if (!data.name || data.name.length < 1 || !data.owner || !data.owner.id || data.private === undefined) {
                console.error("Received incomplete data from PagerTemplateForm:", data);
                toast.error("Failed to update pager template.\r\nReceived incomplete data.");
                return;
            }

            // Update pager template
            itemsStore.updatePagerTemplate(data.id, data.name, data.owner.id, data.private, data.description)
                .then((resp) => {
                    toast.success("Updated pager template:\r\n" + resp.data.pretty_name);
                    this.showTemplateEditForm = false;
                    (this.$refs.itemOverview as InstanceType<typeof ItemOverview>).reloadTemplates();
                })
                .catch((error) => {
                    console.error("Failed to update pager template:", error);
                    toast.error("Failed to update pager template.\r\n" + APIUtils.createErrorToString(error));
                });
        },
    },
}
</script>
