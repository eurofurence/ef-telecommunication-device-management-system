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
    <v-container class="main-container-boxed">
        <v-row>
            <v-col>
                <h1>Hand Out Items</h1>
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
                            <v-card-text>
                                <v-alert
                                    v-if="$route.query.itemid"
                                    type="info"
                                    class="mb-5"
                                >
                                    <p>
                                        You have been redirected here to hand out a predefined item. Please select a user to continue.
                                    </p>
                                    <p v-if="$route.query.skipbasket">
                                        After selecting a user, you will be taken to the review step immediately.
                                    </p>
                                </v-alert>

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
                            </v-card-text>
                        </v-card>
                    </template>

                    <template v-slot:item.2>
                        <v-card title="Select Items" flat>
                            <v-card-text>
                                <v-btn-toggle
                                    v-model="itemSearchType"
                                    variant="outlined"
                                    color="primary"
                                    divided
                                    @update:model-value="($refs.itemSelector as InstanceType<typeof ServerItemSelector>).clear(); onItemSelect(null);"
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

                                <p class="text-overline">
                                    Quick Add Templates
                                </p>
                                <span v-if="!showAllQuickAddTemplates && compatibleQuickAddTemplates.length === 0 && basketIsEmpty">
                                    Please add an item to the basket to see compatible items.
                                </span>
                                <span v-if="!showAllQuickAddTemplates && compatibleQuickAddTemplates.length === 0 && !basketIsEmpty">
                                    No compatible items found.
                                </span>
                                <v-btn
                                    v-for="template in compatibleQuickAddTemplates"
                                    :key="template.id"
                                    :disabled="template.statistics.available == 0"
                                    prepend-icon="mdi-plus-circle"
                                    variant="outlined"
                                    color="green"
                                    class="mx-2 my-1"
                                    @click="($refs.basket as InstanceType<typeof ItemBasket>).addItemTemplate(template, ItemTemplateType.get(template.type))"
                                >
                                    {{ template.name }} ({{ template.owner.shortname }})
                                    <template v-slot:append>
                                        [{{ template.statistics.available }}]
                                    </template>
                                </v-btn>
                                <v-btn
                                    v-if="!showAllQuickAddTemplates && moreQuickAddTemplatesAvailable"
                                    prepend-icon="mdi-plus-circle"
                                    variant="outlined"
                                    color="warning"
                                    class="mx-2 my-1"
                                    size="small"
                                    @click="showAllQuickAddTemplates = true"
                                >
                                    Show all
                                </v-btn>
                                <v-btn
                                    v-if="showAllQuickAddTemplates"
                                    prepend-icon="mdi-minus-circle"
                                    variant="outlined"
                                    color="warning"
                                    class="mx-2 my-1"
                                    size="small"
                                    @click="showAllQuickAddTemplates = false"
                                >
                                    Show compatible only
                                </v-btn>

                                <v-divider class="mt-5 mb-3"></v-divider>

                                <v-container>
                                    <v-row>
                                        <v-col cols="12" md="8">
                                            <ItemBasket
                                                ref="basket"
                                                :basket-items="itemsToBind"
                                                :basket-item-templates="itemTemplatesToBind"
                                                @update:basket="basketIsEmpty = ($refs.basket as InstanceType<typeof ItemBasket>).isEmpty(); itemIdsToExclude = ($refs.basket as InstanceType<typeof ItemBasket>).getItemIds();"
                                                :read-only="false"
                                            ></ItemBasket>
                                        </v-col>
                                        <v-col cols="12" md="4">
                                            <OrderList
                                                :orders="orders"
                                            ></OrderList>
                                        </v-col>
                                    </v-row>
                                </v-container>
                            </v-card-text>
                        </v-card>
                    </template>

                    <template v-slot:item.3>
                        <v-card title="Review Binding" flat>
                            <v-card-text>
                                Please review your binding before creating it. You are about to bind {{ ($refs.basket as any).size() }} items to {{ (selectedUser as any).nickname }}.
                            </v-card-text>
                        </v-card>

                        <v-card title="User" flat>
                            <v-card-text>
                                {{ (selectedUser as any).pretty_name }}
                            </v-card-text>
                        </v-card>

                        <ItemBasket
                            ref="reviewBasket"
                            :basket-items="itemsToBind"
                            :basket-item-templates="itemTemplatesToBind"
                            :read-only="true"
                        ></ItemBasket>
                    </template>

                    <template v-slot:item.4>
                        <v-card title="Create Binding" flat>
                            <div v-if="bindingInProgress">
                                <v-alert
                                    type="info"
                                    text="Binding items to user. Please wait..."
                                >
                                    <v-progress-linear
                                        class="mt-3"
                                        color="primary"
                                        indeterminate
                                    ></v-progress-linear>
                                </v-alert>
                            </div>
                            <div v-if="!bindingInProgress">
                                <div v-if="bindingError">
                                    <v-alert
                                        v-if="bindingError"
                                        type="error"
                                        title="Error"
                                        :text="bindingError"
                                    ></v-alert>
                                </div>
                                <div v-if="!bindingError">
                                    <v-alert
                                        type="success"
                                        title="Binding created"
                                        :text="'Successfully bound ' + createdBindings.length + ' items to ' + (selectedUser as any).pretty_name + '.'"
                                    ></v-alert>
                                </div>
                            </div>
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
                        <v-sheet>
                            <v-btn
                                v-if="currentStep < 4"
                                :disabled="!stepperCanAdvance"
                                @click="currentStep++"
                            >
                                <span v-if="currentStep != 3">Next</span>
                                <span v-if="currentStep == 3">Confirm</span>
                            </v-btn>
                            <v-btn
                                v-if="currentStep == 4"
                                :disabled="false"
                                @click="reset()"
                            >
                                Restart
                            </v-btn>
                            <v-btn
                                v-if="currentStep == 4 && $route.query.returnpath"
                                :to="String($route.query.returnpath)"
                                :disabled="false"
                                color="primary"
                                class="ml-4"
                            >
                                Return to previous page
                            </v-btn>
                        </v-sheet>
                    </template>
                </v-stepper>

            </v-col>
        </v-row>
    </v-container>
