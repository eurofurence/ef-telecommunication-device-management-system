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
    <v-container>
        <v-row>
            <v-col>
                <h1>Profile</h1>
            </v-col>
        </v-row>
        <v-row class="mt-0">
            <v-col>
                <v-list>
                    <v-list-item
                        title="Username"
                        prepend-icon="mdi-account-key"
                    >
                        <v-list-item-subtitle>{{ username }}</v-list-item-subtitle>
                    </v-list-item>
                    <v-list-item
                        title="Nickname"
                        prepend-icon="mdi-account"
                    >
                        <v-skeleton-loader v-if="loading.user" type="text" max-width="256" class="no-margin-loader"></v-skeleton-loader>
                        <v-list-item-subtitle v-if="!loading.user">{{ user.nickname ?? 'N/A' }}</v-list-item-subtitle>
                    </v-list-item>
                    <v-list-item
                        title="EF Registration ID"
                        prepend-icon="mdi-ticket-account"
                    >
                        <v-skeleton-loader v-if="loading.user" type="text" max-width="256" class="no-margin-loader"></v-skeleton-loader>
                        <v-list-item-subtitle v-if="!loading.user">{{ user.ef_reg_id ?? 'N/A' }}</v-list-item-subtitle>
                    </v-list-item>
                    <v-list-item
                        title="EF Security Collar Number"
                        prepend-icon="mdi-shield-account"
                    >
                        <v-skeleton-loader v-if="loading.user" type="text" max-width="256" class="no-margin-loader"></v-skeleton-loader>
                        <v-list-item-subtitle v-if="!loading.user">{{ user.ef_security_collar_id ?? 'N/A' }}</v-list-item-subtitle>
                    </v-list-item>
                    <v-list-item
                        prepend-icon="mdi-form-textbox-password"
                    >
                            <v-list-item-title>
                                <v-btn
                                    color="primary"
                                    text="Change Password"
                                    :href="passwordChangeUrl"
                                    target="_blank"
                                    size="small"
                                ></v-btn>
                            </v-list-item-title>
                    </v-list-item>
                </v-list>
            </v-col>
        </v-row>
        <v-row>
            <v-col>
                <h2>Active Bindings</h2>
                <ItemBasket
                    ref="reviewBasket"
                    :basket-items="boundItems"
                    :read-only="true"
                    :title="null"
                ></ItemBasket>
            </v-col>
        </v-row>
    </v-container>
</template>

<script lang="ts" setup>
const passwordChangeUrl = import.meta.env.VITE_EFTDMS_PASSWORD_CHANGE_URL;
</script>

<script lang="ts">
import {defineComponent} from "vue";
import {useUsersStore} from "@/store/users";
import {useAuthStore} from "@/store/auth";
import {useBindingsStore} from "@/store/bindings";
import ItemBasket from "@/components/ItemBasket.vue";
import {ItemType} from "@/types/ItemType";

const authStore = useAuthStore();
const usersStore = useUsersStore();
const bindingsStore = useBindingsStore();

export default defineComponent({
    name: "Profile",

    components: {ItemBasket},

    data() {
        return {
            username: authStore.username,
            user: {
                id: 0,
                nickname: null,
                ef_reg_id: null,
                ef_security_collar_id: null,
            },
            bindings: [],
            loading: {
                user: true,
                bindings: true,
            },
        }
    },

    computed: {
        boundItems() {
            let boundItems = new Map();
            this.bindings.forEach((binding: any) => {
                boundItems.set(binding.item.id, {
                    type: ItemType.get(binding.item.resourcetype),
                    item: binding.item,
                });
            });
            return boundItems;
        }
    },

    mounted() {
        usersStore.fetchCurrentUserProfile().then((resp) => {
            this.loading.user = false;
            this.user = resp.data;

            bindingsStore.fetchBindingsForUser(this.user.id).then((resp) => {
                this.loading.bindings = false;
                this.bindings = resp.data;
            });
        });
    },
})
</script>

<style>
    .v-skeleton-loader.no-margin-loader {
        > div {
            margin: 0;
        }
    }
</style>