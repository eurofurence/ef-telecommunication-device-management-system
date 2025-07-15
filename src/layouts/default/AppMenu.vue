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
    <v-navigation-drawer
        permanent
        :rail="collapsed"
        :rail-width="railWidth"
        location="left"
        class="mainnav"
    >
        <v-list density="compact" nav open-strategy="multiple" slim>
            <v-list-item prepend-icon="mdi-home-city" title="Overview" value="overview" to="/overview">
                <v-tooltip text="Overview" activator="parent" location="right" :disabled="!collapsed"></v-tooltip>
            </v-list-item>
            <v-list-item prepend-icon="mdi-account" title="My Account" value="account" to="/profile">
                <v-tooltip text="My Account" activator="parent" location="right" :disabled="!collapsed"></v-tooltip>
            </v-list-item>
            <v-list-item prepend-icon="mdi-chart-box-outline" title="Inventory" value="inventory" to="/inventory">
                <v-tooltip text="Inventory" activator="parent" location="right" :disabled="!collapsed"></v-tooltip>
            </v-list-item>
            <v-list-group value="Deployment Map">
                <template v-slot:activator="{ props }">
                    <v-list-item v-bind="props" prepend-icon="mdi-map" title="Deployment Map">
                        <v-tooltip text="Deployment Map" activator="parent" location="right" :disabled="!collapsed"></v-tooltip>
                    </v-list-item>
                </template>
                <v-divider v-if="collapsed" class="mb-1"></v-divider>
                <v-list-item
                    v-for="floor in Floor.getAll()"
                    :title="floor.title"
                    :value="`deployment-map-${floor.value}`"
                    :to="`/deployment-map/${floor.value}`"
                    :class="listChildCssClasses"
                >
                    <template v-slot:prepend>
                        <v-icon
                            :icon="floor.icon"
                            :size="floor.value != 100 ? 'default' : 'x-small'"
                            :class="floor.value != 100 ? '' : 'mx-1'"
                        ></v-icon>
                    </template>
                    <v-tooltip :text="floor.title" activator="parent" location="right" :disabled="!collapsed"></v-tooltip>
                </v-list-item>
                <v-divider v-if="collapsed"></v-divider>
            </v-list-group>
            <v-list-group value="Bindings">
                <template v-slot:activator="{ props }">
                    <v-list-item v-bind="props" prepend-icon="mdi-basket-fill" title="Bindings">
                        <v-tooltip text="Bindings" activator="parent" location="right" :disabled="!collapsed"></v-tooltip>
                    </v-list-item>
                </template>
                <v-divider v-if="collapsed" class="mb-1"></v-divider>
                <v-list-item prepend-icon="mdi-basket-outline" title="Overview" value="bindings-overview" to="/bindings/overview" :class="listChildCssClasses">
                    <v-tooltip text="Bindings Overview" activator="parent" location="right" :disabled="!collapsed"></v-tooltip>
                </v-list-item>
                <v-list-item prepend-icon="mdi-basket-fill" title="Pre-Orders" value="bindings-preorders" to="/bindings/preorders" :class="listChildCssClasses">
                    <v-tooltip text="Pre-Orders" activator="parent" location="right" :disabled="!collapsed"></v-tooltip>
                </v-list-item>
                <v-list-item prepend-icon="mdi-basket-plus-outline" title="Hand out" value="bindings-issue" to="/bindings/issue" :class="listChildCssClasses">
                    <v-tooltip text="Hand out" activator="parent" location="right" :disabled="!collapsed"></v-tooltip>
                </v-list-item>
                <v-list-item prepend-icon="mdi-basket-minus-outline" title="Return" value="bindings-return" to="/bindings/return" :class="listChildCssClasses">
                    <v-tooltip text="Return" activator="parent" location="right" :disabled="!collapsed"></v-tooltip>
                </v-list-item>
                <v-divider v-if="collapsed"></v-divider>
            </v-list-group>
            <v-list-group value="People">
                <template v-slot:activator="{ props }">
                    <v-list-item v-bind="props" prepend-icon="mdi-account-circle" title="People">
                        <v-tooltip text="People" activator="parent" location="right" :disabled="!collapsed"></v-tooltip>
                    </v-list-item>
                </template>
                <v-divider v-if="collapsed" class="mb-1"></v-divider>
                <v-list-item prepend-icon="mdi-account-group-outline" title="Users" value="users" to="/users" :class="listChildCssClasses">
                    <v-tooltip text="Users" activator="parent" location="right" :disabled="!collapsed"></v-tooltip>
                </v-list-item>
                <v-list-item prepend-icon="mdi-account-arrow-right" title="Item Owners" value="itemowners" to="/itemowners" :class="listChildCssClasses">
                    <v-tooltip text="Item Owners" activator="parent" location="right" :disabled="!collapsed"></v-tooltip>
                </v-list-item>
                <v-divider v-if="collapsed"></v-divider>
            </v-list-group>
            <v-list-group value="Radios">
                <template v-slot:activator="{ props }">
                    <v-list-item v-bind="props" prepend-icon="mdi-radio-tower" title="Radios">
                        <v-tooltip text="Radios" activator="parent" location="right" :disabled="!collapsed"></v-tooltip>
                    </v-list-item>
                </template>
                <v-divider v-if="collapsed" class="mb-1"></v-divider>
                <v-list-item prepend-icon="mdi-cellphone-basic" title="Devices" value="radio-radios" to="/radio/devices" :class="listChildCssClasses">
                    <v-tooltip text="Radio Devices" activator="parent" location="right" :disabled="!collapsed"></v-tooltip>
                </v-list-item>
                <v-list-item prepend-icon="mdi-headset" title="Accessories" value="radio-accessories" to="/radio/accessories" :class="listChildCssClasses">
                    <v-tooltip text="Radio Accessories" activator="parent" location="right" :disabled="!collapsed"></v-tooltip>
                </v-list-item>
                <v-list-item prepend-icon="mdi-bell-ring-outline" title="Pagers" value="radio-pagers" to="/radio/pagers" :class="listChildCssClasses">
                    <v-tooltip text="Pagers" activator="parent" location="right" :disabled="!collapsed"></v-tooltip>
                </v-list-item>
                <v-list-item prepend-icon="mdi-sim" title="Codings" value="radio-codings" to="/radio/codings" :class="listChildCssClasses">
                    <v-tooltip text="Radio Codings" activator="parent" location="right" :disabled="!collapsed"></v-tooltip>
                </v-list-item>
                <v-divider v-if="collapsed"></v-divider>
            </v-list-group>
            <v-list-group value="VoIP">
                <template v-slot:activator="{ props }">
                    <v-list-item v-bind="props" prepend-icon="mdi-phone-voip" title="VoIP">
                        <v-tooltip text="VoIP" activator="parent" location="right" :disabled="!collapsed"></v-tooltip>
                    </v-list-item>
                </template>
                <v-divider v-if="collapsed" class="mb-1"></v-divider>
                <v-list-item prepend-icon="mdi-phone" title="Phones" value="voip-phones" to="/voip/phones" :class="listChildCssClasses">
                    <v-tooltip text="Phones" activator="parent" location="right" :disabled="!collapsed"></v-tooltip>
                </v-list-item>
                <v-list-item prepend-icon="mdi-webcam" title="Callboxes" value="voip-callboxes" to="/voip/callboxes" :class="listChildCssClasses">
                    <v-tooltip text="Callboxes" activator="parent" location="right" :disabled="!collapsed"></v-tooltip>
                </v-list-item>
                <v-list-item prepend-icon="mdi-database-cog-outline" title="Provisioning" value="voip-provisioning" to="/voip/provisioning" :class="listChildCssClasses">
                    <v-tooltip text="Provisioning" activator="parent" location="right" :disabled="!collapsed"></v-tooltip>
                </v-list-item>
                <v-divider v-if="collapsed"></v-divider>
            </v-list-group>
            <v-list-item prepend-icon="mdi-clipboard-text-search-outline" title="Event Log" value="eventlog" to="/eventlog">
                <v-tooltip text="Event Log" activator="parent" location="right" :disabled="!collapsed"></v-tooltip>
            </v-list-item>
        </v-list>

        <template v-slot:append>
            <div class="d-flex align-content-end">
                <v-sheet v-if="!collapsed" class="flex-grow-0" :width="railWidth"></v-sheet>
                <v-sheet v-if="!collapsed" class="flex-grow-1 align-content-center">
                    <p class="text-center text-caption font-weight-light">
                        EF-TDMS&nbsp;v{{ appVersion }}
                    </p>
                </v-sheet>
                <v-sheet class="flex-grow-0 text-center" :width="railWidth">
                    <v-btn
                        variant="plain"
                        @click="collapsed = !collapsed"
                        :min-width="railWidth"
                        :max-width="railWidth"
                        slim
                    >
                        <v-icon :icon="collapsed ? 'mdi-arrow-expand-right' : 'mdi-arrow-collapse-left'"></v-icon>
                        <v-tooltip
                            activator="parent"
                            location="top"
                            :text="collapsed ? 'Expand' : 'Collapse'"
                        ></v-tooltip>
                    </v-btn>
                </v-sheet>
            </div>
        </template>
    </v-navigation-drawer>
</template>

<style lang="scss">
.mainnav.v-navigation-drawer--rail .v-list-item {
    padding-inline-start: 8px !important;
}
</style>

<script lang="ts" setup>
import {Floor} from "@/types/Floor.ts";

const appVersion = import.meta.env.APP_VERSION;
const railWidth = 56;
</script>

<script lang="ts">
import {defineComponent} from "vue";

export default defineComponent({
    name: 'AppMenu',

    mounted() {
        this.collapsed = this.$vuetify.display.mdAndDown;
    },

    data: () => ({
        collapsed: false,
    }),

    computed: {
        listChildCssClasses() {
            return this.collapsed ? 'border-s-lg rounded-s-0' : '';
        },
    }
})
</script>
