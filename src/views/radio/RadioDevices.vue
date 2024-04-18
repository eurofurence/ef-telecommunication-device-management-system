<template>
    <ItemOverview
        ref="itemOverview"
        title="Radios"
        icon="mdi-cellphone-basic"
        :items-table="itemsTable"
        :templates-table="templatesTable"
        @click:create-item="showEditForm = true"
        @click:delete-items="deleteRadios"
    />

    <v-dialog v-model="showEditForm" max-width="560">
        <RadioDeviceForm
            @abort="showEditForm = false"
            @submit="createRadio($event)"
        />
    </v-dialog>
</template>

<script lang="ts">
import {useToast} from "vue-toastification";
import {useItemsStore} from "@/store/items";
import ItemOverview from "@/components/ItemOverview.vue";
import RadioDeviceForm from "@/components/forms/RadioDeviceForm.vue";
import {APIUtils} from "@/classes/util/APIUtils";

const itemsStore = useItemsStore();
const toast = useToast();

export default {
    name: "RadioDevices",

    components: {RadioDeviceForm, ItemOverview},

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
                {key: 'handed_out', title: 'Status', align: 'start', sortable: true},
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
            ],
            fetchFunction: itemsStore.fetchRadioTemplatesPage,
        },
        showEditForm: false,
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
                this.$refs.itemOverview.deselectItemsByKey(radioDeviceIds);
                this.$refs.itemOverview.reloadItems();
            }
        },

        createRadio(data: any) {
            console.log(data);
            // Check received data
            if (data === null) {
                console.error("Received null data from RadioDeviceForm.");
                toast.error("Failed to create radio device.\r\nReceived no data.");
                return;
            }

            if (!data.template) {
                console.error("Received incomplete data from RadioDeviceForm:", data);
                toast.error("Failed to create radio device.\r\nReceived incomplete data.");
                return;
            }

            // Create radio coding
            itemsStore.createRadio(data.template, data.callsign, data.serialnumber, data.notes)
                .then((resp) => {
                    toast.success("Created radio device with ID " + resp.data.id);
                    this.showEditForm = false;
                    this.$refs.itemOverview.reloadItems();
                })
                .catch((error) => {
                    console.error("Failed to create radio device:", error);
                    toast.error("Failed to create radio device.\r\n" + APIUtils.createErrorToString(error));
                });
        },
    },
}
</script>
