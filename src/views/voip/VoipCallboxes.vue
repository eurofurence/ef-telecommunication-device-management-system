<template>
    <ItemOverview
        ref="itemOverview"
        title="Callboxes"
        icon="mdi-webcam"
        :items-table="itemsTable"
        :templates-table="templatesTable"
        @click:create-item="showItemEditForm = true"
        @click:delete-items="deleteCallboxes"
        @click:create-item-template="showTemplateEditForm = true"
        @click:delete-item-templates="deleteCallboxTemplates"
    />

    <v-dialog v-model="showItemEditForm" max-width="560">
        <VoipCallboxForm
            @abort="showItemEditForm = false"
            @submit="createCallbox($event)"
        />
    </v-dialog>

    <v-dialog v-model="showTemplateEditForm" max-width="560">
        <VoipCallboxTemplateForm
            @abort="showTemplateEditForm = false"
            @submit="createCallboxTemplate($event)"
        />
    </v-dialog>
</template>

<script lang="ts">
import {useItemsStore} from "@/store/items";
import ItemOverview from "@/components/ItemOverview.vue";
import VoipCallboxForm from "@/components/forms/VoipCallboxForm.vue";
import VoipCallboxTemplateForm from "@/components/forms/VoipCallboxTemplateForm.vue";
import {APIUtils} from "@/classes/util/APIUtils";
import { useToast } from "vue-toastification";

const itemsStore = useItemsStore();
const toast = useToast();

export default {
    name: "VoipCallboxes",

    components: {
        VoipCallboxTemplateForm,
        VoipCallboxForm,
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
                {key: 'has_camera', title: 'Camera', align: 'start', sortable: true},
                {key: 'handed_out', title: 'Status', align: 'start', sortable: true},
            ],
            expandedRowProps: [
                {key: 'template.owner.name', title: 'Owner'},
                {key: 'network', title: 'Phone Network'},
                {key: 'dhcp', title: 'Phone DHCP'},
                {key: 'ip_address', title: 'Phone IP Address'},
                {key: 'mac_address', title: 'Phone MAC Address'},
                {key: 'has_camera', title: 'Has Camera'},
                {key: 'camera_network', title: 'Camera Network'},
                {key: 'camera_dhcp', title: 'Camera DHCP'},
                {key: 'camera_ip_address', title: 'Camera IP Address'},
                {key: 'camera_mac_address', title: 'Camera MAC Address'},
                {key: 'created_at', title: 'Created at'},
                {key: 'updated_at', title: 'Updated at'},
            ],
            fetchFunction: itemsStore.fetchCallboxesPage,
        },
        templatesTable: {
            headers: [
                {key: 'id', title: 'ID', align: 'start', sortable: true},
                {key: 'name', title: 'Template Name', align: 'start', sortable: true},
                {key: 'description', title: 'Description', align: 'start', sortable: true},
                {key: 'owner.name', title: 'Owner', align: 'start', sortable: true},
            ],
            fetchFunction: itemsStore.fetchCallboxTemplatesPage,
        },
        showItemEditForm: false,
        showTemplateEditForm: false,
    }),

    methods: {
        deleteCallboxes(callboxIds: number[]) {
            // TODO: Replace with proper dialog
            if (confirm("Are you sure you want to delete the selected callbox(es)?")) {
                itemsStore.deleteCallboxes(callboxIds)
                    .then((resp) => {
                        toast.success("Deleted " + callboxIds.length + " callbox(es)");
                    })
                    .catch((error) => {
                        toast.error("Failed to delete callbox(es).\r\n" + APIUtils.createErrorToString(error));
                        console.error("Failed to delete callbox(es):", error);
                    });

                // Deselect deleted items and force re-render of table
                this.$refs.itemOverview.deselectItemsByKey(callboxIds);
                this.$refs.itemOverview.reloadItems();
            }
        },

        createCallbox(data: any) {
            // Check received data
            if (data === null) {
                console.error("Received null data from VoipCallboxForm.");
                toast.error("Failed to create callbox.\r\nReceived no data.");
                return;
            }

            if (!data.template || !data.extension || !data.network || data.dhcp === null || data.has_camera === null) {
                console.error("Received incomplete data from VoipCallboxForm:", data);
                toast.error("Failed to create callbox.\r\nReceived incomplete data.");
                return;
            }

            // Create callbox
            itemsStore.createCallbox(
                data.template,
                data.extension,
                data.network,
                data.dhcp,
                data.ip_address,
                data.mac_address,
                data.location,
                data.has_camera,
                data.camera_network,
                data.camera_dhcp,
                data.camera_ip_address,
                data.camera_mac_address,
                data.serialnumber,
                data.notes
            )
                .then((resp) => {
                    toast.success("Created callbox with ID " + resp.data.id);
                    this.showItemEditForm = false;
                    this.$refs.itemOverview.reloadItems();
                })
                .catch((error) => {
                    console.error("Failed to create callbox:", error);
                    toast.error("Failed to create callbox.\r\n" + APIUtils.createErrorToString(error));
                });
        },

        deleteCallboxTemplates(callboxTemplateIds: number[]) {
            // TODO: Replace with proper dialog
            if (confirm("Are you sure you want to delete the selected callbox template(s)?")) {
                itemsStore.deleteCallboxTemplates(callboxTemplateIds)
                    .then((resp) => {
                        toast.success("Deleted " + callboxTemplateIds.length + " callbox template(s)");
                    })
                    .catch((error) => {
                        toast.error("Failed to delete callbox template(s).\r\n" + APIUtils.createErrorToString(error));
                        console.error("Failed to delete callbox template(s):", error);
                    });

                // Deselect deleted items and force re-render of table
                this.$refs.itemOverview.deselectTemplatesByKey(callboxTemplateIds);
                this.$refs.itemOverview.reloadTemplates();
            }
        },

        createCallboxTemplate(data: any) {
            // Check received data
            if (data === null) {
                console.error("Received null data from VoipCallboxTemplateForm.");
                toast.error("Failed to create callbox template.\r\nReceived no data.");
                return;
            }

            if (!data.name || data.name.length < 1 || !data.owner) {
                console.error("Received incomplete data from VoipCallboxTemplateForm:", data);
                toast.error("Failed to create callbox template.\r\nReceived incomplete data.");
                return;
            }

            // Create callbox template
            itemsStore.createCallboxTemplate(data.name, data.owner, data.description)
                .then((resp) => {
                    toast.success("Created callbox template with ID " + resp.data.id);
                    this.showTemplateEditForm = false;
                    this.$refs.itemOverview.reloadTemplates();
                })
                .catch((error) => {
                    console.error("Failed to create callbox template:", error);
                    toast.error("Failed to create callbox template.\r\n" + APIUtils.createErrorToString(error));
                });
        },
    },
}
</script>
