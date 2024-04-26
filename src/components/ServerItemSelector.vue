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
    },

    emits: [
        'update:selection'
    ],

    data: () => ({
        searchQuery: '' as string | null,
        searchDebounceTimeout: null as any,
        searchHasMore: false,
        loading: false,
        selection: null,
        items: [],
    }),

    created() {
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
                let itemPage = await this.fetchFunction(1, this.searchPageSize, [this.itemTitleKey], query, this.availableOnly);
                this.items = itemPage.items.filter((item: any) => !this.itemIdsToExclude.includes(item.id))
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
