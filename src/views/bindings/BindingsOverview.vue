<template>
    <ItemOverview
        ref="itemOverview"
        title="Bindings"
        icon="mdi-basket-outline"
        :items-table="itemsTable"
        @deleteItems="console.error('deleteItems not implemented')"
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
                {key: 'user.username', title: 'Borrower', align: 'start', sortable: true},
                {key: 'bound_by.username', title: 'Issuer', align: 'start', sortable: true},
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
