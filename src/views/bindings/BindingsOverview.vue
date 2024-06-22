<!--
Eurofurence Telecommunication Device Management System (EF-TDMS)
Copyright (C) 2024 Niels Gandraß <niels@gandrass.de>

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
        title="Bindings"
        icon="mdi-basket-outline"
        :items-table="itemsTable"
        @click:delete-items="$router.push('/bindings/return')"
        @click:create-item="$router.push('/bindings/issue')"
    />
</template>

<script lang="ts">
import {useBindingsStore} from "@/store/bindings";
import ItemOverview from "@/components/ItemOverview.vue";

const bindingsStore = useBindingsStore();

export default {
    name: "BindingsOverview",

    components: {
        ItemOverview,
    },

    data: () => ({
        itemsTable: {
            headers: [
                {key: 'id', title: 'ID', align: 'start', sortable: true},
                {key: 'item.template.name', title: 'Type', align: 'start', sortable: true},
                {key: 'item.template.owner.shortname', title: 'Owner', align: 'start', sortable: true},
                {key: 'item.serialnumber', title: 'S/N', align: 'start', sortable: true},
                {key: 'user.pretty_name', title: 'Borrower', align: 'start', sortable: true},
                {key: 'bound_by.pretty_name', title: 'Issuer', align: 'start', sortable: true},
            ],
            expandedRowProps: [
                {key: 'bound_at', title: 'Bound at'},
                {key: 'bound_by.ef_reg_id', title: 'Issuer EF Reg ID'},
                {key: 'user.ef_reg_id', title: 'Borrower EF Reg ID'},
                {key: 'item.template.owner.name', title: 'Item owner'},
                {key: 'item.notes', title: 'Item notes'},
                {key: 'item.template.description', title: 'Template description'},
                {key: 'item.callsign', title: 'Callsign', hideMissing: true},
            ],
            fetchFunction: bindingsStore.fetchBindingsPage,
        },
    }),
}
</script>
