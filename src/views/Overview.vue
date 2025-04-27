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
                <h1>Overview</h1>
            </v-col>
        </v-row>
        <v-row>
            <v-col>
                <div class="d-flex justify-center flex-wrap">
                    <v-card width="400" min-width="350" class="ma-3">
                        <v-card-title>Items</v-card-title>

                        <v-card-text v-if="!statisticsLodaded">
                            <v-skeleton-loader
                                type="card"
                                :loading="true"
                                max-width="380"
                                class="mx-auto"
                            ></v-skeleton-loader>
                        </v-card-text>
                        <v-card-text v-else class="text-center">
                            <v-tooltip text="Red: Bound | Green: Unbound">
                                <template v-slot:activator="{ props }">
                                    <v-progress-circular
                                        :model-value="itemsBoundPercentage"
                                        v-bind="props"
                                        size="150"
                                        width="25"
                                        color="red"
                                        bg-color="green"
                                    >
                                        <h1 class="text-black font-weight-light">{{ Math.round(itemsBoundPercentage) }}%</h1>
                                    </v-progress-circular>
                                </template>
                            </v-tooltip>

                            <div class="d-flex mt-4 justify-center ga-3">
                                <v-chip
                                    variant="text"
                                    prepend-icon="mdi-basket-outline"
                                    class="cursor-default"
                                >
                                    {{ statistics.items.total }} ({{ statistics.items.templates }})
                                    <v-tooltip activator="parent" location="top">
                                        <span>Total items (templates)</span>
                                    </v-tooltip>
                                </v-chip>

                                <v-chip
                                    variant="text"
                                    prepend-icon="mdi-basket-plus-outline"
                                    class="cursor-default text-red-accent-4"
                                >
                                    {{ statistics.items.bound }}
                                    <v-tooltip activator="parent" location="top">
                                        <span>Bound items</span>
                                    </v-tooltip>
                                </v-chip>

                                <v-chip
                                    variant="text"
                                    prepend-icon="mdi-basket-minus-outline"
                                    class="cursor-default text-green-darken-3"
                                >
                                    {{ statistics.items.total - statistics.items.bound - statistics.items.private }}
                                    <v-tooltip activator="parent" location="top">
                                        <span>Available items</span>
                                    </v-tooltip>
                                </v-chip>

                                <v-chip
                                    variant="text"
                                    prepend-icon="mdi-basket-off-outline"
                                    class="cursor-default text-brown"
                                >
                                    {{ statistics.items.private }}
                                    <v-tooltip activator="parent" location="top">
                                        <span>Private items</span>
                                    </v-tooltip>
                                </v-chip>
                            </div>
                        </v-card-text>
                    </v-card>

                    <v-card width="400" min-width="350" class="ma-3">
                        <v-card-title>Users</v-card-title>

                        <v-card-text v-if="!statisticsLodaded">
                            <v-skeleton-loader
                                type="card"
                                :loading="true"
                                max-width="380"
                                class="mx-auto"
                            ></v-skeleton-loader>
                        </v-card-text>
                        <v-card-text v-else class="text-center">

                            <v-tooltip text="Red: With Bindings | Green: Nothing issued">
                                <template v-slot:activator="{ props }">
                                    <v-progress-circular
                                        :model-value="usersWithBindingsPercentage"
                                        v-bind="props"
                                        size="150"
                                        width="25"
                                        color="red"
                                        bg-color="green"
                                    >
                                        <h1 class="text-black font-weight-light">{{ Math.round(usersWithBindingsPercentage) }}%</h1>
                                    </v-progress-circular>
                                </template>
                            </v-tooltip>

                            <div class="d-flex mt-4 justify-center ga-3">
                                <v-chip
                                    variant="text"
                                    prepend-icon="mdi-account-group"
                                    class="cursor-default"
                                >
                                    {{ statistics.users.total }}
                                    <v-tooltip activator="parent" location="top">
                                        <span>Total users</span>
                                    </v-tooltip>
                                </v-chip>

                                <v-chip
                                    variant="text"
                                    prepend-icon="mdi-account-arrow-right-outline"
                                    class="cursor-default text-red-accent-4"
                                >
                                    {{ statistics.users.with_bindings }}
                                    <v-tooltip activator="parent" location="top">
                                        <span>Users with bindings</span>
                                    </v-tooltip>
                                </v-chip>


                                <v-chip
                                    variant="text"
                                    prepend-icon="mdi-account-arrow-left-outline"
                                    class="cursor-default text-green-darken-3"
                                >
                                    {{ statistics.users.without_bindings }}
                                    <v-tooltip activator="parent" location="top">
                                        <span>Users without bindings</span>
                                    </v-tooltip>
                                </v-chip>
                            </div>
                        </v-card-text>
                    </v-card>
                </div>
            </v-col>
        </v-row>
        <v-row class="mt-0">
            <v-col class="pt-0 text-center">
                <LastUpdated :date="statisticsUpdated"/>
            </v-col>
        </v-row>
        <v-row class="mt-0">
            <v-col class="text-center">
                <v-btn
                    color="info"
                    prepend-icon="mdi-chart-box-outline"
                    class="mx-4"
                    @click="$router.push('/inventory')"
                >
                    Show More
                </v-btn>
            </v-col>
        </v-row>
        <v-row class="mt-5">
            <v-col class="text-center">
                <v-btn
                    size="x-large"
                    color="success"
                    prepend-icon="mdi-plus"
                    class="ma-md-4 ma-2"
                    @click="$router.push('/bindings/issue')"
                >
                    Issue Items
                </v-btn>
                <v-btn
                    size="x-large"
                    color="error"
                    prepend-icon="mdi-trash-can-outline"
                    class="ma-md-4 ma-2"
                    @click="$router.push('/bindings/return')"
                >
                    Return Items
                </v-btn>
            </v-col>
        </v-row>
        <v-row>
            <v-col>
                <h2>Latest Events</h2>
            </v-col>
        </v-row>
        <v-row>
            <v-col>
                <EventTimeline
                    :events="logEvents"
                ></EventTimeline>
            </v-col>
        </v-row>
    </v-container>
