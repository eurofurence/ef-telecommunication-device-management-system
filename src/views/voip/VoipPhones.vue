<template>
    <ItemOverview
        ref="itemOverview"
        title="VoIP Phones"
        icon="mdi-phone"
        :items-table="itemsTable"
        :templates-table="templatesTable"
        @click:create-item="showItemEditForm = true"
        @click:delete-items="deletePhones"
        @click:create-item-template="showTemplateEditForm = true"
        @click:delete-item-templates="deletePhoneTemplates"
    />

    <v-dialog v-model="showItemEditForm" max-width="560">
        <VoipPhoneForm
            @abort="showItemEditForm = false"
            @submit="createPhone($event)"
        />
    </v-dialog>

    <v-dialog v-model="showTemplateEditForm" max-width="560">
        <VoipPhoneTemplateForm
            @abort="showTemplateEditForm = false"
            @submit="createPhoneTemplate($event)"
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
                {key: 'handed_out', title: 'Status', align: 'start', sortable: true},
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
        showItemEditForm: false,
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

            if (!data.template || !data.extension || !data.network || data.dhcp === null) {
                console.error("Received incomplete data from VoipPhoneForm:", data);
                toast.error("Failed to create phone.\r\nReceived incomplete data.");
                return;
            }

            // Create phone
            itemsStore.createPhone(
                data.template,
                data.extension,
                data.network,
                data.dhcp,
                data.ip_address,
                data.mac_address,
                data.location,
                data.serialnumber,
                data.notes
            )
                .then((resp) => {
                    toast.success("Created phone with ID " + resp.data.id);
                    this.showItemEditForm = false;
                    (this.$refs.itemOverview as InstanceType<typeof ItemOverview>).reloadItems();
                })
                .catch((error) => {
                    console.error("Failed to create phone:", error);
                    toast.error("Failed to create phone.\r\n" + APIUtils.createErrorToString(error));
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

            if (!data.name || data.name.length < 1 || !data.owner || data.private === undefined) {
                console.error("Received incomplete data from VoipPhoneTemplateForm:", data);
                toast.error("Failed to create phone template.\r\nReceived incomplete data.");
                return;
            }

            // Create phone template
            itemsStore.createPhoneTemplate(data.name, data.owner, data.private, data.description)
                .then((resp) => {
                    toast.success("Created phone template with ID " + resp.data.id);
                    this.showTemplateEditForm = false;
                    (this.$refs.itemOverview as InstanceType<typeof ItemOverview>).reloadTemplates();
                })
                .catch((error) => {
                    console.error("Failed to create phone template:", error);
                    toast.error("Failed to create phone template.\r\n" + APIUtils.createErrorToString(error));
                });
        },
    },
}
</script>
