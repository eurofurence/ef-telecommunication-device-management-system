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
        <!-- Base map image -->
        <l-image-overlay
            :url="`/src/assets/deploymentmap/${floor}.svg`"
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
                        <span>Lat: {{ clickedCoordinatesRounded.lat }}, Lng:{{ clickedCoordinatesRounded.lng }}</span>
                        <v-icon
                            v-if="isActive"
                            icon="mdi-close"
                            size="small"
                        ></v-icon>
                    </div>
                </template>
            </v-tooltip>
        </l-control>

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

        <!-- Zoom control -->
        <l-control-zoom position="topright"></l-control-zoom>

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
            clickedCoordinates: null,
            items: [],
            itemsLoading: true,
            selectedItemTypes: ItemType.getAll().map((itemType) => itemType.key),
        };
    },

    mounted() {
        this.updateItems();
    },

    watch: {
        floor() {
            this.updateItems();
        },
    },

    computed: {
        ItemType() {
            return ItemType
        },

        IconUtils() {
            return IconUtils
        },

        itemsFiltered() {
            return this.items.filter((item) => {
                return this.selectedItemTypes.includes(item.item.resourcetype);
            });
        },

        clickedCoordinatesRounded() {
            return {
                lat: (Math.round(this.clickedCoordinates.lat * 100) / 100).toFixed(2),
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
            this.itemsLoading = true;
            itemsStore.fetchItemCoordinatesForFloor(this.floor).then((resp) => {
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