</template>

<script setup lang="ts">
import ServerItemSelector from "@/components/ServerItemSelector.vue";
import ItemBasket from "@/components/ItemBasket.vue";
import OrderList from "@/components/OrderList.vue";
</script>

<script lang="ts">
import {defineComponent} from "vue";
import {useUsersStore} from "@/store/users";
import {useItemsStore} from "@/store/items";
import {ItemTemplateType, ItemType} from "@/types/ItemType";
import {emptyItemsBasket, emptyItemTemplatesBasket} from "@/components/ItemBasket.vue";
import {useBindingsStore} from "@/store/bindings";
import {useToast} from "vue-toastification";

const toast = useToast();
const usersStore = useUsersStore();
const itemsStore = useItemsStore();
const bindingsStore = useBindingsStore();

const emptyItemSearchFunction = async () => ({
    items: [],
    total: 0
});

export default defineComponent({
    name: "BindingsIssue",

    data() {
        return {
            // Global
            currentStep: 1,

            // Step 1 (User)
            selectedUser: null,

            // Step 2 (Items)
            itemSearchType: ItemType.RadioDevice,
            quickAddTemplates: [] as any[],
            showAllQuickAddTemplates: false,
            basketIsEmpty: true,
            itemIdsToExclude: [] as number[],
            orders: [] as any[],

            // Step 3 (Review)
            itemsToBind: emptyItemsBasket(),
            itemTemplatesToBind: emptyItemTemplatesBasket(),

            // Step 4 (Binding)
            bindingInProgress: false,
            bindingError: "",
            createdBindings: [] as any[],
        }
    },

    computed: {
        itemSearchFetchFunction() {
            if (!this.itemSearchType) {
                return emptyItemSearchFunction;
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
                default:
                    return emptyItemSearchFunction;
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

        itemTemplateIdsInBasket() {
            let templateIds = new Set<number>();

            this.itemsToBind.forEach((entry) => {
                if (!entry.item.template) {
                    return;
                }

                templateIds.add(entry.item.template.id);
            });
            this.itemTemplatesToBind.forEach((entry) => {
                if (!entry.template) {
                    return;
                }

                templateIds.add(entry.template.id);
            });

            return templateIds;
        },

        compatibleQuickAddTemplates() {
            if (this.showAllQuickAddTemplates) {
                return this.quickAddTemplates;
            }

            let templateIdsInBasket = this.itemTemplateIdsInBasket;
            return this.quickAddTemplates.filter((template) => {
                if (template.compatible_with) {
                    if (template.compatible_with.length === 0) {
                        // Show items without any compatibility limitations
                        return true;
                    } else {
                        // Compatibility limitations given. Filter
                        return template.compatible_with.some((id: number) => templateIdsInBasket.has(id));
                    }
                } else {
                    // Show if no compatibility list given
                    return true;
                }
            });
        },

        moreQuickAddTemplatesAvailable() {
            return this.compatibleQuickAddTemplates.length < this.quickAddTemplates.length;
        },
    },

    watch: {
        currentStep(newStep, oldStep) {
            // Enter into item selection step
            if (newStep == 2) {
                if (this.$route.query.itemid) {
                    this.addItemToBasketById(
                        parseInt(String(this.$route.query.itemid)),
                        (String(this.$route.query.skipbasket) === "true") ?? false
                    );

                    this.$router.replace({query: {
                        ...this.$route.query,
                        itemid: undefined,
                        skipbasket: undefined,
                    }});
                }

                itemsStore.fetchQuickAddTemplates().then((resp) => {
                    this.quickAddTemplates = resp.items;
                });

                // @ts-ignore
                bindingsStore.fetchOrdersForUser(this.selectedUser.id).then((resp) => {
                    this.orders = resp.data;
                });
            }

            // Enter into binding creation step
            if (newStep == 4) {
                this.bindingInProgress = true;
                bindingsStore.createBindings(
                    // @ts-ignore
                    this.selectedUser.id,
                    [...this.itemsToBind.keys()],
                    this.itemTemplatesToBind.map((template) => template.template.id)
                ).then((resp) => {
                    this.createdBindings = resp.data;
                    this.bindingError = "";
                    this.bindingInProgress = false;
                }).catch((error) => {
                    if (error.response) {
                        // Print object as json is response.data is object
                        if (typeof error.response.data === "object") {
                            this.bindingError = JSON.stringify(error.response.data);
                        } else {
                            this.bindingError = error.response.data;
                        }
                    } else if (error.request) {
                        this.bindingError = "The request was made but no response was received. Please try again later.";
                    } else {
                        this.bindingError = error.message;
                    }

                    this.bindingInProgress = false;
                })
            }
        }
    },

    methods: {
        reset() {
            (this.$refs.itemSelector as InstanceType<typeof ServerItemSelector>).clear();
            (this.$refs.userSelector as InstanceType<typeof ServerItemSelector>).clear();
            this.itemsToBind = emptyItemsBasket();
            this.itemTemplatesToBind = emptyItemTemplatesBasket();
            this.orders = [];
            this.showAllQuickAddTemplates = false;
            this.bindingInProgress = false;
            this.bindingError = "";
            this.createdBindings = [];
            this.currentStep = 1;
        },

        onUserSelected(user: any) {
            this.selectedUser = user;
            setTimeout(() => {
                this.currentStep++;
            }, 250);
        },

        onItemSelect(item: any) {
            if (item) {
                (this.$refs.basket as InstanceType<typeof ItemBasket>).addItem(item, this.itemSearchType);
                (this.$refs.itemSelector as InstanceType<typeof ServerItemSelector>).clear();
            }
        },

        addItemToBasketById(itemId: number, advanceOnSuccess: boolean = false) {
            if (isNaN(itemId) || itemId <= 0) {
                toast.error("Failed to autoadd item with ID " + itemId + ": Invalid ID.");
                return;
            }

            itemsStore.fetchItemMetadata(itemId)
                .then((resp) => {
                    if (!resp.data || !resp.data.id || resp.data.id != itemId) {
                        toast.error("Failed to autoadd item with ID " + itemId + ": Item not found.");
                        return;
                    }

                    if (resp.data.handed_out) {
                        toast.error("Failed to autoadd item with ID " + itemId + ": Item is already handed out.");
                        return;
                    }

                    (this.$refs.basket as InstanceType<typeof ItemBasket>).addItem(resp.data, ItemType.get(resp.data.resourcetype));

                    if (advanceOnSuccess) {
                        this.currentStep++;
                    }
                })
                .catch((error) => {
                    toast.error("Failed to autoadd item with ID " + itemId + ": Remote API request failed.");
                });

        }
    }

})
</script>