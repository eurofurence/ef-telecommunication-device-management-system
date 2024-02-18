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
                                ref="userSelector"
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
                                :item-ids-to-exclude="itemIdsToExclude"
                                :autofocus="true"
                                @update:selection="onItemSelect"
                            ></ServerItemSelector>

                            <v-btn
                                v-for="template in quickAddTemplates"
                                :key="template.id"
                                :disabled="template.statistics.available == 0"
                                prepend-icon="mdi-plus-circle"
                                variant="outlined"
                                color="green"
                                class="mx-2 my-1"
                                @click="$refs.basket.addItemTemplate(template, ItemTemplateType[template.type])"
                            >
                                {{ template.name }} ({{ template.owner.shortname }})
                                <template v-slot:append>
                                    [{{ template.statistics.available }}]
                                </template>
                            </v-btn>

                            <ItemBasket
                                ref="basket"
                                :basket-items="itemsToBind"
                                :basket-item-templates="itemTemplatesToBind"
                                @update:basket="basketIsEmpty = $refs.basket.isEmpty(); itemIdsToExclude = $refs.basket.getItemIds();"
                            ></ItemBasket>
                        </v-card>
                    </template>

                    <template v-slot:item.3>
                        <v-card title="Review Binding" flat>
                            <v-card-text>
                                Please review your binding before creating it. You are about to bind {{ $refs.basket.size() }} items to {{ selectedUser.username }}.
                            </v-card-text>
                        </v-card>

                        <v-card title="User" flat>
                            <v-card-text>
                                {{ selectedUser.pretty_name }}
                            </v-card-text>
                        </v-card>

                        <ItemBasket
                            ref="basket"
                            :basket-items="itemsToBind"
                            :basket-item-templates="itemTemplatesToBind"
                            :read-only="true"
                        ></ItemBasket>
                    </template>

                    <template v-slot:item.4>
                        <v-card title="Binding Created" flat>
                            <v-alert
                                type="error"
                                title="Not implemented yet"
                                text="Sorry Dave, I'm afraid I can't do that. This functionality is not implemented yet. Please try again later."
                            ></v-alert>
                        </v-card>
                    </template>

                    <template v-slot:prev>
                        <v-btn
                            :disabled="currentStep == 1 || currentStep >= 4"
                            @click="currentStep--"
                        >
                            Previous
                        </v-btn>
                    </template>

                    <template v-slot:next>
                        <v-btn
                            v-if="currentStep < 4"
                            :disabled="!stepperCanAdvance"
                            @click="currentStep++"
                        >
                            Next
                        </v-btn>
                        <v-btn
                            v-if="currentStep == 4"
                            :disabled="false"
                            @click="reset()"
                        >
                            Restart
                        </v-btn>
                    </template>
                </v-stepper>

            </v-col>
        </v-row>
    </v-container>
</template>

<script setup lang="ts">
import ServerItemSelector from "@/components/ServerItemSelector.vue";
import ItemBasket from "@/components/ItemBasket.vue";
</script>

<script lang="ts">
import { defineComponent } from "vue";
import {useUsersStore} from "@/store/users";
import {useItemsStore} from "@/store/items";
import {ItemTemplateType, ItemType} from "@/types/ItemType";
import { emptyItemsBasket, emptyItemTemplatesBasket } from "@/components/ItemBasket.vue";

const usersStore = useUsersStore();
const itemsStore = useItemsStore();

export default defineComponent({

    data() {
        return {
            // Global
            currentStep: 1,

            // Step 1 (User)
            selectedUser: null,

            // Step 2 (Items)
            itemSearchType: ItemType.RadioDevice,
            quickAddTemplates: [],
            basketIsEmpty: true,
            itemIdsToExclude: [],

            // Step 3 (Review)
            itemsToBind: emptyItemsBasket(),
            itemTemplatesToBind: emptyItemTemplatesBasket(),
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
                    return !this.basketIsEmpty;
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
        reset() {
            this.$refs.itemSelector.clear();
            this.$refs.userSelector.clear();
            this.$refs.basket.clear();
            this.itemsToBind = emptyItemsBasket();
            this.itemTemplatesToBind = emptyItemTemplatesBasket();
            this.currentStep = 1;
        },

        onUserSelected(user: any) {
            this.selectedUser = user;
        },

        onItemSelect(item: any) {
            if (item) {
                this.$refs.basket.addItem(item, this.itemSearchType)
                this.$refs.itemSelector.clear();
            }
        },
    }

})
</script>