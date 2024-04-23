<template>
    <v-navigation-drawer
        permanent
        location="left"
    >
        <v-list density="compact" nav open-strategy="multiple" slim>
            <v-list-item prepend-icon="mdi-home-city" title="Overview" value="overview" to="/overview"></v-list-item>
            <v-list-item prepend-icon="mdi-account" title="My Account" value="account" to="/profile"></v-list-item>
            <v-list-item prepend-icon="mdi-map" title="Deployment Map" value="deployment-map" to="/deployment-map"></v-list-item>
            <v-list-group value="Bindings">
                <template v-slot:activator="{ props }">
                    <v-list-item v-bind="props" prepend-icon="mdi-basket-fill" title="Bindings"></v-list-item>
                </template>
                <v-list-item prepend-icon="mdi-basket-outline" title="Overview" value="bindings-overview" to="/bindings/overview"></v-list-item>
                <v-list-item prepend-icon="mdi-basket-fill" title="Pre-Orders" value="bindings-preorders" to="/bindings/preorders"></v-list-item>
                <v-list-item prepend-icon="mdi-basket-plus-outline" title="Hand out" value="bindings-issue" to="/bindings/issue"></v-list-item>
                <v-list-item prepend-icon="mdi-basket-minus-outline" title="Return" value="bindings-return" to="/bindings/return"></v-list-item>
            </v-list-group>
            <v-list-group value="People">
                <template v-slot:activator="{ props }">
                    <v-list-item v-bind="props" prepend-icon="mdi-account-circle" title="People"></v-list-item>
                </template>
                <v-list-item prepend-icon="mdi-account-group-outline" title="Users" value="users" to="/users"></v-list-item>
                <v-list-item prepend-icon="mdi-account-arrow-right" title="Item Owners" value="itemowners" to="/itemowners"></v-list-item>
            </v-list-group>
            <v-list-group value="Radios">
                <template v-slot:activator="{ props }">
                    <v-list-item v-bind="props" prepend-icon="mdi-radio-tower" title="Radios"></v-list-item>
                </template>
                <v-list-item prepend-icon="mdi-cellphone-basic" title="Devices" value="radio-radios" to="/radio/devices"></v-list-item>
                <v-list-item prepend-icon="mdi-headset" title="Accessories" value="radio-accessories" to="/radio/accessories"></v-list-item>
                <v-list-item prepend-icon="mdi-bell-ring-outline" title="Pagers" value="radio-pagers" to="/radio/pagers"></v-list-item>
                <v-list-item prepend-icon="mdi-sim" title="Codings" value="radio-codings" to="/radio/codings"></v-list-item>
            </v-list-group>
            <v-list-group value="VoIP">
                <template v-slot:activator="{ props }">
                    <v-list-item v-bind="props" prepend-icon="mdi-phone-voip" title="VoIP"></v-list-item>
                </template>
                <v-list-item prepend-icon="mdi-phone" title="Phones" value="voip-phones" to="/voip/phones"></v-list-item>
                <v-list-item prepend-icon="mdi-webcam" title="Callboxes" value="voip-callboxes" to="/voip/callboxes"></v-list-item>
            </v-list-group>
            <v-list-item prepend-icon="mdi-clipboard-text-search-outline" title="Event Log" value="eventlog" to="/eventlog"></v-list-item>
        </v-list>

        <template v-slot:append>
            <p class="text-center text-caption font-weight-light">
                EF-TDMS&nbsp;v{{ app_version }}
            </p>
        </template>
    </v-navigation-drawer>
</template>

<script lang="ts" setup>
const app_version = import.meta.env.APP_VERSION;
</script>
