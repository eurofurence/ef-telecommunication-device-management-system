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
                                :icon="ItemType[order.type] ? ItemType[order.type].icon : 'mdi-shape-outline'"
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
        orders: {type: Array, required: true},
    },
})
</script>