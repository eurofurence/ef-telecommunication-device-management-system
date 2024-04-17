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

    <v-snackbar
        v-model="snackbar"
        :color="snackbarColor"
        :timeout="5000"
    >
        {{ snackbarContent }}

        <template v-slot:actions>
            <v-btn
                color="white"
                variant="text"
                @click="snackbar = false"
            >
                Dismiss
            </v-btn>
        </template>
    </v-snackbar>
</template>

<script lang="ts">
import {useUsersStore} from "@/store/users";
import ItemOverview from "@/components/ItemOverview.vue";
import ItemOwnerForm from "@/components/forms/ItemOwnerForm.vue";
import {APIUtils} from "@/classes/util/APIUtils";

const usersStore = useUsersStore();

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
        snackbar: false,
        snackbarColor: "error",
        snackbarContent: "",
    }),

    methods: {
        deleteItemOwners(itemOwnerIds: number[]) {
            // TODO: Replace with proper dialog
            if (confirm("Are you sure you want to delete the selected item owners?")) {
                usersStore.deleteItemOwners(itemOwnerIds)
                    .then((resp) => {
                        this.snackbarContent = "Deleted " + itemOwnerIds.length + " item owner(s)";
                        this.snackbarColor = "success";
                        this.snackbar = true;
                    })
                    .catch((error) => {
                        this.snackbarContent = "Failed to delete item owner(s)";
                        this.snackbarColor = "error";
                        this.snackbar = true;
                        console.error("Failed to delete item owner(s):", error);
                    });

                // Deselect deleted items and force re-render of table
                this.$refs.itemOverview.deselectItemsByKey(itemOwnerIds);
                this.$refs.itemOverview.reloadItems();
            }
        },

        async createItemOwner(data: any) {
            try {
                // Check received data
                if (data === null) {
                    console.error("Received null data from ItemOwnerForm");
                    throw new Error("Received no data");
                }

                if (!data.name || !data.shortname) {
                    console.error("Received incomplete data from ItemOwnerForm:", data);
                    throw new Error("Received incomplete data");
                }

                // Create new item owner
                await usersStore.createItemOwner(data.name, data.shortname)
                    .then((resp) => {
                        this.snackbarContent = "Created item owner with ID " + resp.data.id;
                        this.snackbarColor = "success";
                        this.snackbar = true;

                        this.showEditForm = false;
                        this.$refs.itemOverview.reloadItems();
                    })
                    .catch((error) => {
                        throw new Error(APIUtils.createErrorToString(error));
                    });
            } catch (error) {
                console.error("Failed to create item owner:", error);
                this.snackbarContent = "Failed to create item owner.<br>" + error.message;
                this.snackbarColor = "error";
                this.snackbar = true;
            }

        }
    }
}
</script>
