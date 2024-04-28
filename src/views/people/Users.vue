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
    name: "Users",

    components: {
        ItemOverview
    },

    data: () => ({
        itemsTable: {
            headers: [
                {key: 'id', title: 'User-ID', align: 'start', sortable: true},
                {key: 'ef_reg_id', title: 'Reg-ID', align: 'start', sortable: true},
                {key: 'nickname', title: 'Nickname', align: 'start', sortable: true},
                {key: 'email', title: 'E-Mail', align: 'start', sortable: false},
                {key: 'ef_security_collar_id', title: 'Collar-ID', align: 'start', sortable: true},
                {key: 'last_seen', title: 'Last seen', align: 'start', sortable: false},
            ],
            fetchFunction: usersStore.fetchUsersPage,
            preventCreate: true,
            preventEdit: true,
            preventDelete: true,
        }
    }),
}
</script>