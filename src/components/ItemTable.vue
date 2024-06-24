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
    <v-data-table-server
        :key="tableKey"
        v-model="selected"
        v-model:items-per-page="currentItemsPerPage"
        :headers="headers as any[]"
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
                        :disabled="preventDelete"
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
                        :disabled="preventCreate"
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

        <template v-slot:item.handed_out="{item}: {item: any}">
            <v-chip
                v-if="!item.template.private"
                :color="item.handed_out ? 'error' : 'success'"
                text-color="white"
            >
                {{ item.handed_out ? 'Handed out' : 'Available' }}
                <v-tooltip
                    v-if="item.handed_out"
                    activator="parent"
                    :text="item.handed_out"
                ></v-tooltip>
            </v-chip>
            <v-chip
                v-if="item.template.private"
                color="grey"
                text-color="white"
            >
                Private
            </v-chip>
        </template>

        <template v-slot:item.private="{item}: {item: any}">
            <v-chip
                :color="item.private ? 'error' : 'success'"
                text-color="white"
            >
                {{ item.private ? 'Yes' : 'No' }}
            </v-chip>
        </template>

        <template v-slot:item.allow_quickadd="{item}: {item: any}">
            <v-chip
                :color="item.allow_quickadd ? 'success' : 'error'"
                text-color="white"
            >
                {{ item.allow_quickadd ? 'Yes' : 'No' }}
            </v-chip>
        </template>

        <template v-slot:item.has_camera="{item}: {item: any}">
            <v-chip
                :color="item.has_camera ? 'success' : 'error'"
                text-color="white"
            >
                {{ item.has_camera ? 'Yes' : 'No' }}
            </v-chip>
        </template>

        <template v-slot:item.color="{item}: {item: any}">
            <v-chip
                :color="item.color"
            >
                {{ item.color }}
            </v-chip>
        </template>

        <template v-slot:item.coding="{item}: {item: any}">
            <v-chip
                :color="item.coding.color"
            >
                {{ item.coding.name }}
            </v-chip>
        </template>

        <template v-slot:item.template.coding="{item}: {item: any}">
            <v-chip
                :color="item.template.coding.color"
            >
                {{ item.template.coding.name }}
            </v-chip>
        </template>

        <template v-slot:item.type="{item}: {item: any}">
            <v-tooltip :text="item.type">
                <template v-slot:activator="{ props }">
                    <v-icon
                        v-bind="props"
                        :icon="ItemType.get(item.type) ? ItemType.get(item.type).icon : 'mdi-shape-outline'"
                    ></v-icon>
                </template>

            </v-tooltip>
        </template>

        <template v-slot:item.notes="{item}: {item: any}">
            <v-tooltip v-if="item.notes" :text="item.notes">
                <template v-slot:activator="{ props }">
                    <v-icon v-bind="props">mdi-information-outline</v-icon>
                </template>
            </v-tooltip>
        </template>

        <template v-slot:expanded-row="{ columns, item }: {columns: any, item: any}">
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
                        class="ml-4 mb-4"
                        color="warning"
                        :disabled="preventEdit"
                        @click="$emit('click:editItem', item)"
                    >
                        <v-icon left>mdi-pencil</v-icon>
                        Edit
                    </v-btn>

                    <v-btn
                        class="ml-4 mb-4"
                        color="error"
                        :disabled="preventDelete"
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

<script lang="ts" setup>
import {ItemType} from "@/types/ItemType";
</script>

<script lang="ts">
import { defineComponent } from "vue";
import type { PropType } from "vue";

import {PropUtils} from "@/classes/util/PropUtils";
import {ExpandedRowProp} from "@/types/ExpandedRowProps";
import {TableHeader} from "@/types/TableHeader";

export default defineComponent({
    name: "ItemTable",

    expose: [
        'reload',
        'deselectItemsByKey',
    ],

    emits: [
        'click:createItem',
        'click:editItem',
        'click:deleteItems',
    ],

    computed: {
        PropUtils() {
            return PropUtils
        }
    },

    props: {
        headers: {type: Array<TableHeader>, required: true},
        fetchFunction: {type: Function, required: true},
        expandedRowProps: {type: Array as PropType<ExpandedRowProp[]>, required: false, default: null},
        initialSearch: {type: String, required: false, default: ''},
        itemsPerPage: {type: Number, required: false, default: 25},
        preventCreate: {type: Boolean, required: false, default: false},
        preventEdit: {type: Boolean, required: false, default: false},
        preventDelete: {type: Boolean, required: false, default: false},
    },

    data: () => ({
        tableKey: 0,
        loading: true,
        totalItems: 0,
        currentItemsPerPage: 25,
        serverItems: [] as any[],
        selected: [] as any[],
        search: '',
        searchDebounceTimeout: null as any,
    }),

    created() {
        this.search = this.initialSearch;
    },

    watch: {
        itemsPerPage() {
            this.currentItemsPerPage = this.itemsPerPage;
        },
    },

    methods: {
        loadItems({page, itemsPerPage, sortBy, search}: {page: number, itemsPerPage: number, sortBy: string, search: string}) {
            this.loading = true;

            // Debounce search
            if (this.searchDebounceTimeout) {
                clearTimeout(this.searchDebounceTimeout);
            }
            this.searchDebounceTimeout = setTimeout(async () => {
                this.fetchFunction(page, itemsPerPage, sortBy, search).then(({items, total}: {items: any[], total: number}) => {
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
