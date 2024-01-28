<template>
    <v-card
        :prepend-icon="icon"
        variant="flat"
    >
        <template v-slot:title>
            <div class="d-flex justify-space-between align-center">
                <div>{{ title }}</div>
                <div v-if="templatesTable">
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
            <v-window v-model="tab" direction="horizontal">
                <v-window-item value="items" v-if="itemsTable">
                    <v-data-table-server
                        :key="itemsTableKey"
                        v-model="itemsTableSelected"
                        v-model:items-per-page="itemsTable.itemsPerPage"
                        :headers="itemsTable.headers"
                        :items-length="itemsTable.totalItems"
                        :items="itemsTable.serverItems"
                        :loading="itemsTable.loading"
                        :search="itemsTable.search"
                        item-value="id"
                        @update:options="loadItems"
                        density="comfortable"
                        show-select
                        show-expand
                    >
                        <template v-slot:top>
                            <v-text-field
                                v-model="itemsTable.search"
                                label="Search"
                                single-line
                                hide-details
                                clearable
                            ></v-text-field>
                        </template>

                        <template v-slot:loading>
                            <v-skeleton-loader type="table-row@10"></v-skeleton-loader>
                        </template>

                        <template v-slot:item.handed_out="{item}">
                            <v-chip
                                :color="item.handed_out ? 'error' : 'success'"
                                text-color="white"
                            >
                                {{ item.handed_out ? 'Handed out' : 'Available' }}
                            </v-chip>
                        </template>

                        <template v-slot:item.has_camera="{item}">
                            <v-chip
                                :color="item.has_camera ? 'success' : 'error'"
                                text-color="white"
                            >
                                {{ item.has_camera ? 'Yes' : 'No' }}
                            </v-chip>
                        </template>

                        <template v-slot:body.append>
                            <v-btn
                                v-if="itemsTableSelected.length > 0"
                                color="error"
                                @click="$emit('deleteItems', itemsTableSelected)"
                            >
                                <v-icon left>mdi-trash-can-outline</v-icon>
                                Delete
                            </v-btn>
                            <v-btn
                                color="primary"
                                @click="$emit('createItem')"
                            >
                                <v-icon left>mdi-plus</v-icon>
                                Create
                            </v-btn>
                            <v-btn
                                color="info"
                                @click="reloadItems"
                            >
                                <v-icon left>mdi-refresh</v-icon>
                                Refresh
                            </v-btn>
                        </template>

                        <template v-slot:expanded-row="{ columns, item }">
                            <tr>
                                <td :colspan="columns.length">
                                    <v-list lines="one" v-if="itemsTable.expandedRowProps">
                                        <v-list-item
                                            v-for="prop in itemsTable.expandedRowProps"
                                            :key="prop.key"
                                        >
                                            <v-list-item-title>{{ prop.title }}</v-list-item-title>
                                            <v-list-item-subtitle>{{ PropUtils.getPropByStringPath(item, prop.key) || "—" }}</v-list-item-subtitle>
                                        </v-list-item>
                                    </v-list>

                                    <v-btn
                                        class="mx-4 mb-4"
                                        color="error"
                                        @click="$emit('deleteItems', [item.id])"
                                    >
                                        <v-icon left>mdi-trash-can-outline</v-icon>
                                        Delete
                                    </v-btn>
                                </td>
                            </tr>
                        </template>
                    </v-data-table-server>
                </v-window-item>

                <v-window-item value="templates" v-if="templatesTable">
                    <v-data-table-server
                        :key="templatesTableKey"
                        v-model="templatesTableSelected"
                        v-model:items-per-page="templatesTable.itemsPerPage"
                        :headers="templatesTable.headers"
                        :items-length="templatesTable.totalItems"
                        :items="templatesTable.serverItems"
                        :loading="templatesTable.loading"
                        :search="templatesTable.search"
                        item-value="id"
                        @update:options="loadTempaltes"
                        density="comfortable"
                        show-select
                        show-expand
                    >
                        <template v-slot:top>
                            <v-text-field
                                v-model="templatesTable.search"
                                label="Search"
                                single-line
                                hide-details
                                clearable
                            ></v-text-field>
                        </template>

                        <template v-slot:loading>
                            <v-skeleton-loader type="table-row@10"></v-skeleton-loader>
                        </template>

                        <template v-slot:expanded-row="{ columns, item }">
                            <tr>
                                <td :colspan="columns.length">
                                    <ul v-if="templatesTable.expandedRowProps">
                                        <li v-for="prop in templatesTable.expandedRowProps">
                                            {{ prop.title }}: {{ PropUtils.getPropByStringPath(item, prop.key) }}
                                        </li>
                                    </ul>
                                    <v-btn
                                        color="error"
                                        @click="$emit('deleteItemTemplates', [item.id])"
                                    >
                                        <v-icon left>mdi-trash-can-outline</v-icon>
                                        Delete
                                    </v-btn>
                                </td>
                            </tr>
                        </template>
                    </v-data-table-server>
                </v-window-item>
            </v-window>
        </v-card-text>
    </v-card>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import type { PropType } from "vue";

import type { ServerTableMetadata } from "@/types/ServerTableMetadata";
import {PropUtils} from "@/classes/util/PropUtils";

export default defineComponent({
    computed: {
        PropUtils() {
            return PropUtils
        }
    },
    props: {
        title: {type: String, required: true},
        icon: {type: String, required: false},
        itemsTable: {type: Object as PropType<ServerTableMetadata>, required: true},
        templatesTable: {type: Object as PropType<ServerTableMetadata>, required: false},
    },

    data: () => ({
        tab: 'items',
        itemsTableKey: 0,
        itemsTableSelected: [],
        templatesTableKey: 0,
        templatesTableSelected: [],
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
            this.itemsTable.loading = true;
            this.itemsTable.fetchFunction(page, itemsPerPage, sortBy, search).then(({items, total}) => {
                this.itemsTable.serverItems = items;
                this.itemsTable.totalItems = total;
                this.itemsTable.loading = false;
            });
        },

        loadTempaltes({page, itemsPerPage, sortBy, search}) {
            if (!this.templatesTable) {
                return;
            }

            this.templatesTable.loading = true;
            this.templatesTable.fetchFunction(page, itemsPerPage, sortBy, search).then(({items, total}) => {
                this.templatesTable.serverItems = items;
                this.templatesTable.totalItems = total;
                this.templatesTable.loading = false;
            });
        },

        reloadItems() {
            this.itemsTableKey++;
        },

        reloadTempaltes() {
            this.templatesTableKey++;
        }
    },
})
</script>
