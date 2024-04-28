<template>
    <v-container class="main-container-boxed">
        <v-row>
            <v-col>
                <h1>Return Items</h1>
            </v-col>
        </v-row>
        <v-row>
            <v-col>
                <v-stepper
                    v-model="currentStep"
                    :items="['User', 'Items', 'Review', 'Unbinding']"
                    alt-labels
                >
                    <template v-slot:item.1>
                        <v-card title="Select User" flat>
                            <v-card-text>
                                <ServerItemSelector
                                    ref="userSelector"
                                    :fetch-function="usersStore.fetchUsersPage"
                                    label="Username or Reg-ID"
                                    icon="mdi-account"
                                    item-title-key="pretty_name"
                                    item-value-key="id"
                                    :autofocus="true"
                                    @update:selection="onUserSelected"
                                ></ServerItemSelector>

                                <ServerItemSelector
                                    ref="callsignSelector"
                                    :fetch-function="usersStore.fetchUsersPageByCallsign"
                                    label="Callsign"
                                    icon="mdi-cellphone-basic"
                                    item-title-key="pretty_name"
                                    item-value-key="id"
                                    :autofocus="false"
                                    :no-filter="true"
                                    @update:selection="onUserSelected"
                                ></ServerItemSelector>

                                <v-alert
                                    v-if="$route.query.itemid"
                                    type="info"
                                >
                                    <p>
                                        You have been redirected here to return a predefined item. Please select a user to continue.
                                    </p>
                                    <p v-if="$route.query.skipbasket">
                                        After selecting a user, you will be taken to the review step immediately.
                                    </p>
                                </v-alert>
                            </v-card-text>
                        </v-card>
                    </template>

                    <template v-slot:item.2>
                        <v-card title="Select Items" flat>
                            <v-card-text>
                                <div v-if="userBindingsLoading">
                                    <v-alert
                                        type="info"
                                        title=""
                                        text="Retrieving bindings for user. Please wait..."
                                    >
                                        <v-progress-linear
                                            class="mt-3"
                                            color="primary"
                                            indeterminate
                                        ></v-progress-linear>
                                    </v-alert>
                                </div>
                                <div v-if="!userBindingsLoading">
                                    <div v-if="userBindings.length == 0">
                                        <v-alert
                                            type="success"
                                            title="No Bindings"
                                            :text="'The user ' + (selectedUser as any).pretty_name + ' currently has no active bindings.'"
                                        ></v-alert>
                                    </div>
                                    <div v-if="userBindings.length > 0">
                                        <p>
                                            Please select the items you would like to unbind from {{ (selectedUser as any).pretty_name }}.
                                        </p>
                                        <v-card flat>
                                            <v-card-text>
                                                <v-list>
                                                    <v-item-group
                                                        v-model="bindingsToRemove"
                                                        multiple
                                                    >
                                                        <v-item
                                                            v-for="binding in userBindings"
                                                            v-slot="{ isSelected, toggle }"
                                                            :value="binding"
                                                        >
                                                            <v-hover>
                                                                <template v-slot:default="{ isHovering, props }">
                                                                    <v-list-item
                                                                        v-bind="props"
                                                                        :active="isSelected"
                                                                        @click="toggle"
                                                                        color="primary"
                                                                        base-color="grey-darken-1"
                                                                        rounded
                                                                    >
                                                                        <template v-slot:prepend>
                                                                            <v-icon>{{ ItemType.get(binding.item.resourcetype).icon }}</v-icon>
                                                                        </template>

                                                                        <v-list-item-title>
                                                                            {{ binding.item.pretty_name }}
                                                                        </v-list-item-title>

                                                                        <template v-slot:append>
                                                                            <v-checkbox-btn
                                                                                readonly
                                                                                :model-value="isSelected"
                                                                            ></v-checkbox-btn>
                                                                        </template>
                                                                    </v-list-item>
                                                                </template>
                                                            </v-hover>
                                                        </v-item>
                                                    </v-item-group>
                                                </v-list>
                                                <v-sheet width="100%" class="mt-2 text-center">

                                                </v-sheet>
                                            </v-card-text>
                                        </v-card>
                                    </div>
                                </div>
                            </v-card-text>
                        </v-card>
                    </template>

                    <template v-slot:item.3>
                        <v-card title="Review Items to Unbind" flat>
                            <v-card-text>
                                Please review your action. You are about to unbind {{ bindingsToRemove.length }} items from {{ selectedUser.nickname }}.
                            </v-card-text>
                        </v-card>

                        <v-card title="User" flat>
                            <v-card-text>
                                {{ (selectedUser as any).pretty_name }}
                            </v-card-text>
                        </v-card>

                        <ItemBasket
                            ref="reviewBasket"
                            title="Items"
                            :basket-items="itemsToUnbind"
                            :read-only="true"
                            :flat="true"
                        ></ItemBasket>
                    </template>

                    <template v-slot:item.4>
                        <v-card title="Unbinding Items" flat>
                            <div v-if="unbindingInProgress">
                                <v-alert
                                    type="info"
                                    text="Unbinding items from user. Please wait..."
                                >
                                    <v-progress-linear
                                        class="mt-3"
                                        color="primary"
                                        indeterminate
                                    ></v-progress-linear>
                                </v-alert>
                            </div>
                            <div v-if="!unbindingInProgress">
                                <div v-if="unbindingError">
                                    <v-alert
                                        v-if="unbindingError"
                                        type="error"
                                        title="Error"
                                        :text="unbindingError"
                                    ></v-alert>
                                </div>
                                <div v-if="!unbindingError">
                                    <v-alert
                                        type="success"
                                        title="Items unbound"
                                        :text="'Successfully unbound ' + bindingsToRemove.length + ' items from ' + (selectedUser as any).pretty_name + '.'"
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
                                v-if="currentStep == 2 && !userBindingsLoading && userBindings.length > 0"
                                color="primary"
                                @click="bindingsToRemove = userBindings; currentStep++;"
                                class="mr-3"
                            >
                                Unbind all
                            </v-btn>
                            <v-btn
                                v-if="currentStep < 4 && !stepperCanReset"
                                :disabled="!stepperCanAdvance"
                                @click="currentStep++"
                            >
                                <span v-if="currentStep != 3">Next</span>
                                <span v-if="currentStep == 3">Confirm</span>
                            </v-btn>
                            <v-btn
                                v-if="stepperCanReset"
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
</script>

