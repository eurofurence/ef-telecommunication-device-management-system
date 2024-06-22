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
        title="Item Owners"
        icon="mdi-account-arrow-right"
        :items-table="itemsTable"
        @click:create-item="showEditForm = true"
        @click:delete-items="deleteItemOwners"
    />

    <v-dialog v-model="showEditForm" max-width="560">
        <ItemOwnerForm
            @abort="showEditForm = false"
            @submit="createItemOwner($event)"
        />
    </v-dialog>
</template>

<script lang="ts">
import { useToast } from "vue-toastification";
import { useUsersStore } from "@/store/users";
import ItemOverview from "@/components/ItemOverview.vue";
import ItemOwnerForm from "@/components/forms/ItemOwnerForm.vue";
import {APIUtils} from "@/classes/util/APIUtils";

const usersStore = useUsersStore();
const toast = useToast();

export default {
    name: "ItemOwners",

    components: {
        ItemOverview,
        ItemOwnerForm,
    },

    data: () => ({
        itemsTable: {
            headers: [
                {key: 'id', title: 'Owner-ID', align: 'start', sortable: true},
                {key: 'shortname', title: 'Shortname', align: 'start', sortable: true},
                {key: 'name', title: 'Name', align: 'start', sortable: true},
            ],
            fetchFunction: usersStore.fetchItemOwnersPage,
        },
        showEditForm: false,
    }),

    methods: {
        deleteItemOwners(itemOwnerIds: number[]) {
            // TODO: Replace with proper dialog
            if (confirm("Are you sure you want to delete the selected item owners?")) {
                usersStore.deleteItemOwners(itemOwnerIds)
                    .then((resp) => {
                        toast.success("Deleted " + itemOwnerIds.length + " item owner(s)");
                    })
                    .catch((error) => {
                        toast.error("Failed to delete item owner(s).\r\n" + APIUtils.createErrorToString(error));
                        console.error("Failed to delete item owner(s):", error);
                    });

                // Deselect deleted items and force re-render of table
                (this.$refs.itemOverview as InstanceType<typeof ItemOverview>).deselectItemsByKey(itemOwnerIds);
                (this.$refs.itemOverview as InstanceType<typeof ItemOverview>).reloadItems();
            }
        },

        createItemOwner(data: any) {
                // Check received data
                if (data === null) {
                    console.error("Received null data from ItemOwnerForm");
                    toast.error("Failed to create item owner.\r\nReceived no data.");
                    return;
                }

                if (!data.name || !data.shortname) {
                    console.error("Received incomplete data from ItemOwnerForm:", data);
                    toast.error("Failed to create item owner.\r\nReceived incomplete data.");
                    return;
                }

                // Create new item owner
                usersStore.createItemOwner(data.name, data.shortname)
                    .then((resp) => {
                        toast.success("Created item owner with ID " + resp.data.id);
                        this.showEditForm = false;
                        (this.$refs.itemOverview as InstanceType<typeof ItemOverview>).reloadItems();
                    })
                    .catch((error) => {
                        console.error("Failed to create item owner:", error);
                        toast.error("Failed to create item owner.\r\n" + APIUtils.createErrorToString(error));
                    });
        }
    }
}
</script>
