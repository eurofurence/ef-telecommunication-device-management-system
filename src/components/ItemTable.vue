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
            <v-window v-model="tab" direction="vertical">
                <v-window-item value="items" v-if="itemsTable">
                    <v-data-table-server
                        v-model:items-per-page="itemsTable.itemsPerPage"
                        :headers="itemsTable.headers"
                        :items-length="itemsTable.totalItems"
                        :items="itemsTable.serverItems"
                        :loading="itemsTable.loading"
                        :search="itemsTable.search"
                        item-value="name"
                        @update:options="loadItems"
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
                    </v-data-table-server>
                </v-window-item>

                <v-window-item value="templates" v-if="templatesTable">
                    <v-data-table-server
                        v-model:items-per-page="templatesTable.itemsPerPage"
                        :headers="templatesTable.headers"
                        :items-length="templatesTable.totalItems"
                        :items="templatesTable.serverItems"
                        :loading="templatesTable.loading"
                        :search="templatesTable.search"
                        item-value="name"
                        @update:options="loadTempaltes"
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

export default defineComponent({
    props: {
        title: {type: String, required: true},
        icon: {type: String, required: false},
        itemsTable: {type: Object as PropType<ServerTableMetadata>, required: true},
        templatesTable: {type: Object as PropType<ServerTableMetadata>, required: false}
    },

    data: () => ({
        tab: 'items',
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
        }
    }
})
</script>
