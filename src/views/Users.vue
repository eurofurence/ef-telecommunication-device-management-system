<template>
    <h1>Users</h1>
    <v-data-table-server
        v-model:items-per-page="itemsPerPage"
        :headers="headers"
        :items-length="totalItems"
        :items="serverItems"
        :loading="loading"
        :search="search"
        item-value="name"
        @update:options="loadItems"
    ></v-data-table-server>
</template>

<script type="ts">
import {useUsersStore} from "@/store/users";

const usersStore = useUsersStore();

export default {
    // TODO: Add search fields for username, email, reg-id, collar-id
    data: () => ({
        headers: [
            {key: 'id', title: 'User-ID', align: 'start', sortable: true},
            {key: 'ef_reg_id', title: 'Reg-ID', align: 'start', sortable: true},
            {key: 'username', title: 'Username', align: 'start', sortable: true},
            {key: 'email', title: 'E-Mail', align: 'start', sortable: false},
            {key: 'ef_security_collar_id', title: 'Collar-ID', align: 'start', sortable: true},
            {key: 'last_seen', title: 'Last seen', align: 'start', sortable: false},
        ],
        search: '',
        serverItems: [],
        loading: true,
        itemsPerPage: 25,
        totalItems: 0,
    }),

    methods: {
        loadItems({page, itemsPerPage, sortBy}) {
            this.loading = true;
            usersStore.fetchUsersPage(page, itemsPerPage, sortBy).then(({items, total}) => {
                this.serverItems = items;
                this.totalItems = total;
                this.loading = false;
            });
        }
    }
}
</script>