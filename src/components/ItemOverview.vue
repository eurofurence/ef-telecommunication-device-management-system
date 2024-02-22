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
                    <ItemTable
                        ref="itemsTable"
                        :headers="itemsTable.headers"
                        :expanded-row-props="itemsTable.expandedRowProps ?? []"
                        :fetch-function="itemsTable.fetchFunction"
                        :initial-search="itemsTable.search ?? ''"
                        :items-per-page="itemsTable.itemsPerPage ?? 25"
                    ></ItemTable>
                </v-window-item>

                <v-window-item value="templates" v-if="templatesTable">
                    <ItemTable
                        ref="templatesTable"
                        :headers="templatesTable.headers"
                        :expanded-row-props="templatesTable.expandedRowProps ?? []"
                        :fetch-function="templatesTable.fetchFunction"
                        :initial-search="templatesTable.search ?? ''"
                        :items-per-page="templatesTable.itemsPerPage ?? 25"
                    ></ItemTable>
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
import ItemTable from "@/components/ItemTable.vue";

export default defineComponent({
    name: "ItemOverview",

    components: {
        ItemTable,
    },

    props: {
        title: {type: String, required: true},
        icon: {type: String, required: false},
        itemsTable: {type: Object as PropType<ServerTableMetadata>, required: true},
        templatesTable: {type: Object as PropType<ServerTableMetadata>, required: false},
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

        reloadItems() {
            this.$refs.itemsTable.reload();
        },

        reloadTemplates() {
            this.$refs.templatesTable.reload();
        },
    },
})
</script>
