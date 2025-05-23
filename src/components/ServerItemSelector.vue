<!--
Eurofurence Telecommunication Device Management System (EF-TDMS)
Copyright (C) 2025 Niels Gandraß <niels@gandrass.de>

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
    <v-autocomplete
        :label="label"
        :placeholder="placeholder"
        v-model="selection"
        :items="items"
        :item-title="itemTitleKey"
        @update:search="updateSearch($event)"
        @update:model-value="$emit('update:selection', $event)"
        :loading="loading"
        :prepend-inner-icon="icon"
        :autofocus="autofocus"
        :no-filter="noFilter"
        clearable
        persistent-clear
        return-object
    >
        <template v-slot:no-data>
            <v-list-item v-if="!loading">
                <v-list-item-title class="text-grey">
                    <span v-if="searchQueryIsValid">No matching items found</span>
                    <span v-else>Enter at least {{ minimumSearchLength }} characters to search</span>
                </v-list-item-title>
            </v-list-item>
            <v-skeleton-loader v-else type="list-item"></v-skeleton-loader>
        </template>

        <template v-slot:append-item v-if="!loading && searchHasMore">
            <v-list-item>
                <v-list-item-title class="text-grey">
                    <span>Not all results shown. Pleas narrow down your search.</span>
                </v-list-item-title>
            </v-list-item>
        </template>
    </v-autocomplete>
</template>

<script lang="ts">
import { defineComponent } from "vue";

export default defineComponent({
    name: "ServerItemSelector",

    props: {
        fetchFunction: {type: Function, required: true},
        availableOnly: {type: Boolean, required: false, default: false},
        label: {type: String, required: true},
        placeholder: {type: String, required: false},
        icon: {type: String, required: false},
        itemTitleKey: {type: String, required: false, default: 'title'},
        autofocus: {type: Boolean, required: false, default: false},
        minimumSearchLength: {type: Number, required: false, default: 1},
        searchPageSize: {type: Number, required: false, default: 10},
        itemIdsToExclude: {type: Array, required: false, default: []},
        noFilter: {type: Boolean, required: false, default: false},
        prefetch: {type: Boolean, required: false, default: false},
        initialSelection: {type: Object, required: false, default: null},
    },

    emits: [
        'update:selection'
    ],

    data: () => ({
        searchQuery: '' as string | null,
        searchDebounceTimeout: null as any,
        searchHasMore: false,
        loading: false,
        selection: null as any,
        items: [],
    }),

    created() {
        if (this.initialSelection) {
            this.selection = this.initialSelection;
        }
        if (this.prefetch) {
            this.searchItems('');
        }
    },

    computed: {
        /**
         * Returns true if the search query is valid
         */
        searchQueryIsValid(): boolean {
            if (!this.searchQuery) {
                return false;
            }

            return this.searchQuery.length >= this.minimumSearchLength;
        }
    },

    methods: {
        /**
         * Handles update:search event emitted by v-autocomplete
         *
         * @param query The new search query value
         */
        updateSearch(query: string): void {
            this.searchQuery = query;
            if (this.searchQueryIsValid) {
                this.searchItems(this.searchQuery);
            } else {
                this.loading = false;
                this.items = [];
                this.searchHasMore = false;
            }
        },

        /**
         * Fetches a page of items from the API based on the search query
         *
         * @param query The search query
         */
        searchItems(query: string): void {
            // Debounce search
            this.loading = true;
            if (this.searchDebounceTimeout) {
                clearTimeout(this.searchDebounceTimeout);
            }
            this.searchDebounceTimeout = setTimeout(async () => {
                // Execute search API call
                let itemPage = await this.fetchFunction(1, this.searchPageSize, [this.itemTitleKey], query, this.availableOnly ? ['available=true'] : []);
                this.items = itemPage.items
                    .filter((item: any) => !this.itemIdsToExclude.includes(item.id))
                    .sort((a: any, b: any) => a[this.itemTitleKey].localeCompare(b[this.itemTitleKey]));
                this.searchHasMore = itemPage.total > this.searchPageSize;
                this.loading = false;
            }, 500);
        },

        /**
         * Clears the selection, if any
         */
        clear(): void {
            this.selection = null;
        }
    }

})
</script>
