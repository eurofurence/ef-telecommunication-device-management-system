<template>
    <v-card
        prepend-icon="mdi-cellphone-basic"
        variant="flat"
    >
        <template v-slot:title>
            <div class="d-flex justify-space-between align-center">
                <div>Radio Devices</div>
                <div>
                    <v-btn
                        class="my-2"
                        color="primary"
                        @click="switchTab()"
                        :variant="tab === 'templates' ? 'elevated' : 'outlined'"
                    >
                        <v-icon start icon="mdi-shape-outline"></v-icon>
                        Templates
                    </v-btn>
                </div>
            </div>
        </template>

        <v-card-text>
            <v-window v-model="tab" direction="vertical">
                <v-window-item value="items">
                    <v-data-table-server
                        v-model:items-per-page="tables.items.itemsPerPage"
                        :headers="tables.items.headers"
                        :items-length="tables.items.totalItems"
                        :items="tables.items.serverItems"
                        :loading="tables.items.loading"
                        :search="tables.items.search"
                        item-value="name"
                        @update:options="loadItems"
                    >
                        <template v-slot:top>
                            <v-text-field
                                v-model="tables.items.search"
                                label="Search"
                                single-line
                                hide-details
                                clearable
                            ></v-text-field>
                        </template>
                    </v-data-table-server>
                </v-window-item>

                <v-window-item value="templates">
                    <v-data-table-server
                        v-model:items-per-page="tables.templates.itemsPerPage"
                        :headers="tables.templates.headers"
                        :items-length="tables.templates.totalItems"
                        :items="tables.templates.serverItems"
                        :loading="tables.templates.loading"
                        :search="tables.templates.search"
                        item-value="name"
                        @update:options="loadTempaltes"
                    >
                        <template v-slot:top>
                            <v-text-field
                                v-model="tables.templates.search"
                                label="Search"
                                single-line
                                hide-details
                                clearable
                            ></v-text-field>
                        </template>
                    </v-data-table-server>
                </v-window-item>
            </v-window>
        </v-card-text>
    </v-card>
</template>

<script type="ts">
import {useItemsStore} from "@/store/items";

const itemsStore = useItemsStore();

export default {
    data: () => ({
        tab: 'items',
        tables: {
            'items': {
                headers: [
                    {key: 'id', title: 'Device-ID', align: 'start', sortable: true},
                    {key: 'template', title: 'Template', align: 'start', sortable: true},
                    {key: 'callsign', title: 'Callsign', align: 'start', sortable: true},
                    {key: 'serialnumber', title: 'S/N', align: 'start', sortable: true},
                    {key: 'handed_out', title: 'Status', align: 'start', sortable: true},
                    {key: 'notes', title: 'Notes', align: 'start', sortable: false},
                ],
                search: '',
                serverItems: [],
                loading: true,
                itemsPerPage: 25,
                totalItems: 0,
                fetchFunction: itemsStore.fetchRadiosPage,
            },
            'templates': {
                headers: [
                    {key: 'id', title: 'Template-ID', align: 'start', sortable: true},
                    {key: 'name', title: 'Name', align: 'start', sortable: true},
                    {key: 'description', title: 'Description', align: 'start', sortable: true},
                ],
                search: '',
                serverItems: [],
                loading: true,
                itemsPerPage: 25,
                totalItems: 0,
                fetchFunction: itemsStore.fetchRadioTemplatesPage,
            }
        },
    }),

    methods: {
        switchTab() {
            if (this.tab === 'items') {
                this.tab = 'templates';
            } else {
                this.tab = 'items';
            }
        },

        loadItems({page, itemsPerPage, sortBy, search}) {
            this.tables.items.loading = true;
            this.tables.items.fetchFunction(page, itemsPerPage, sortBy, search).then(({items, total}) => {
                this.tables.items.serverItems = items;
                this.tables.items.totalItems = total;
                this.tables.items.loading = false;
            });
        },

        loadTempaltes({page, itemsPerPage, sortBy, search}) {
            this.tables.templates.loading = true;
            this.tables.templates.fetchFunction(page, itemsPerPage, sortBy, search).then(({items, total}) => {
                this.tables.templates.serverItems = items;
                this.tables.templates.totalItems = total;
                this.tables.templates.loading = false;
            });
        }
    }
}
</script>