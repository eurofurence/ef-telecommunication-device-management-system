<template>
    <v-card flat>
        <v-card-title :v-if="title">{{ title }}</v-card-title>
        <v-card-text>
            <v-list>
                <v-list-subheader v-if="isEmpty()">
                    No items added yet
                </v-list-subheader>
                <v-hover v-for="entry in basketItems.values()">
                    <template v-slot:default="{ isHovering, props }">
                        <v-list-item
                            v-bind="props"
                            @click="removeItem(entry.item.id)"
                        >
                            <template v-slot:prepend>
                                <v-icon>{{ entry.type.icon }}</v-icon>
                            </template>

                            <v-list-item-title>
                                {{ entry.item.pretty_name }}
                            </v-list-item-title>

                            <template v-slot:append v-if="!readOnly">
                                <v-btn
                                    icon="mdi-delete"
                                    @click="removeItem(entry.item.id)"
                                    variant="flat"
                                    color="transparent"
                                >
                                    <template v-slot:default>
                                        <v-icon :color="isHovering ? 'red' : undefined"></v-icon>
                                    </template>
                                </v-btn>
                            </template>
                        </v-list-item>
                    </template>
                </v-hover>

                <v-divider v-if="basketItems.size > 0 && basketItemTemplates.length > 0"></v-divider>
                <v-hover v-for="(entry, idx) in basketItemTemplates">
                    <template v-slot:default="{ isHovering, props }">
                        <v-list-item
                            v-bind="props"
                            @click="removeItemTemplate(idx)"
                        >
                            <template v-slot:prepend>
                                <v-icon>{{ entry.type.itemType.icon }}</v-icon>
                            </template>

                            <v-list-item-title>
                                {{ entry.template.pretty_name }}
                            </v-list-item-title>

                            <template v-slot:append v-if="!readOnly">
                                <v-btn
                                    icon="mdi-delete"
                                    @click="removeItemTemplate(idx)"
                                    variant="flat"
                                    color="transparent"
                                >
                                    <template v-slot:default>
                                        <v-icon :color="isHovering ? 'red' : undefined"></v-icon>
                                    </template>
                                </v-btn>
                            </template>
                        </v-list-item>
                    </template>
                </v-hover>
            </v-list>
        </v-card-text>
    </v-card>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import {ItemTemplateTypeMetadata, ItemTypeMetadata} from "@/types/ItemType";

export const emptyItemsBasket = () => new Map<number, { type: ItemTypeMetadata, item: any }>();
export const emptyItemTemplatesBasket = () => new Array<{ type: ItemTemplateTypeMetadata, template: any }>;

export default defineComponent({
    name: "ItemBasket",

    props: {
        title: {type: String, required: false, default: "Basket"},
        basketItems: {type: Map<number, {type: ItemTypeMetadata, item: any}>, required: false, default: emptyItemsBasket},
        basketItemTemplates: {type: Array<{type: ItemTemplateTypeMetadata, template: any}>, required: false, default: emptyItemTemplatesBasket},
        readOnly: {type: Boolean, required: false, default: false},
    },

    emits: [
        'update:basket'
    ],

    methods: {
        addItem(item: any, type: ItemTypeMetadata) {
            if (this.readOnly) {
                return;
            }

            this.basketItems.set(item.id, {
                type: type,
                item: item
            });
            this.$emit('update:basket');
        },

        addItemTemplate(template: any, type: ItemTemplateTypeMetadata) {
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
            this.basketItemTemplates.length = 0;
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