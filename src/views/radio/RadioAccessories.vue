<template>
    <ItemOverview
        ref="itemOverview"
        title="Radio Accessories"
        icon="mdi-headset"
        :items-table="itemsTable"
        :templates-table="templatesTable"
        @click:create-item="showItemEditForm = true"
        @click:delete-items="deleteRadioAccessories"
        @click:create-item-template="showTemplateEditForm = true"
        @click:delete-item-templates="deleteRadioAccessoryTemplates"
    />

    <v-dialog v-model="showItemEditForm" max-width="560">
        <RadioAccessoriesForm
            @abort="showItemEditForm = false"
            @submit="createRadioAccessories($event)"
        />
    </v-dialog>

    <v-dialog v-model="showTemplateEditForm" max-width="560">
        <RadioAccessoryTemplateForm
            @abort="showTemplateEditForm = false"
            @submit="createRadioAccessoryTemplate($event)"
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
                {key: 'allow_quickadd', title: 'Quickadd', align: 'start', sortable: true},
            ],
            expandedRowProps: [
                {key: 'compatible_with', title: 'Compatible with'},
            ],
            fetchFunction: itemsStore.fetchRadioAccessoryTemplatesPage,
        },
        showItemEditForm: false,
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

            if (!data.template || !data.amount) {
                console.error("Received incomplete data from RadioAccessoriesForm:", data);
                toast.error("Failed to create radio accessories.\r\nReceived incomplete data.");
                return;
            }

            // Create radio accessories
            itemsStore.createRadioAccessories(data.template, data.serialnumber, data.notes, data.amount)
                .then((resp) => {
                    toast.success(`Created ${resp.data.length} radio accessories`);
                    this.showItemEditForm = false;
                    (this.$refs.itemOverview as InstanceType<typeof ItemOverview>).reloadItems();
                })
                .catch((error) => {
                    console.error("Failed to create radio accessories:", error);
                    toast.error("Failed to create radio accessories.\r\n" + APIUtils.createErrorToString(error));
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

            if (!data.name || data.name.length < 1 || !data.owner || !data.allow_quickadd) {
                console.error("Received incomplete data from RadioAccessoryTemplateForm:", data);
                toast.error("Failed to create radio accessory template.\r\nReceived incomplete data.");
                return;
            }

            // Create radio accessory template
            itemsStore.createRadioAccessoryTemplate(data.name, data.owner, data.description, data.allow_quickadd)
                .then((resp) => {
                    toast.success("Created radio accessory template with ID " + resp.data.id);
                    this.showTemplateEditForm = false;
                    (this.$refs.itemOverview as InstanceType<typeof ItemOverview>).reloadTemplates();
                })
                .catch((error) => {
                    console.error("Failed to create radio accessory template:", error);
                    toast.error("Failed to create radio accessory template.\r\n" + APIUtils.createErrorToString(error));
                });
        },
    }
}
</script>
