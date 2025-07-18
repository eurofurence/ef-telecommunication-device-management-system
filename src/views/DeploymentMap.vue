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
    <l-map
        ref="map"
        :key="componentKey"
        v-model:zoom="zoom"
        :center="[66, 50]"
        :use-global-leaflet="false"
        :options="options"
        @click="clickedCoordinates = $event.latlng"
    >
        <!-- Base map images -->
        <l-image-overlay
            v-if="floor == -1"
            :url="maplayerFloorN1"
            :bounds="[[0, 0], [100, 100]]"
        ></l-image-overlay>
        <l-image-overlay
            v-if="floor == 0"
            :url="maplayerFloor0"
            :bounds="[[0, 0], [100, 100]]"
        ></l-image-overlay>
        <l-image-overlay
            v-if="floor == 100"
            :url="maplayerFloor100"
            :bounds="[[0, 0], [100, 100]]"
        ></l-image-overlay>
        <l-image-overlay
            v-if="floor == 1"
            :url="maplayerFloor1"
            :bounds="[[0, 0], [100, 100]]"
        ></l-image-overlay>
        <l-image-overlay
            v-if="floor == 2"
            :url="maplayerFloor2"
            :bounds="[[0, 0], [100, 100]]"
        ></l-image-overlay>
        <l-image-overlay
            v-if="floor == 3"
            :url="maplayerFloor3"
            :bounds="[[0, 0], [100, 100]]"
        ></l-image-overlay>
        <l-image-overlay
            v-if="floor == 4"
            :url="maplayerFloor4"
            :bounds="[[0, 0], [100, 100]]"
        ></l-image-overlay>

        <!-- Coordinate display -->
        <l-control
            v-if="clickedCoordinates"
            position="bottomleft"
        >
            <v-tooltip text="Coordinates of last click" location="top">
                <template v-slot:activator="{ props, isActive }">
                    <div
                        v-bind="props"
                        class="cursor-pointer d-flex align-content-center ga-1"
                        @click="clickedCoordinates = null"
                    >
                        <v-icon icon="mdi-crosshairs-gps"></v-icon>
                        <span>Lat: {{ clickedCoordinatesRounded.lat }}, Lng: {{ clickedCoordinatesRounded.lng }}</span>
                        <v-icon
                            v-if="isActive"
                            icon="mdi-close"
                            size="small"
                        ></v-icon>
                    </div>
                </template>
            </v-tooltip>
        </l-control>

        <!-- Zoom control -->
        <!-- ATTENTION: Keep the l-control-zoom at precisely this location because if l-control order is changed, a
        black magic like race condition will occur that right away catapults the Vue main loop into a never-ending loop
        of death. This bug only occurs in production builds. Develop builds work just fine. And please, do not even
        think about asking me why this is happening. -->
        <l-control-zoom position="bottomright"></l-control-zoom>

        <!-- Refresh button -->
        <l-control
            position="topright"
            @click="updateItems(true)"
        >
            <v-tooltip v-if="!itemsLoading" text="Refresh">
                <template v-slot:activator="{ props }">
                    <v-btn
                        v-bind="props"
                        icon="mdi-refresh"
                        size="small"
                    ></v-btn>
                </template>
            </v-tooltip>
            <v-tooltip v-if="itemsLoading" text="Loading ...">
                <template v-slot:activator="{ props }">
                    <v-btn
                        v-bind="props"
                        icon=""
                        size="small"
                    >
                        <v-progress-circular
                            indeterminate
                            size="small"
                        ></v-progress-circular>
                    </v-btn>
                </template>
            </v-tooltip>
        </l-control>

        <!-- ItemType selector -->
        <l-control
            position="topright"
        >
            <v-chip-group
                v-model="selectedItemTypes"
                direction="vertical"
                multiple
            >
                <v-chip
                    v-for="itemType in ItemType.getAll()"
                    :key="itemType.key"
                    :value="itemType.key"
                    color="primary"
                    class="mr-0"
                >
                    <v-icon :icon="itemType.icon"></v-icon>
                    <v-tooltip activator="parent" :text="itemType.label"></v-tooltip>
                </v-chip>
            </v-chip-group>
        </l-control>

        <!-- Item markers -->
        <l-marker
            v-for="item in itemsFiltered"
            :key="item.item.id"
            :lat-lng="[item.latitude, item.longitude]"
            :ref="`itemMarker-${item.item.id}`"
            @click="clickedCoordinates = {lat: item.latitude, lng: item.longitude}"
        >
            <l-icon
                :icon-url="IconUtils.MapMarkerWithItemType(item.item.resourcetype, item.item.handed_out ? '#cd0505' : '#2db135')"
                :icon-size="mapMarkerDimensions.iconSize"
                :icon-anchor="mapMarkerDimensions.iconAnchor"
                :popup-anchor="mapMarkerDimensions.popupAnchor"
            ></l-icon>
            <l-popup>
                <p>
                    {{ item.item.pretty_name }}
                </p>
                <div class="text-center">
                    <v-btn
                        v-if="!item.item.handed_out"
                        :to="`/bindings/issue?itemid=${item.item.id}&skipbasket=true&returnpath=${returnPathEncoded}`"
                        color="success"
                        size="small"
                    >
                        Hand Out
                    </v-btn>
                    <v-btn
                        v-if="item.item.handed_out"
                        :to="`/bindings/return?itemid=${item.item.id}&skipbasket=true&returnpath=${returnPathEncoded}`"
                        color="error"
                        size="small"
                    >
                        Return
                    </v-btn>
                </div>
            </l-popup>
        </l-marker>
    </l-map>
