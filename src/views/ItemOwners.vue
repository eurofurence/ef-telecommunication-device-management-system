<template>
    <h1>Item Owners</h1>
    <v-data-table-server
        v-model:items-per-page="itemsPerPage"
        :headers="headers"
        :items-length="totalItems"
        :items="serverItems"
        :loading="loading"
        :search="search"
        item-value="name"
        @update:options="loadItems"
    >
        <template v-slot:top>
            <v-text-field
                v-model="search"
                label="Search"
                single-line
                hide-details
                clearable
            ></v-text-field>
        </template>
    </v-data-table-server>
</template>

<script type="ts">
import {useUsersStore} from "@/store/users";

const usersStore = useUsersStore();

export default {
    data: () => ({
        headers: [
            {key: 'id', title: 'Owner-ID', align: 'start', sortable: true},
            {key: 'shortname', title: 'Shortname', align: 'start', sortable: true},
            {key: 'name', title: 'Name', align: 'start', sortable: true},
        ],
        search: '',
        serverItems: [],
        loading: true,
        itemsPerPage: 25,
        totalItems: 0,
    }),

    methods: {
        loadItems({page, itemsPerPage, sortBy, search}) {
            this.loading = true;
            usersStore.fetchItemOwnersPage(page, itemsPerPage, sortBy, search).then(({items, total}) => {
                this.serverItems = items;
                this.totalItems = total;
                this.loading = false;
            });
        }
    }
}
</script>