<template>
    <ItemTable
        title="Item Owners"
        icon="mdi-account-arrow-right"
        :items-table="itemsTable"
    />
</template>

<script lang="ts">
import {useUsersStore} from "@/store/users";
import ItemTable from "@/components/ItemTable.vue";

const usersStore = useUsersStore();

export default {
    components: {ItemTable},
    data: () => ({
        itemsTable: {
            headers: [
                {key: 'id', title: 'Owner-ID', align: 'start', sortable: true},
                {key: 'shortname', title: 'Shortname', align: 'start', sortable: true},
                {key: 'name', title: 'Name', align: 'start', sortable: true},
            ],
            fetchFunction: usersStore.fetchItemOwnersPage,
            search: '',
            serverItems: [],
            loading: true,
            itemsPerPage: 25,
            totalItems: 0,
        }
    }),
}
</script>
