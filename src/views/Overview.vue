<template>
    <v-container>
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

                            <div class="d-flex mt-4 justify-space-between">
                                <v-list-item
                                    density="compact"
                                    prepend-icon="mdi-basket-outline"
                                >
                                    <v-list-item-subtitle>
                                        {{ statistics.items.total }} ({{ statistics.templates.total }})
                                    </v-list-item-subtitle>
                                    <v-tooltip activator="parent" location="top">
                                        <span>Total items</span>
                                    </v-tooltip>
                                </v-list-item>

                                <v-list-item
                                    density="compact"
                                    prepend-icon="mdi-basket-plus-outline"
                                    class="text-red-accent-4"
                                >
                                    <v-list-item-subtitle>
                                        {{ statistics.items.bound }}
                                    </v-list-item-subtitle>
                                    <v-tooltip activator="parent" location="top">
                                        <span>Bound items</span>
                                    </v-tooltip>
                                </v-list-item>

                                <v-list-item
                                    density="compact"
                                    prepend-icon="mdi-basket-minus-outline"
                                    class="text-green-darken-3"
                                >
                                    <v-list-item-subtitle>
                                        {{ statistics.items.unbound }}
                                    </v-list-item-subtitle>
                                    <v-tooltip activator="parent" location="top">
                                        <span>Unbound items</span>
                                    </v-tooltip>
                                </v-list-item>
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

                            <div class="d-flex mt-4 justify-space-between">
                                <v-list-item
                                    density="compact"
                                    prepend-icon="mdi-account-group"
                                >
                                    <v-list-item-subtitle>
                                        {{ statistics.users.total }}
                                    </v-list-item-subtitle>
                                    <v-tooltip activator="parent" location="top">
                                        <span>Total users</span>
                                    </v-tooltip>
                                </v-list-item>

                                <v-list-item
                                    density="compact"
                                    prepend-icon="mdi-account-arrow-right-outline"
                                    class="text-red-accent-4"
                                >
                                    <v-list-item-subtitle>
                                        {{ statistics.users.with_bindings }}
                                    </v-list-item-subtitle>
                                    <v-tooltip activator="parent" location="top">
                                        <span>Users with bindings</span>
                                    </v-tooltip>
                                </v-list-item>


                                <v-list-item
                                    density="compact"
                                    prepend-icon="mdi-account-arrow-left-outline"
                                    class="text-green-darken-3"
                                >
                                    <v-list-item-subtitle>
                                        {{ statistics.users.without_bindings }}
                                    </v-list-item-subtitle>
                                    <v-tooltip activator="parent" location="top">
                                        <span>Users without bindings</span>
                                    </v-tooltip>
                                </v-list-item>
                            </div>
                        </v-card-text>
                    </v-card>
                </div>
            </v-col>
        </v-row>
        <v-row>
            <v-col>
                <h2>Latest Events</h2>
            </v-col>
        </v-row>
        <v-row>
            <v-col>
                <EventTimeline/>
            </v-col>
        </v-row>
    </v-container>
</template>

<script lang="ts">
import {defineComponent} from "vue";

import {useBindingsStore} from "@/store/bindings";
import {SystemStatistics} from "@/types/SystemStatistics";
import EventTimeline from "@/components/EventTimeline.vue";

const bindingsStore = useBindingsStore();

export default defineComponent({
    components: {EventTimeline},
    data() {
        return {
            statisticsLodaded: false,
            statistics: Object as SystemStatistics,
        }
    },

    computed: {
        itemsBoundPercentage() {
            return this.statistics.items.bound / this.statistics.items.total * 100;
        },
        usersWithBindingsPercentage() {
            return this.statistics.users.with_bindings / this.statistics.users.total * 100;
        }
    },

    mounted() {
        bindingsStore.fetchStatistics().then((response) => {
            this.statistics = response;
            this.statisticsLodaded = true;
        })
    },
})
</script>