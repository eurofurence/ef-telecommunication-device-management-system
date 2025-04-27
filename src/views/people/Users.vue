<!--
Eurofurence Telecommunication Device Management System (EF-TDMS)
Copyright (C) 2025 Niels Gandraß <niels@gandrass.de>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
-->

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
                {key: 'email', title: 'E-Mail', align: 'start', sortable: true},
                {key: 'ef_security_collar_id', title: 'Collar-ID', align: 'start', sortable: true},
                {key: 'last_login', title: 'Last login', align: 'start', sortable: false},
            ],
            fetchFunction: usersStore.fetchUsersPage,
            preventCreate: true,
            preventEdit: true,
            preventDelete: true,
        }
    }),
}
</script>