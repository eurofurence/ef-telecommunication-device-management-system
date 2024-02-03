<template>
    <l-map
        ref="map"
        v-model:zoom="zoom"
        :center="[65, 802]"
        :use-global-leaflet="false"
        :options="options"
    >
        <l-image-overlay
            url="/src/assets/deployment-map.svg"
            :bounds="bonds"
        ></l-image-overlay>
    </l-map>
</template>

<script lang="ts">
import "leaflet/dist/leaflet.css";
import { LMap, LTileLayer, LImageOverlay } from "@vue-leaflet/vue-leaflet";

export default {
    components: {
        LImageOverlay,
        LMap,
        LTileLayer,
    },

    data() {
        return {
            zoom: 3.0,
            options: {
                zoomDelta: 0.5,
                zoomSnap: 0.5,
            },
        };
    },

    computed: {
        bonds() {
            return [[0, 0], [1281, 1605]];
        },
    },
};
</script>