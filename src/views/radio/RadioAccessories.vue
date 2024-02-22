<template>
    <ItemOverview
        ref="itemOverview"
        title="Radio Accessories"
        icon="mdi-headset"
        :items-table="itemsTable"
        :templates-table="templatesTable"
        @deleteItems="deleteRadioAccessories"
        @deleteTemplates="deleteRadioAccessoryTemplates"
    />
</template>

<script lang="ts">
import {useItemsStore} from "@/store/items";
import ItemOverview from "@/components/ItemOverview.vue";

const itemsStore = useItemsStore();

export default {
    name: "RadioAccessories",

    components: {
        ItemOverview,
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
            fetchFunction: itemsStore.fetchRadioAccessoryTemplatesPage,
        },
    }),

    methods: {
        deleteRadioAccessories(itemIds: any[]) {
            // TODO: Replace with proper dialog
            if (confirm("Are you sure you want to delete these items?")) {
                itemIds.forEach((id) => {
                    itemsStore.deleteRadioAccessory(id);
                });

                // Force re-render of table
                this.$refs.itemOverview.reloadItems();
            }
        },
        deleteRadioAccessoryTemplates(templateIds: any[]) {
            // TODO: Replace with proper dialog
            if (confirm("Are you sure you want to delete these templates?")) {
                templateIds.forEach((id) => {
                    // TODO
                    console.log("deleting ... ", id);
                });

                // Force re-render of table
                this.$refs.itemOverview.reloadTemplates();
            }
        }
    }
}
</script>
