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
    <v-container class="main-container-boxed">
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

            searchDebounceTimeout: null as ReturnType<typeof setTimeout>|null,
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