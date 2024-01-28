<template>
    <ItemTable
        title="VoIP Phones"
        icon="mdi-phone"
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
            search: '',
            loading: true,
            itemsPerPage: 25,
            serverItems: [],
            totalItems: 0,
        },
        templatesTable: {
            headers: [
                {key: 'id', title: 'ID', align: 'start', sortable: true},
                {key: 'name', title: 'Name', align: 'start', sortable: true},
                {key: 'description', title: 'Description', align: 'start', sortable: true},
                {key: 'owner.name', title: 'Owner', align: 'start', sortable: true},
            ],
            fetchFunction: itemsStore.fetchPhoneTemplatesPage,
            search: '',
            loading: true,
            itemsPerPage: 25,
            serverItems: [],
            totalItems: 0,
        },
    }),
}
</script>
