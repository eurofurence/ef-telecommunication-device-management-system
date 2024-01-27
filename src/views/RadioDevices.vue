<template>
    <ItemTable
        title="Radios"
        icon="mdi-cellphone-basic"
        :items-table="itemsTable"
        :templates-table="templatesTable"
    />
</template>

<script lang="ts">
import {useItemsStore} from "@/store/items";
import ItemTable from "@/components/ItemTable.vue";

const itemsStore = useItemsStore();

export default {
    components: {ItemTable},
    data: () => ({
        itemsTable: {
            headers: [
                {key: 'id', title: 'Device-ID', align: 'start', sortable: true},
                {key: 'template', title: 'Template', align: 'start', sortable: true},
                {key: 'callsign', title: 'Callsign', align: 'start', sortable: true},
                {key: 'serialnumber', title: 'S/N', align: 'start', sortable: true},
                {key: 'handed_out', title: 'Status', align: 'start', sortable: true},
                {key: 'notes', title: 'Notes', align: 'start', sortable: false},
            ],
            fetchFunction: itemsStore.fetchRadiosPage,
            search: '',
            loading: true,
            itemsPerPage: 25,
            serverItems: [],
            totalItems: 0,
        },
        templatesTable: {
            headers: [
                {key: 'id', title: 'Template-ID', align: 'start', sortable: true},
                {key: 'name', title: 'Name', align: 'start', sortable: true},
                {key: 'description', title: 'Description', align: 'start', sortable: true},
            ],
            fetchFunction: itemsStore.fetchRadioTemplatesPage,
            search: '',
            loading: true,
            itemsPerPage: 25,
            serverItems: [],
            totalItems: 0,
        },
    }),
}
</script>