<script lang="ts">
import { defineComponent } from "vue";
import {useUsersStore} from "@/store/users";
import {ItemType} from "@/types/ItemType";
import {useBindingsStore} from "@/store/bindings";
import {emptyItemsBasket} from "@/components/ItemBasket.vue";
import {useToast} from "vue-toastification";

const toast = useToast();
const usersStore = useUsersStore();
const bindingsStore = useBindingsStore();

export default defineComponent({
    name: "BindingsReturn",

    data() {
        return {
            // Global
            currentStep: 1,

            // Step 1 (User)
            selectedUser: {nickname: 'unknown'},

            // Step 2 (Items)
            userBindings: [] as any[],
            userBindingsLoading: true,

            // Step 3 (Review)
            bindingsToRemove: [] as any[],
            itemsToUnbind: emptyItemsBasket(),

            // Step 4 (Binding)
            unbindingInProgress: true,
            unbindingError: "",
        }
    },

    mounted() {
        if (this.$route.query.itemid) {
            const itemId = parseInt(this.$route.query.itemid.toString());
            bindingsStore.fetchBindingByItemId(itemId)
                .then((resp) => {
                    if (!resp.data || !resp.data.item || !resp.data.user || resp.data.item.id != itemId) {
                        toast.error("Failed to select predefined item: Item not found or not handed out.");
                    }

                    this.selectedUser = resp.data.user;
                    this.bindingsToRemove = [resp.data];
                    this.currentStep = this.$route.query.skipbasket ? 3 : 2;
                })
                .catch((error) => {
                    toast.error("Failed to select predefined item: Request to backend API failed.");
                })
                .finally(() => {
                    this.$router.replace({query: {
                        ...this.$route.query,
                        itemid: undefined,
                        skipbasket: undefined,
                    }});
                });
        }
    },

    computed: {
        stepperCanAdvance() {
            switch (this.currentStep) {
                case 1:
                    return !!this.selectedUser;
                case 2:
                    return this.bindingsToRemove.length > 0;
                case 3:
                    return true;
                case 4:
                    return true;
            }
        },

        stepperCanReset() {
            return (this.currentStep == 4)
                || (this.currentStep == 2 && !this.userBindingsLoading && this.userBindings.length == 0);
        },
    },

    watch: {
        currentStep(newStep, oldStep) {
            // Enter into item selection step
            if (newStep == 2) {
                this.userBindingsLoading = true;
                // @ts-ignore
                bindingsStore.fetchBindingsForUser(this.selectedUser.id).then((resp) => {
                    this.userBindings = resp.data;
                    this.userBindingsLoading = false;
                });
            }

            // Put review items into review basket
            if (oldStep <= 2 && newStep == 3) {
                this.itemsToUnbind.clear();
                this.bindingsToRemove.forEach((binding) => {
                    this.itemsToUnbind.set(binding.item.id, { type: ItemType.get(binding.item.resourcetype), item: binding.item });
                });
            }

            // Enter into binding creation step
            if (newStep == 4) {
                this.unbindingInProgress = true;
                bindingsStore.deleteBindings(
                    this.bindingsToRemove.map((binding) => binding.id)
                ).then((resp) => {
                    this.unbindingError = "";
                    this.unbindingInProgress = false;
                }).catch((error) => {
                    if (error.response) {
                        // Print object as json is response.data is object
                        if (typeof error.response.data === "object") {
                            this.unbindingError = JSON.stringify(error.response.data);
                        } else {
                            this.unbindingError = error.response.data;
                        }
                    } else if (error.request) {
                        this.unbindingError = "The request was made but no response was received. Please try again later.";
                    } else {
                        this.unbindingError = error.message;
                    }

                    this.unbindingInProgress = false;
                })
            }
        },
    },

    methods: {
        reset() {
            (this.$refs.userSelector as InstanceType<typeof ServerItemSelector>).clear();
            (this.$refs.callsignSelector as InstanceType<typeof ServerItemSelector>).clear();
            this.selectedUser = {nickname: 'unknown'};
            this.userBindings = [];
            this.userBindingsLoading = true;
            this.bindingsToRemove = [];
            this.itemsToUnbind.clear();
            this.unbindingInProgress = true;
            this.unbindingError = "";
            this.currentStep = 1;
        },

        onUserSelected(user: any) {
            this.selectedUser = user;
            setTimeout(() => {
                this.currentStep++;
            }, 250);
        },
    }

})
</script>