</template>

<script lang="ts">
import {defineComponent} from "vue";

import {useBindingsStore} from "@/store/bindings";
import type {SystemStatistics} from "@/types/SystemStatistics";
import EventTimeline from "@/components/EventTimeline.vue";
import {useEventLogStore} from "@/store/eventlog";
import LastUpdated from "@/components/LastUpdated.vue";

const bindingsStore = useBindingsStore();
const eventLogStore = useEventLogStore();

export default defineComponent({
    name: "Overview",

    components: {LastUpdated, EventTimeline},

    data() {
        return {
            refreshIntervallId: null as ReturnType<typeof setInterval> | null,

            statisticsLodaded: false,
            statisticsUpdated: new Date(0),
            statistics: {} as SystemStatistics,

            logEventsLoaded: false,
            logEvents: [],
        }
    },

    computed: {
        itemsBoundPercentage() {
            if (!this.statistics.items.total) {
                return 0;
            } else {
                return this.statistics.items.bound / (this.statistics.items.total - this.statistics.items.private) * 100;
            }
        },
        usersWithBindingsPercentage() {
            if (!this.statistics.users.total) {
                return 0;
            } else {
                return this.statistics.users.with_bindings / this.statistics.users.total * 100;
            }
        },
    },

    methods: {
        refreshData() {
            bindingsStore.fetchStatistics().then((response) => {
                this.statistics = response;
                this.statisticsUpdated = new Date();
                this.statisticsLodaded = true;
            });

            eventLogStore.fetchEventLogsPage(1, 10, ['timestamp'], '').then((response) => {
                this.logEvents = response.items;
                this.logEventsLoaded = true;
            });
        }
    },

    mounted() {
        this.refreshData();
        this.refreshIntervallId = setInterval(this.refreshData, 30000);
    },

    beforeUnmount() {
        clearInterval(this.refreshIntervallId as any);
    }
})
</script>