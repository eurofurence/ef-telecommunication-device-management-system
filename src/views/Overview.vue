<template>
    <v-container class="main-container-boxed">
        <v-row>
            <v-col>
                <h1>Overview</h1>
            </v-col>
        </v-row>
        <v-row>
            <v-col>
                <div class="d-flex justify-center">
                    <v-card width="400" class="ma-3">
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

                    <v-card width="400" class="ma-3">
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
        <v-row>
            <v-col>
                <Doughnut
                    :data="chartData"
                    :options="chartOptions"
                ></Doughnut>
            </v-col>
        </v-row>
        <v-row>
            <v-col class="text-center">
                <v-btn
                    size="x-large"
                    color="success"
                    prepend-icon="mdi-plus"
                    class="mx-4"
                    @click="$router.push('/bindings/issue')"
                >
                    Issue Items
                </v-btn>
                <v-btn
                    size="x-large"
                    color="error"
                    prepend-icon="mdi-trash-can-outline"
                    class="mx-4"
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
import {SystemStatistics} from "@/types/SystemStatistics";
import EventTimeline from "@/components/EventTimeline.vue";
import {useEventLogStore} from "@/store/eventlog";

import { Doughnut } from 'vue-chartjs'
import { Chart as ChartJS, RadialLinearScale, ArcElement, Tooltip, Legend } from 'chart.js'
import {ItemType} from "@/types/ItemType";

ChartJS.register(RadialLinearScale, ArcElement, Tooltip, Legend)

const bindingsStore = useBindingsStore();
const eventLogStore = useEventLogStore();

export default defineComponent({
    name: "Overview",

    components: {EventTimeline, Doughnut},

    data() {
        return {
            refreshIntervallId: null as ReturnType<typeof setInterval> | null,

            statisticsLodaded: false,
            statistics: {} as SystemStatistics,

            logEventsLoaded: false,
            logEvents: [],

            chartOptions: {
                responsive: true,
                legend: {
                    display: false,
                },
                plugins: {
                    tooltip: {
                        callbacks: {
                            title: (items) => items[0].dataset.titles[items[0].dataIndex] ?? '',
                            label: (ctx) => ` ${ctx.dataset.labels[ctx.dataIndex]}: ${ctx.formattedValue}`,
                        }
                    },
                }
            },
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
        chartData() {
            if (!this.statisticsLodaded) {
                return {
                    labels: ['Loading...'],
                    datasets: [{data: [1]}]
                }
            }

            let datasets = {
                itemTypes: {
                    labels: [],
                    titles: [],
                    data: [],
                    backgroundColor: [],
                    weight: 0.5,
                },
                tplTotals: {
                    labels: [],
                    titles: [],
                    data: [],
                    backgroundColor: [],
                },
                tplAvailability: {
                    labels: [],
                    titles: [],
                    data: [],
                    backgroundColor: [],
                    weight: 0.3,
                }
            }

            for (const [itemTypeKey, templates] of Object.entries(this.statistics.templates)) {
                const itemType = ItemType.get(itemTypeKey);
                let itemTypeTotal = 0;
                let itemTypeBound = 0;
                let itemTypePrivate = 0;

                for (const tpl of templates) {
                    // Segment for total item count of template
                    datasets.tplTotals.titles.push(itemType.label);
                    datasets.tplTotals.labels.push(tpl.pretty_name);
                    datasets.tplTotals.data.push(tpl.total);
                    datasets.tplTotals.backgroundColor.push(itemType.color);

                    // Segments for (un-)available items of template
                    if (!tpl.private) {
                        datasets.tplAvailability.titles.push(tpl.pretty_name);
                        datasets.tplAvailability.labels.push('Available');
                        datasets.tplAvailability.data.push(tpl.total - tpl.bound);
                        datasets.tplAvailability.backgroundColor.push('#00AA00');

                        datasets.tplAvailability.titles.push(tpl.pretty_name);
                        datasets.tplAvailability.labels.push('Handed out');
                        datasets.tplAvailability.data.push(tpl.bound);
                        datasets.tplAvailability.backgroundColor.push('#AA0000');

                        itemTypeBound += tpl.bound;
                    } else {
                        datasets.tplAvailability.titles.push(tpl.pretty_name);
                        datasets.tplAvailability.labels.push('Private');
                        datasets.tplAvailability.data.push(tpl.total);
                        datasets.tplAvailability.backgroundColor.push('#AAAAAA');

                        itemTypePrivate += tpl.total;
                    }

                    itemTypeTotal += tpl.total;
                }

                datasets.itemTypes.labels.push(itemType.label);
                datasets.itemTypes.data.push(itemTypeTotal);
                datasets.itemTypes.backgroundColor.push(itemType.color + 'CC');
            }

            return {
                labels: datasets.itemTypes.labels,
                datasets: Object.values(datasets),
            }
        }
    },

    methods: {
        refreshData() {
            bindingsStore.fetchStatistics().then((response) => {
                this.statistics = response;
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
        this.refreshIntervallId = setInterval(this.refreshData, 15000);
    },

    beforeUnmount() {
        clearInterval(this.refreshIntervallId as any);
    }
})
</script>