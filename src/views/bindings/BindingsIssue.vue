<template>
    <v-container>
        <v-row>
            <v-col>
                <h1>Create Binding</h1>
            </v-col>
        </v-row>
        <v-row>
            <v-col>
                <v-stepper
                    v-model="currentStep"
                    :items="['User', 'Items', 'Create Binding', 'Confirmation']"
                    :disabled="!stepperCanAdvance"
                    alt-labels
                >
                    <template v-slot:item.1>
                        <v-card title="Select User" flat>
                            <ServerItemSelector
                                :fetch-function="usersStore.fetchUsersPage"
                                label="User"
                                icon="mdi-account"
                                item-title-key="pretty_name"
                                item-value-key="id"
                                :autofocus="true"
                                @update:selection="onUserSelected"
                            ></ServerItemSelector>
                        </v-card>
                    </template>

                    <template v-slot:item.2>
                        <v-card title="Select Items" flat>
                            <v-btn-toggle
                                v-model="itemSearchType"
                                variant="outlined"
                                color="primary"
                                divided
                                @update:model-value="$refs.itemSelector.clear(); onItemSelect(null);"
                            >
                                <v-btn v-for="type in [ItemType.RadioDevice, ItemType.Pager, ItemType.Phone, ItemType.Callbox]" :value="type">
                                    <v-icon start>{{ type.icon }}</v-icon>
                                    <span class="hidden-sm-and-down">{{ type.label }}</span>
                                </v-btn>
                            </v-btn-toggle>
                            <ServerItemSelector
                                ref="itemSelector"
                                :fetch-function="itemSearchFetchFunction"
                                :label="itemSearchType.label"
                                :icon="itemSearchType.icon"
                                item-title-key="pretty_name"
                                item-value-key="id"
                                :item-ids-to-exclude="Array.from(itemsToBind.keys())"
                                :autofocus="true"
                                @update:selection="onItemSelect"
                            ></ServerItemSelector>

                            <v-list>
                                <v-list-item v-for="entry in itemsToBind.values()">
                                    <template v-slot:prepend>
                                        <v-icon>{{ entry.type.icon }}</v-icon>
                                    </template>

                                    <v-list-item-title>{{ entry.item.pretty_name }}</v-list-item-title>

                                    <template v-slot:append>
                                        <v-btn icon="mdi-delete" @click="removeItemFromBasket(entry.item.id)" variant="flat"></v-btn>
                                    </template>
                                </v-list-item>
                            </v-list>
                        </v-card>
                    </template>

                    <template v-slot:item.3>
                        <v-card title="Create Binding" flat>...</v-card>
                    </template>

                    <template v-slot:item.4>
                        <v-card title="Confirmation" flat>...</v-card>
                    </template>
                </v-stepper>

            </v-col>
        </v-row>
    </v-container>
</template>

<script setup lang="ts">
import ServerItemSelector from "@/components/ServerItemSelector.vue";
</script>

<script lang="ts">
import { defineComponent } from "vue";
import {useUsersStore} from "@/store/users";
import {useItemsStore} from "@/store/items";
import {ItemType} from "@/types/ItemType";

const usersStore = useUsersStore();
const itemsStore = useItemsStore();

export default defineComponent({

    data() {
        return {
            selectedUser: null,
            itemSearchType: ItemType.RadioDevice,
            currentStep: 1,
            itemsToBind: new Map(),
        }
    },

    computed: {
        itemSearchFetchFunction() {
            if (!this.itemSearchType) {
                return () => [];
            }

            switch (this.itemSearchType.key) {
                case ItemType.RadioDevice.key:
                    return itemsStore.fetchRadiosPage;
                case ItemType.Pager.key:
                    return itemsStore.fetchPagersPage;
                case ItemType.Phone.key:
                    return itemsStore.fetchPhonesPage;
                case ItemType.Callbox.key:
                    return itemsStore.fetchCallboxesPage;
            }
        },

        stepperCanAdvance() {
            switch (this.currentStep) {
                case 1:
                    return !!this.selectedUser;
                case 2:
                    return this.itemsToBind.size > 0;
                case 3:
                    return false;
                case 4:
                    return false;
            }
        }
    },

    methods: {
        onUserSelected(user: any) {
            this.selectedUser = user;
        },

        onItemSelect(item: any) {
            if (item) {
                this.addItemToBasket(item);
                this.$refs.itemSelector.clear();
            }
        },

        addItemToBasket(item: any) {
            this.itemsToBind.set(item.id, {
                type: this.itemSearchType,
                item: item
            });
        },

        removeItemFromBasket(itemId: number) {
            this.itemsToBind.delete(itemId);
        },

        clearBasket() {
            this.itemsToBind.clear();
        }
    }

})
</script>