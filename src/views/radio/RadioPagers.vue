<template>
    <ItemOverview
        ref="itemOverview"
        title="Pagers"
        icon="mdi-bell-ring-outline"
        :items-table="itemsTable"
        :templates-table="templatesTable"
        @click:create-item="showItemEditForm = true"
        @click:delete-items="deletePagers"
        @click:create-item-template="showTemplateEditForm = true"
        @click:delete-item-templates="deletePagerTemplates"
    />

    <v-dialog v-model="showItemEditForm" max-width="560">
        <PagerForm
            @abort="showItemEditForm = false"
            @submit="createPager($event)"
        />
    </v-dialog>

    <v-dialog v-model="showTemplateEditForm" max-width="560">
        <PagerTemplateForm
            @abort="showTemplateEditForm = false"
            @submit="createPagerTemplate($event)"
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
            ],
            fetchFunction: itemsStore.fetchPagerTemplatesPage,
            search: '',
            loading: true,
            itemsPerPage: 25,
            serverItems: [],
            totalItems: 0,
        },
        showItemEditForm: false,
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

            if (!data.template) {
                console.error("Received incomplete data from PagerForm:", data);
                toast.error("Failed to create pager.\r\nReceived incomplete data.");
                return;
            }

            // Create pager
            itemsStore.createPager(data.template, data.serialnumber, data.notes)
                .then((resp) => {
                    toast.success("Created pager with ID " + resp.data.id);
                    this.showItemEditForm = false;
                    (this.$refs.itemOverview as InstanceType<typeof ItemOverview>).reloadItems();
                })
                .catch((error) => {
                    console.error("Failed to create pager:", error);
                    toast.error("Failed to create pager.\r\n" + APIUtils.createErrorToString(error));
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

            if (!data.name || data.name.length < 1 || !data.owner) {
                console.error("Received incomplete data from PagerTemplateForm:", data);
                toast.error("Failed to create pager template.\r\nReceived incomplete data.");
                return;
            }

            // Create pager template
            itemsStore.createPagerTemplate(data.name, data.owner, data.description)
                .then((resp) => {
                    toast.success("Created pager template with ID " + resp.data.id);
                    this.showTemplateEditForm = false;
                    (this.$refs.itemOverview as InstanceType<typeof ItemOverview>).reloadTemplates();
                })
                .catch((error) => {
                    console.error("Failed to create pager template:", error);
                    toast.error("Failed to create pager template.\r\n" + APIUtils.createErrorToString(error));
                });
        },
    },
}
</script>
