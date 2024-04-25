<template>
    <l-map
        ref="map"
        v-model:zoom="zoom"
        :center="[66, 50]"
        :use-global-leaflet="false"
        :options="options"
        @click="clickedCoordinates = $event.latlng"
    >
        <l-image-overlay
            :url="`/src/assets/deploymentmap/${floor}.svg`"
            :bounds="[[0, 0], [100, 100]]"
        ></l-image-overlay>

        <l-control
            v-if="clickedCoordinates"
            position="bottomleft"
        >
            Lat: {{ clickedCoordinatesRounded.lat }}, Lng:{{ clickedCoordinatesRounded.lng }}
        </l-control>

        <l-marker
            v-for="item in items"
            :key="item.item.id"
            :lat-lng="[item.latitude, item.longitude]"
        >
            <l-icon
                :icon-url="IconUtils.MapMarkerWithItemType(item.item.resourcetype, item.item.handed_out ? '#cd0505' : '#2db135')"
                :icon-size="mapMarkerDimensions.iconSize"
                :icon-anchor="mapMarkerDimensions.iconAnchor"
                :popup-anchor="mapMarkerDimensions.popupAnchor"
            ></l-icon>
            <l-popup>{{ item.item.pretty_name }}</l-popup>
        </l-marker>
    </l-map>
</template>

<script lang="ts">
import "leaflet/dist/leaflet.css";
import { LMap, LTileLayer, LImageOverlay, LControlLayers, LMarker, LControl, LPopup, LIcon } from "@vue-leaflet/vue-leaflet";
import {useItemsStore} from "@/store/items";
import {IconUtils} from "@/classes/util/IconUtils";

const itemsStore = useItemsStore();

export default {
    name: "DeploymentMap",

    components: {
        LImageOverlay,
        LMap,
        LTileLayer,
        LControlLayers,
        LMarker,
        LControl,
        LPopup,
        LIcon
    },

    props: {
        floor: {type: Number, required: true,},
    },

    data() {
        return {
            zoom: 4.0,
            options: {
                zoomDelta: 0.5,
                zoomSnap: 0.5,
            },
            clickedCoordinates: null,
            items: [],
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
        IconUtils() {
            return IconUtils
        },

        clickedCoordinatesRounded() {
            return {
                lat: Math.round(this.clickedCoordinates.lat * 100) / 100,
                lng: Math.round(this.clickedCoordinates.lng * 100) / 100,
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
        }
    },

    methods: {
        async updateItems() {
            itemsStore.fetchItemCoordinatesForFloor(this.floor).then((resp) => {
                this.items = resp.items;
            })
        },
    }
};
</script>

<style lang="scss">
.leaflet-marker-icon {
    -webkit-filter: drop-shadow( 2px 2px 3px rgba(0, 0, 0, .3));
    filter: drop-shadow( 2px 2px 3px rgba(0, 0, 0, .3));
}
</style>