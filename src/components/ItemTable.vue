<template>
    <v-data-table-server
        :key="tableKey"
        v-model="selected"
        v-model:items-per-page="itemsPerPage"
        :headers="headers"
        :items-length="totalItems"
        :items="serverItems"
        :loading="loading"
        :search="search"
        item-value="id"
        @update:options="loadItems"
        density="comfortable"
        show-select
        show-expand
        expand-on-click
    >
        <template v-slot:top>
            <div class="d-flex justify-end flex-nowrap">
                <div class="flex-grow-1 flex-shrink-1">
                    <v-sheet>
                        <v-text-field
                            v-model="search"
                            label="Search"
                            prepend-inner-icon="mdi-magnify"
                            single-line
                            hide-details
                            clearable
                        ></v-text-field>
                    </v-sheet>
                </div>
                <div class="flex-align-end flex-shrink-1 ml-2">
                    <v-btn
                        v-if="selected.length > 0"
                        color="error"
                        @click="$emit('click:deleteItems', selected)"
                        class="my-3 mx-1"
                    >
                        <v-icon left>mdi-trash-can-outline</v-icon>
                        Delete
                        <v-tooltip activator="parent" location="top">
                            Delete selected items
                        </v-tooltip>
                    </v-btn>
                    <v-btn
                        v-if="selected.length === 0"
                        color="success"
                        @click="$emit('click:createItem')"
                        class="my-3 mx-1"
                    >
                        <v-icon left>mdi-plus</v-icon>
                        Create
                        <v-tooltip activator="parent" location="top">
                            Create a new item
                        </v-tooltip>
                    </v-btn>
                    <v-tooltip location="top">
                        <template v-slot:activator="{ props }">
                            <v-btn
                                v-bind="props"
                                color="grey-darken-1"
                                @click="reload"
                                class="my-3 mx-1 pa-0"
                                icon="mdi-refresh"
                                density="comfortable"
                            ></v-btn>
                        </template>
                        <span>Reload</span>
                    </v-tooltip>
                </div>
            </div>
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

        <template v-slot:item.color="{item}">
            <v-chip
                :color="item.color"
            >
                {{ item.color }}
            </v-chip>
        </template>

        <template v-slot:item.coding="{item}">
            <v-chip
                :color="item.coding.color"
            >
                {{ item.coding.name }}
            </v-chip>
        </template>

        <template v-slot:item.template.coding="{item}">
            <v-chip
                :color="item.template.coding.color"
            >
                {{ item.template.coding.name }}
            </v-chip>
        </template>

        <template v-slot:item.notes="{item}">
            <v-tooltip v-if="item.notes" :text="item.notes">
                <template v-slot:activator="{ props }">
                    <v-icon v-bind="props">mdi-information-outline</v-icon>
                </template>
            </v-tooltip>
        </template>

        <template v-slot:expanded-row="{ columns, item }">
            <tr>
                <td :colspan="columns.length">
                    <v-list lines="one" v-if="expandedRowProps">
                        <div
                            v-for="prop in expandedRowProps"
                            :key="prop.key"
                        >
                            <v-list-item v-if="!prop.hideMissing || PropUtils.getPropByStringPath(item, prop.key) !== undefined">
                                <v-list-item-title>{{ prop.title }}</v-list-item-title>
                                <v-list-item-subtitle>{{ PropUtils.getPropByStringPath(item, prop.key) || "—" }}</v-list-item-subtitle>
                            </v-list-item>
                        </div>
                    </v-list>

                    <v-btn
                        class="mx-4 mb-4"
                        color="error"
                        @click="$emit('click:deleteItems', [item.id])"
                    >
                        <v-icon left>mdi-trash-can-outline</v-icon>
                        Delete
                    </v-btn>
                </td>
            </tr>
        </template>
    </v-data-table-server>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import type { PropType } from "vue";

import {PropUtils} from "@/classes/util/PropUtils";
import {ExpandedRowProp} from "@/types/ExpandedRowProps";
import {TableHeader} from "@/types/TableHeader";

export default defineComponent({
    name: "ItemTable",

    emits: [
        'click:createItem',
        'click:deleteItems',
    ],

    computed: {
        PropUtils() {
            return PropUtils
        }
    },

    props: {
        headers: {type: Array as PropType<TableHeader[]>, required: true},
        fetchFunction: {type: Function, required: true},
        expandedRowProps: {type: Array as PropType<ExpandedRowProp[]>, required: false, default: null},
        initialSearch: {type: String, required: false, default: ''},
        itemsPerPage: {type: Number, required: false, default: 25},
    },

    data: () => ({
        tableKey: 0,
        loading: true,
        totalItems: 0,
        serverItems: [],
        selected: [],
        search: '',
        searchDebounceTimeout: null as any,
    }),

    created() {
        this.search = this.initialSearch;
    },

    methods: {
        loadItems({page, itemsPerPage, sortBy, search}) {
            this.loading = true;

            // Debounce search
            if (this.searchDebounceTimeout) {
                clearTimeout(this.searchDebounceTimeout);
            }
            this.searchDebounceTimeout = setTimeout(async () => {
                this.fetchFunction(page, itemsPerPage, sortBy, search).then(({items, total}) => {
                    this.serverItems = items;
                    this.totalItems = total;
                    this.loading = false;
                });
            }, 500);
        },

        reload() {
            this.tableKey++;
        },

        deselectItemsByKey(keys: number[]) {
            this.selected = this.selected.filter((key: any) => !keys.includes(key));
        },
    },
})
</script>