</template>

<script lang="ts" setup>
import maplayerFloorN1 from '@/assets/deploymentmap/-1.svg';
import maplayerFloor0 from '@/assets/deploymentmap/0.svg';
import maplayerFloor1 from '@/assets/deploymentmap/1.svg';
import maplayerFloor2 from '@/assets/deploymentmap/2.svg';
import maplayerFloor3 from '@/assets/deploymentmap/3.svg';
import maplayerFloor4 from '@/assets/deploymentmap/4.svg';

// Special partial floor between floor 0 and floor 1 ("Zwischenebene")
import maplayerFloor100 from '@/assets/deploymentmap/100.svg';
</script>

<script lang="ts">
import {defineComponent} from "vue";
import "leaflet/dist/leaflet.css";
import { LMap, LImageOverlay, LMarker, LControl, LPopup, LIcon, LControlZoom } from "@vue-leaflet/vue-leaflet";
import {useItemsStore} from "@/store/items";
import {IconUtils} from "@/classes/util/IconUtils";
import {ItemType} from "@/types/ItemType";

const itemsStore = useItemsStore();

export default defineComponent({
    name: "DeploymentMap",

    components: {
        LMap,
        LImageOverlay,
        LMarker,
        LControl,
        LPopup,
        LIcon,
        LControlZoom,
    },

    props: {
        floor: {type: [Number, String], required: true},
        highlightItemId: {type: [Number, String], required: false},
    },

    data() {
        return {
            componentKey: 0,
            zoom: 4.0,
            options: {
                zoomControl: false,
                zoomDelta: 0.5,
                zoomSnap: 0.5,
            },
            clickedCoordinates: null as { lat: number, lng: number } | null,
            items: [],
            itemsLoading: true,
            selectedItemTypes: ItemType.getAll().map((itemType) => itemType.key),
        };
    },

    mounted() {
        this.updateItems().then(() => {
            setTimeout(() => {
                if (this.highlightItemId) {
                    const marker = this.$refs[`itemMarker-${this.highlightItemId}`];
                    if (marker) {
                        (marker as any)[0].leafletObject.openPopup();
                    }
                }
            }, 500);
        });
    },

    watch: {
        floor() {
            this.updateItems();
        },
    },

    computed: {
        itemsFiltered(): any[] {
            if (!this.items) {
                return [];
            }

            return this.items.filter((item: any) => {
                return this.selectedItemTypes.includes(item.item.resourcetype);
            });
        },

        clickedCoordinatesRounded() {
            return {
                // @ts-ignore
                lat: (Math.round(this.clickedCoordinates.lat * 100) / 100).toFixed(2),
                // @ts-ignore
                lng: (Math.round(this.clickedCoordinates.lng * 100) / 100).toFixed(2),
            };
        },

        mapMarkerDimensions() {
            if (this.zoom > 4.25) {
                return {
                    iconSize: [64, 64],
                    iconAnchor: [32, 64],
                    popupAnchor: [0, -48],
                };
            } else if (this.zoom > 3.25) {
                return {
                    iconSize: [48, 48],
                    iconAnchor: [24, 48],
                    popupAnchor: [0, -32],
                };
            } else {
                return {
                    iconSize: [32, 32],
                    iconAnchor: [16, 32],
                    popupAnchor: [0, -24],
                }
            }
        },

        returnPathEncoded() {
            return encodeURIComponent(this.$router.currentRoute.value.path);
        },
    },

    methods: {
        async updateItems(forceRerender: boolean = false) {
            this.items = [];
            this.itemsLoading = true;

            return itemsStore.fetchItemCoordinatesForFloor(this.floor as number).then((resp: any) => {
                this.items = resp.items;
                this.itemsLoading = false;

                if (forceRerender) {
                    this.componentKey++;
                }
            })
        },
    }
});
</script>

<style lang="scss">
.leaflet-marker-icon {
    -webkit-filter: drop-shadow( 2px 2px 3px rgba(0, 0, 0, .3));
    filter: drop-shadow( 2px 2px 3px rgba(0, 0, 0, .3));
}

.leaflet-control-container {
    .leaflet-top.leaflet-right {
        display: flex;
        flex-direction: column;
        align-items: center;
    }
}
</style>