<template>
    <ItemOverview
        ref="itemOverview"
        title="Pre-Orders"
        icon="mdi-basket-fill"
        :items-table="itemsTable"
        @click:create-item="showItemEditForm = true"
        @click:delete-items="deleteOrders"
    />

    <v-dialog v-model="showItemEditForm" max-width="560">
        <BindingPreorderForm
            @abort="showItemEditForm = false"
            @submit="createOrder($event)"
        />
    </v-dialog>
</template>

<script lang="ts">
import {useToast} from "vue-toastification";
import ItemTable from "@/components/ItemTable.vue";
import ItemOverview from "@/components/ItemOverview.vue";
import {useBindingsStore} from "@/store/bindings";
import BindingPreorderForm from "@/components/forms/BindingPreorderForm.vue";
import {APIUtils} from "@/classes/util/APIUtils";

const bindingsStore = useBindingsStore();
const toast = useToast();

export default {
    name: "BindingsPreorders",

    components: {
        BindingPreorderForm,
        ItemOverview,
        ItemTable
    },

    data: () => ({
        itemsTable: {
            headers: [
                {key: 'id', title: 'ID', align: 'start', sortable: true},
                {key: 'user.pretty_name', title: 'User', align: 'start', sortable: true},
                {key: 'type', title: 'Type', align: 'start', sortable: true},
                {key: 'title', title: 'Title', align: 'start', sortable: true},
                {key: 'item_template.name', title: 'Template', align: 'start', sortable: true},
                {key: 'item.pretty_name', title: 'Item', align: 'start', sortable: true},
            ],
            fetchFunction: bindingsStore.fetchOrdersPage,
        },
        showItemEditForm: false,
    }),

    methods: {
        deleteOrders(orderIds: number[]) {
            // TODO: Replace with proper dialog
            if (confirm("Are you sure you want to delete the selected pre-order(s)?")) {
                bindingsStore.deleteOrders(orderIds)
                    .then((resp) => {
                        toast.success("Deleted " + orderIds.length + " pre-order(s)");
                    })
                    .catch((error) => {
                        toast.error("Failed to delete pre-order(s).\r\n" + APIUtils.createErrorToString(error));
                        console.error("Failed to delete pre-order(s):", error);
                    });

                // Deselect deleted items and force re-render of table
                (this.$refs.itemOverview as InstanceType<typeof ItemOverview>).deselectItemsByKey(orderIds);
                (this.$refs.itemOverview as InstanceType<typeof ItemOverview>).reloadItems();
            }
        },

        createOrder(data: any) {
            // Check received data
            if (data === null) {
                console.error("Received null data from BindingPreorderForm.");
                toast.error("Failed to create pre-order.\r\nReceived no data.");
                return;
            }

            if (!data.user || !data.type || !data.title) {
                console.error("Received incomplete data from BindingPreorderForm:", data);
                toast.error("Failed to create pre-order.\r\nReceived incomplete data.");
                return;
            }

            // Create pre-order
            bindingsStore.createOrder(data.user, data.type, data.title)
                .then((resp) => {
                    toast.success("Created pre-order with ID " + resp.data.id);
                    this.showItemEditForm = false;
                    (this.$refs.itemOverview as InstanceType<typeof ItemOverview>).reloadItems();
                })
                .catch((error) => {
                    console.error("Failed to create pre-order:", error);
                    toast.error("Failed to create pre-order.\r\n" + APIUtils.createErrorToString(error));
                });
        }
    },
}
</script>
