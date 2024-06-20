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
                        :prevent-create="itemsTable.preventCreate ?? false"
                        :prevent-edit="itemsTable.preventEdit ?? false"
                        :prevent-delete="itemsTable.preventDelete ?? false"
                        @click:create-item="$emit('click:createItem', $event)"
                        @click:edit-item="$emit('click:editItem', $event)"
                        @click:delete-items="$emit('click:deleteItems', $event)"
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
                        :prevent-create="templatesTable.preventCreate ?? false"
                        :prevent-edit="templatesTable.preventEdit ?? false"
                        :prevent-delete="templatesTable.preventDelete ?? false"
                        @click:create-item="$emit('click:createItemTemplate', $event)"
                        @click:edit-item="$emit('click:editItemTemplate', $event)"
                        @click:delete-items="$emit('click:deleteItemTemplates', $event)"
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
import ItemTable from "@/components/ItemTable.vue";

export default defineComponent({
    name: "ItemOverview",

    expose: [
        'reloadItems',
        'reloadTemplates',
        'deselectItemsByKey',
        'deselectTemplatesByKey',
    ],

    components: {
        ItemTable,
    },

    emits: [
        'click:createItem',
        'click:createItemTemplate',
        'click:editItem',
        'click:editItemTemplate',
        'click:deleteItems',
        'click:deleteItemTemplates',
    ],

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
            (this.$refs.itemsTable as InstanceType<typeof ItemTable>).reload();
        },

        reloadTemplates() {
            (this.$refs.templatesTable as InstanceType<typeof ItemTable>).reload();
        },

        deselectItemsByKey(keys: number[]) {
            (this.$refs.itemsTable as InstanceType<typeof ItemTable>).deselectItemsByKey(keys);
        },

        deselectTemplatesByKey(keys: number[]) {
            (this.$refs.templatesTable as InstanceType<typeof ItemTable>).deselectItemsByKey(keys);
        },
    },
})
</script>
