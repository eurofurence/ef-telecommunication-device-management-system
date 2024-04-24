<template>
    <h1>Floor {{ floor }}</h1>
    <l-map
        ref="map"
        v-model:zoom="zoom"
        :center="[65, 802]"
        :use-global-leaflet="false"
        :options="options"
        @click="clickedCoordinates = $event.latlng"
    >
        <l-image-overlay
            :url="`/src/assets/deploymentmap/${floor}.svg`"
            :bounds="bonds"
        ></l-image-overlay>

        <l-control
            position="bottomleft"
        >Lat: {{ clickedCoordinatesRounded.lat }}, Lng:{{ clickedCoordinatesRounded.lng }}</l-control>
    </l-map>
</template>

<script lang="ts">
import "leaflet/dist/leaflet.css";
import { LMap, LTileLayer, LImageOverlay, LControlLayers, LMarker, LControl } from "@vue-leaflet/vue-leaflet";

export default {
    name: "DeploymentMap",

    components: {
        LImageOverlay,
        LMap,
        LTileLayer,
        LControlLayers,
        LMarker,
        LControl
    },

    props: {
        floor: {type: Number, required: true,},
    },

    data() {
        return {
            zoom: 3.0,
            options: {
                zoomDelta: 0.5,
                zoomSnap: 0.5,
            },
            clickedCoordinates: {lat: 0, lng: 0},
        };
    },

    computed: {
        bonds() {
            return [[0, 0], [1281, 1605]];
        },

        clickedCoordinatesRounded() {
            return {
                lat: Math.round(this.clickedCoordinates.lat * 100) / 100,
                lng: Math.round(this.clickedCoordinates.lng * 100) / 100,
            };
        },
    },
};
</script>