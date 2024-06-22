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
    <v-card rounded elevation="2">
        <v-card-title>
            Orders
        </v-card-title>
        <v-divider></v-divider>
        <v-card-text>
            <v-list select-strategy="independent" class="py-0">
                <v-list-subheader v-if="orders.length === 0">
                    No orders found
                </v-list-subheader>

                <v-list-item v-for="order in orders" :key="order.id" :value="order.id" color="grey-lighten-2">
                    <template v-slot:prepend="{ isActive }">
                        <v-list-item-action start>
                            <v-icon
                                :icon="ItemType.get(order.type) ? ItemType.get(order.type).icon : 'mdi-shape-outline'"
                                :color="isActive ? 'grey' : 'black'"
                            ></v-icon>
                        </v-list-item-action>
                    </template>

                    <template v-slot:default="{ isActive }">
                        <v-list-item-title :class="{ 'text-decoration-line-through text-grey': isActive }">
                            {{ order.title }}
                        </v-list-item-title>
                    </template>
                </v-list-item>
            </v-list>
        </v-card-text>
    </v-card>
</template>

<script lang="ts" setup>
import {ItemType} from "@/types/ItemType";
</script>

<script lang="ts">
import { defineComponent } from "vue";

export default defineComponent({
    name: "ItemBasket",

    props: {
        orders: {type: Array<any>, required: true},
    },
})
</script>