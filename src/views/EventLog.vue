<template>
    <v-container>
        <v-row>
            <v-col>
                <h1>Event Log</h1>
            </v-col>
        </v-row>
        <v-row>
            <v-col cols="12" md="6" class="py-0">
                <v-select
                    v-model="filterEventTypes"
                    :items="LogEventType.getAll()"
                    item-title="label"
                    item-value="key"
                    label="Event Type"
                    multiple
                    clearable
                    prepend-inner-icon="mdi-filter-outline"
                    @update:model-value="searchUpdated"
                >
                    <template v-slot:selection="{ item, index }">
                        <v-chip v-if="index < 2">
                            <span>{{ item.title }}</span>
                        </v-chip>
                        <span
                            v-if="index === 2"
                            class="text-grey text-caption align-self-center"
                        >
                        (+{{ filterEventTypes.length - 2 }} others)
                      </span>
                    </template>
                </v-select>
            </v-col>
            <v-col cols="12" md="6" class="py-0">
                <v-text-field
                    v-model="filterSearchText"
                    label="Search"
                    prepend-inner-icon="mdi-magnify"
                    @update:model-value="searchUpdated"
                ></v-text-field>
            </v-col>
        </v-row>
        <v-row>
            <v-col>
                <EventTimeline
                    :events="Object.values(logEvents)"
                    :loading="!logEventsLoaded"
                    :loader-height="pageSize"
                ></EventTimeline>
            </v-col>
        </v-row>
        <v-row>
            <v-col>
                <v-pagination
                    v-model="currentPage"
                    :length="maxPages"
                    @update:model-value="refreshData"
                ></v-pagination>
            </v-col>
        </v-row>
    </v-container>
</template>

<script lang="ts" setup>
import {LogEventType} from "@/types/LogEvent";
</script>

<script lang="ts">
import {defineComponent} from "vue";

import EventTimeline from "@/components/EventTimeline.vue";
import {useEventLogStore} from "@/store/eventlog";

const eventLogStore = useEventLogStore();

export default defineComponent({
    name: "EventLog",

    components: {EventTimeline},

    data() {
        return {
            logEventsLoaded: false,
            logEvents: [],

            currentPage: 1,
            maxPages: 1,
            pageSize: 25,

            searchDebounceTimeout: null as number,
            filterSearchText: "",
            filterEventTypes: [],
        }
    },

    methods: {
        searchUpdated() {
            this.logEvents = [];
            this.currentPage = 1;
            this.refreshData();
        },

        refreshData() {
            // Indicate loading in UI and reset internal data state
            this.logEventsLoaded = false;

            // Debounce API call
            if (this.searchDebounceTimeout) {
                clearTimeout(this.searchDebounceTimeout);
            }

            this.searchDebounceTimeout = setTimeout(() => {
                eventLogStore.fetchEventLogsPage(this.currentPage, this.pageSize, ['timestamp'], this.filterSearchText, this.filterEventTypes).then((response) => {
                    this.logEvents = response.items;
                    this.maxPages = Math.ceil(response.total/this.pageSize);
                    this.logEventsLoaded = true;
                })
            }, 500);
        },
    },

    mounted() {
        this.refreshData();
    },

})
</script>