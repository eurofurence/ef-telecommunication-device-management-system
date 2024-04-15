<template>
    <ItemOverview
        ref="itemOverview"
        title="Pre-Orders"
        icon="mdi-basket-fill"
        :items-table="itemsTable"
    />
</template>

<script lang="ts">
import ItemTable from "@/components/ItemTable.vue";
import ItemOverview from "@/components/ItemOverview.vue";
import {useBindingsStore} from "@/store/bindings";

const bindingsStore = useBindingsStore();

export default {
    name: "BindingsPreorders",

    components: {
        ItemOverview,
        ItemTable
    },

    data: () => ({
        itemsTable: {
            headers: [
                {key: 'id', title: 'ID', align: 'start', sortable: true},
                {key: 'user.pretty_name', title: 'User', align: 'start', sortable: true},
                {key: 'type', title: 'Type', align: 'start', sortable: true},
                {key: 'title', title: 'Title', align: 'start', sortable: true},
                {key: 'item_template.name', title: 'Template', align: 'start', sortable: true},
                {key: 'item.pretty_name', title: 'Item', align: 'start', sortable: true},
            ],
            fetchFunction: bindingsStore.fetchOrdersPage,
        }
    }),
}
</script>
