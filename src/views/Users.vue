<template>
    <ItemTable
        title="Users"
        icon="mdi-account-group-outline"
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
                {key: 'id', title: 'User-ID', align: 'start', sortable: true},
                {key: 'ef_reg_id', title: 'Reg-ID', align: 'start', sortable: true},
                {key: 'username', title: 'Username', align: 'start', sortable: true},
                {key: 'email', title: 'E-Mail', align: 'start', sortable: false},
                {key: 'ef_security_collar_id', title: 'Collar-ID', align: 'start', sortable: true},
                {key: 'last_seen', title: 'Last seen', align: 'start', sortable: false},
            ],
            fetchFunction: usersStore.fetchUsersPage,
            search: '',
            serverItems: [],
            loading: true,
            itemsPerPage: 25,
            totalItems: 0,
        }
    }),
}
</script>