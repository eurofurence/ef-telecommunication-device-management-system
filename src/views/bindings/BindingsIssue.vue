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
                    :items="['User', 'Items', 'Review', 'Binding']"
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
                                <v-btn v-for="type in ItemType.getAll()" :value="type">
                                    <v-icon start>{{ type.icon }}</v-icon>
                                    <span class="hidden-sm-and-down">{{ type.shortLabel }}</span>
                                </v-btn>
                            </v-btn-toggle>
                            <ServerItemSelector
                                ref="itemSelector"
                                :fetch-function="itemSearchFetchFunction"
                                :available-only="true"
                                :label="itemSearchType.label"
                                :icon="itemSearchType.icon"
                                item-title-key="pretty_name"
                                item-value-key="id"
                                :item-ids-to-exclude="Array.from(itemsToBind.keys())"
                                :autofocus="true"
                                @update:selection="onItemSelect"
                            ></ServerItemSelector>

                            <v-btn
                                v-for="template in quickAddTemplates"
                                :key="template.id"
                                prepend-icon="mdi-plus-circle"
                                variant="outlined"
                                color="green"
                                class="mx-2 my-1"
                                @click="addItemTemplateToBasket(template)"
                            >
                                {{ template.name }} ({{ template.owner.shortname }})
                                <template v-slot:append>
                                    [{{ template.statistics.available }}]
                                </template>
                            </v-btn>

                            <v-card flat>
                                <v-card-title>Basket</v-card-title>
                                <v-card-text>
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
                                        <v-divider v-if="itemsToBind.size > 0 && itemTemplatesToBind.length > 0"></v-divider>
                                        <v-list-item v-for="(entry, idx) in itemTemplatesToBind">
                                            <template v-slot:prepend>
                                                <v-icon>{{ entry.type.itemType.icon }}</v-icon>
                                            </template>

                                            <v-list-item-title>{{ entry.template.pretty_name }}</v-list-item-title>

                                            <template v-slot:append>
                                                <v-btn icon="mdi-delete" @click="removeItemTemplateFromBasket(idx)"
                                                       variant="flat"></v-btn>
                                            </template>
                                        </v-list-item>
                                    </v-list>
                                </v-card-text>
                            </v-card>
                        </v-card>
                    </template>

                    <template v-slot:item.3>
                        <v-card title="Review Binding" flat>...</v-card>
                    </template>

                    <template v-slot:item.4>
                        <v-card title="Binding Created" flat>...</v-card>
                    </template>

                    <template v-slot:next>
                        <v-btn
                            :disabled="!stepperCanAdvance"
                            @click="currentStep++"
                        >
                            Next
                        </v-btn>
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
import {ItemTemplateType, ItemType} from "@/types/ItemType";

const usersStore = useUsersStore();
const itemsStore = useItemsStore();

// TODO: Only show items that are not already bound

export default defineComponent({

    data() {
        return {
            selectedUser: null,
            itemSearchType: ItemType.RadioDevice,
            currentStep: 1,
            itemsToBind: new Map(),
            itemTemplatesToBind: [],
            quickAddTemplates: [],
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
                case ItemType.RadioAccessory.key:
                    return itemsStore.fetchRadioAccessoriesPage;
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
                    return !this.basketIsEmpty();
                case 3:
                    return true;
                case 4:
                    return true;
            }
        },

    },

    watch: {
        currentStep(newStep, oldStep) {
            if (newStep == 2) {
                itemsStore.fetchQuickAddTemplates().then((resp) => {
                    this.quickAddTemplates = resp.items;
                });
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

        addItemTemplateToBasket(template: any) {
            this.itemTemplatesToBind.push({
                type: ItemTemplateType[template.type],
                template: template
            });
        },

        removeItemFromBasket(itemId: number) {
            this.itemsToBind.delete(itemId);
        },

        removeItemTemplateFromBasket(idx: number) {
            this.itemTemplatesToBind.splice(idx, 1);
        },

        basketIsEmpty() {
            return this.itemsToBind.size === 0 && this.itemTemplatesToBind.length === 0;
        },

        clearBasket() {
            this.itemsToBind.clear();
            this.itemTemplatesToBind = [];
        }
    }

})
</script>