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
    <v-container class="main-container-boxed">
        <v-row>
            <v-col>
                <v-tooltip text="Refresh data">
                    <template v-slot:activator="{ props }">
                        <v-btn
                            v-bind="props"
                            class="float-end"
                            icon="mdi-refresh"
                            @click="refreshData"
                        ></v-btn>
                    </template>
                </v-tooltip>
                <h1>Inventory</h1>
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
        <v-row class="mb-5">
            <v-col>
                <div class="d-flex flex-row flex-wrap justify-center ga-4 mb-n4">
                    <v-tooltip
                        v-for="x in chartItemTypesFilter as any"
                        :text="`${x.active ? 'Hide' : 'Show'} ${x.type.shortLabel}`"
                        location="top"
                    >
                        <template v-slot:activator="{ props }">
                            <v-switch
                                v-bind="props"
                                v-model="x.active"
                                :label="x.type.label"
                                :color="x.type.color"
                                density="compact"
                                hide-details
                            ></v-switch>
                        </template>
                    </v-tooltip>

                    <v-tooltip
                        :text="`${chartShowPrivateItems ? 'Hide' : 'Show'} private items`"
                        location="top"
                    >
                        <template v-slot:activator="{ props }">
                            <v-switch
                                v-bind="props"
                                v-model="chartShowPrivateItems"
                                label="Private"
                                color="grey"
                            ></v-switch>
                        </template>
                    </v-tooltip>
                </div>
                <Doughnut
                    :data="chartData"
                    :options="chartOptions as any"
                    style="max-height: 85vh"
                ></Doughnut>
            </v-col>
        </v-row>
    </v-container>
</template>

<script lang="ts">
import {defineComponent} from "vue";

import {useBindingsStore} from "@/store/bindings";
import {SystemStatistics} from "@/types/SystemStatistics";

import { Doughnut } from 'vue-chartjs'
import { Chart as ChartJS, RadialLinearScale, ArcElement, Tooltip, Legend } from 'chart.js'
import {ItemType} from "@/types/ItemType";
import LastUpdated from "@/components/LastUpdated.vue";

ChartJS.register(RadialLinearScale, ArcElement, Tooltip, Legend)

const bindingsStore = useBindingsStore();

export default defineComponent({
    name: "Inventory",

    components: {LastUpdated, Doughnut},

    data() {
        return {
            refreshIntervallId: null as ReturnType<typeof setInterval> | null,

            statisticsLodaded: false,
            statisticsUpdated: new Date(0),
            statistics: {} as SystemStatistics,

            chartItemTypesFilter: {} as any,
            chartShowPrivateItems: true,

            chartOptions: {
                cutout: '33%',
                responsive: true,
                plugins: {
                    legend: false,
                    tooltip: {
                        callbacks: {
                            title: (items: any) => items[0].dataset.titles[items[0].dataIndex] ?? '',
                            label: (ctx: any) => ` ${ctx.dataset.labels[ctx.dataIndex]}: ${ctx.formattedValue}`,
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
            // Handle loading
            if (!this.statisticsLodaded) {
                return {
                    labels: ['Loading...'],
                    datasets: [{data: [1], backgroundColor: ['#CCCCCC']}]
                }
            }

            // Prepare data structure
            let datasets = {
                tplAvailability: {
                    labels: [] as string[],
                    titles: [] as string[],
                    data: [] as number[],
                    backgroundColor: [] as string[],
                    weight: 0.4,
                },
                tplTotals: {
                    labels: [] as string[],
                    titles: [] as string[],
                    data: [] as number[],
                    backgroundColor: [] as string[],
                    weight: 1,
                },
                itemTypes: {
                    labels: [] as string[],
                    titles: [] as string[],
                    data: [] as number[],
                    backgroundColor: [] as string[],
                    weight: 0.75,
                },
            }

            // Iterate over all item types, adding all their templates and stats
            for (const [itemTypeKey, templates] of Object.entries(this.statistics.templates)) {
                // Only process enabled item types
                if (this.chartItemTypesFilter[itemTypeKey].active == false) {
                    continue;
                }

                // Prepare data and category counters
                const itemType = ItemType.get(itemTypeKey);
                let itemTypeTotal = 0;
                let itemTypeBound = 0;
                let itemTypePrivate = 0;

                /**
                 * Adds the given template to the dataset structure
                 *
                 * @param tpl Template to append
                 */
                const _addTemplateToDataset = (tpl: any) => {
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
                        datasets.tplAvailability.backgroundColor.push('#4CAF50');

                        datasets.tplAvailability.titles.push(tpl.pretty_name);
                        datasets.tplAvailability.labels.push('Handed out');
                        datasets.tplAvailability.data.push(tpl.bound);
                        datasets.tplAvailability.backgroundColor.push('#F44336');

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

                // Process templates
                templates.filter((tpl: any) => !tpl.private).forEach((tpl: void) => _addTemplateToDataset(tpl))
                if (this.chartShowPrivateItems) {
                    templates.filter((tpl: any) => tpl.private).forEach((tpl: void) => _addTemplateToDataset(tpl))
                }

                // Add category stats
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
            this.statisticsLodaded = false;
            bindingsStore.fetchStatistics().then((response) => {
                this.statistics = response;
                this.statisticsUpdated = new Date();
                this.statisticsLodaded = true;
            });
        }
    },

    beforeMount() {
        ItemType.getAll()
            .filter(t => t != ItemType.Unknown)
            .forEach(t => this.chartItemTypesFilter[t.key] = {
                active: true,
                type: t,
            });
    },

    mounted() {
        this.refreshData();
    },
})
</script>