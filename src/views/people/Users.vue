<template>
    <ItemOverview
        ref="itemOverview"
        title="Users"
        icon="mdi-account-group-outline"
        :items-table="itemsTable"
    />
</template>

<script lang="ts">
import {useUsersStore} from "@/store/users";
import ItemOverview from "@/components/ItemOverview.vue";

const usersStore = useUsersStore();

export default {
    // TODO: Remove user creation button. This should only be done via the backend. Need to adjust this in ItemTable component
    name: "Users",

    components: {
        ItemOverview
    },

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
        }
    }),
}
</script>