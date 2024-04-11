<template>
    <ItemOverview
        ref="itemOverview"
        title="Radio Codings"
        icon="mdi-sim"
        :items-table="itemsTable"
    />
</template>

<script lang="ts">
import ItemTable from "@/components/ItemTable.vue";
import ItemOverview from "@/components/ItemOverview.vue";
import {useItemsStore} from "@/store/items";

const itemsStore = useItemsStore();

export default {
    name: "RadioCodings",

    components: {
        ItemOverview,
        ItemTable
    },

    data: () => ({
        itemsTable: {
            headers: [
                {key: 'id', title: 'ID', align: 'start', sortable: true},
                {key: 'name', title: 'Name', align: 'start', sortable: true},
                {key: 'color', title: 'Color', align: 'start', sortable: true},
                {key: 'description', title: 'Description', align: 'start', sortable: true},
            ],
            fetchFunction: itemsStore.fetchRadioCodingsPage,
        }
    }),
}
</script>
