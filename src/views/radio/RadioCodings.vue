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
        title="Radio Codings"
        icon="mdi-sim"
        :items-table="itemsTable"
        @click:create-item="itemFormData = null; showEditForm = true"
        @click:edit-item="itemFormData = $event; showEditForm = true"
        @click:delete-items="deleteRadioCodings"
    />

    <v-dialog v-model="showEditForm" max-width="560">
        <RadioCodingForm
            :item="itemFormData"
            @abort="showEditForm = false"
            @submit="itemFormData ? updateRadioCoding($event) : createRadioCoding($event)"
        />
    </v-dialog>
</template>

<script lang="ts">
import {useToast} from "vue-toastification";
import ItemOverview from "@/components/ItemOverview.vue";
import {useItemsStore} from "@/store/items";
import RadioCodingForm from "@/components/forms/RadioCodingForm.vue";
import {APIUtils} from "@/classes/util/APIUtils";

const itemsStore = useItemsStore();
const toast = useToast();

export default {
    name: "RadioCodings",

    components: {
        RadioCodingForm,
        ItemOverview,
    },

    data: () => ({
        itemsTable: {
            headers: [
                {key: 'id', title: 'ID', align: 'start', sortable: true},
                {key: 'name', title: 'Name', align: 'start', sortable: true},
                {key: 'color', title: 'Color', align: 'start', sortable: false},
                {key: 'description', title: 'Description', align: 'start', sortable: true},
            ],
            fetchFunction: itemsStore.fetchRadioCodingsPage,
        },
        itemFormData: null as any,
        showEditForm: false,
    }),

    methods: {
        deleteRadioCodings(radioCodingIds: number[]) {
            // TODO: Replace with proper dialog
            if (confirm("Are you sure you want to delete the selected radio codings?")) {
                itemsStore.deleteRadioCodings(radioCodingIds)
                    .then((resp) => {
                        toast.success("Deleted " + radioCodingIds.length + " radio coding(s)");
                    })
                    .catch((error) => {
                        toast.error("Failed to delete radio coding(s).\r\n" + APIUtils.createErrorToString(error));
                        console.error("Failed to delete radio coding(s):", error);
                    });

                // Deselect deleted items and force re-render of table
                (this.$refs.itemOverview as InstanceType<typeof ItemOverview>).deselectItemsByKey(radioCodingIds);
                (this.$refs.itemOverview as InstanceType<typeof ItemOverview>).reloadItems();
            }
        },

        createRadioCoding(data: any) {
            // Check received data
            if (data === null) {
                console.error("Received null data from RadioCodingForm.");
                toast.error("Failed to create radio coding.\r\nReceived no data.");
                return;
            }

            if (!data.name || !data.color) {
                console.error("Received incomplete data from RadioCodingForm:", data);
                toast.error("Failed to create radio coding.\r\nReceived incomplete data.");
                return;
            }

            // Create radio coding
            itemsStore.createRadioCoding(data.name, data.color, data.description)
                .then((resp) => {
                    toast.success("Created new radio coding:\r\n" + resp.data.pretty_name);
                    this.showEditForm = false;
                    (this.$refs.itemOverview as InstanceType<typeof ItemOverview>).reloadItems();
                })
                .catch((error) => {
                    console.error("Failed to create radio coding:", error);
                    toast.error("Failed to create radio coding.\r\n" + APIUtils.createErrorToString(error));
                });
        },

        updateRadioCoding(data: any) {
            // Check received data
            if (data === null) {
                console.error("Received null data from RadioCodingForm.");
                toast.error("Failed to update radio coding.\r\nReceived no data.");
                return;
            }

            if (!data.id) {
                console.error("Received incomplete data from RadioCodingForm:", data);
                toast.error("Failed to update radio coding.\r\nMissing ID.");
                return;
            }

            if (!data.name || !data.color) {
                console.error("Received incomplete data from RadioCodingForm:", data);
                toast.error("Failed to update radio coding.\r\nReceived incomplete data.");
                return;
            }

            // Update radio coding
            itemsStore.updateRadioCoding(data.id, data.name, data.color, data.description)
                .then((resp) => {
                    toast.success("Updated radio coding:\r\n" + resp.data.pretty_name);
                    this.showEditForm = false;
                    (this.$refs.itemOverview as InstanceType<typeof ItemOverview>).reloadItems();
                })
                .catch((error) => {
                    console.error("Failed to update radio coding:", error);
                    toast.error("Failed to update radio coding.\r\n" + APIUtils.createErrorToString(error));
                });
        },
    }
}
</script>
