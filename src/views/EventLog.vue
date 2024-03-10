<template>
    <v-container>
        <v-row>
            <v-col>
                <h1>Event Log</h1>
            </v-col>
        </v-row>
        <v-row>
            <v-col>
                <v-select
                    v-model="filterEventTypes"
                    :items="LogEventType.getAll()"
                    item-title="label"
                    item-value="key"
                    label="Select"
                    chips
                    multiple
                    @update:model-value="searchUpdated"
                ></v-select>
                <v-text-field
                    v-model="filterSearchText"
                    @update:model-value="searchUpdated"
                ></v-text-field>
            </v-col>
        </v-row>
        <v-row>
            <v-col>
                <EventTimeline
                    :events="logEvents"
                    :loading="!logEventsLoaded"
                ></EventTimeline>
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

            searchDebounceTimeout: null as number,
            filterSearchText: "",
            filterEventTypes: [],
        }
    },

    methods: {
        searchUpdated() {
            this.refreshData();
        },

        async refreshData() {
            // Indicate loading in UI
            this.logEventsLoaded = false;

            // Debounce API call
            if (this.searchDebounceTimeout) {
                clearTimeout(this.searchDebounceTimeout);
            }

            this.searchDebounceTimeout = setTimeout(async () => {
                // Filter for event types
                if (this.filterEventTypes.length > 0) {
                    console.log("TODO");
                }

                // Execute API call
                eventLogStore.fetchEventLogsPage(1, 25, ['timestamp'], this.filterSearchText).then((response) => {
                    this.logEvents = response.items;
                    this.logEventsLoaded = true;
                })
            }, 500);
        }
    },

    mounted() {
        this.refreshData();
    },

})
</script>