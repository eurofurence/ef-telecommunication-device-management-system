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
    <v-navigation-drawer
        permanent
        location="left"
    >
        <v-list density="compact" nav open-strategy="multiple" slim>
            <v-list-item prepend-icon="mdi-home-city" title="Overview" value="overview" to="/overview"></v-list-item>
            <v-list-item prepend-icon="mdi-account" title="My Account" value="account" to="/profile"></v-list-item>
            <v-list-item prepend-icon="mdi-chart-box-outline" title="Inventory" value="inventory" to="/inventory"></v-list-item>
            <v-list-group value="Deployment Map">
                <template v-slot:activator="{ props }">
                    <v-list-item v-bind="props" prepend-icon="mdi-map" title="Deployment Map"></v-list-item>
                </template>
                <v-list-item prepend-icon="mdi-numeric-0" title="Ground Floor" value="deployment-map-0" to="/deployment-map/0"></v-list-item>
                <v-list-item prepend-icon="mdi-numeric-1" title="First Floor" value="deployment-map-1" to="/deployment-map/1"></v-list-item>
                <v-list-item prepend-icon="mdi-numeric-2" title="Second Floor" value="deployment-map-2" to="/deployment-map/2"></v-list-item>
                <v-list-item prepend-icon="mdi-numeric-3" title="Third Floor" value="deployment-map-3" to="/deployment-map/3"></v-list-item>
                <v-list-item prepend-icon="mdi-numeric-4" title="Fourth Floor" value="deployment-map-4" to="/deployment-map/4"></v-list-item>
            </v-list-group>
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
