<template>
    <v-card flat>
        <v-card-title>Basket</v-card-title>
        <v-card-text>
            <v-list>
                <v-list-item v-for="entry in basketItems.values()">
                    <template v-slot:prepend>
                        <v-icon>{{ entry.type.icon }}</v-icon>
                    </template>

                    <v-list-item-title>{{ entry.item.pretty_name }}</v-list-item-title>

                    <template v-slot:append v-if="!readOnly">
                        <v-btn icon="mdi-delete" @click="removeItem(entry.item.id)" variant="flat"></v-btn>
                    </template>
                </v-list-item>
                <v-divider v-if="basketItems.size > 0 && basketItemTemplates.length > 0"></v-divider>
                <v-list-item v-for="(entry, idx) in basketItemTemplates">
                    <template v-slot:prepend>
                        <v-icon>{{ entry.type.itemType.icon }}</v-icon>
                    </template>

                    <v-list-item-title>{{ entry.template.pretty_name }}</v-list-item-title>

                    <template v-slot:append v-if="!readOnly">
                        <v-btn icon="mdi-delete" @click="removeItemTemplate(idx)"
                               variant="flat"></v-btn>
                    </template>
                </v-list-item>
            </v-list>
        </v-card-text>
    </v-card>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import {ItemTemplateType, ItemType} from "@/types/ItemType";

export const emptyItemsBasket = () => new Map<number, { type: ItemType, item: any }>();
export const emptyItemTemplatesBasket = () => []<{ type: ItemTemplateType, template: any }>;

export default defineComponent({
    name: "ItemBasket",

    props: {
        basketItems: {type: Map, required: true},
        basketItemTemplates: {type: Array, required: true},
        readOnly: {type: Boolean, required: false, default: false},
    },

    methods: {
        addItem(item: any, type: ItemType) {
            if (this.readOnly) {
                return;
            }

            this.basketItems.set(item.id, {
                type: type,
                item: item
            });
            this.$emit('update:basket');
        },

        addItemTemplate(template: any, type: ItemTemplateType) {
            if (this.readOnly) {
                return;
            }

            this.basketItemTemplates.push({
                type: type,
                template: template
            });
            this.$emit('update:basket');
        },

        removeItem(itemId: number) {
            if (this.readOnly) {
                return;
            }

            this.basketItems.delete(itemId);
            this.$emit('update:basket');
        },

        removeItemTemplate(idx: number) {
            if (this.readOnly) {
                return;
            }

            this.basketItemTemplates.splice(idx, 1);
            this.$emit('update:basket');
        },

        clear() {
            if (this.readOnly) {
                return;
            }

            this.basketItems.clear();
            this.basketItemTemplates = [];
            this.$emit('update:basket')
        },

        getItems() {
            return Array.from(this.basketItems.values());
        },

        getItemIds() {
            return Array.from(this.basketItems.keys());
        },

        getItemTemplates() {
            return Array.from(this.basketItemTemplates);
        },

        size() {
            return this.basketItems.size + this.basketItemTemplates.length;
        },

        isEmpty() {
            return this.size() === 0;
        },
    }

})
</script>