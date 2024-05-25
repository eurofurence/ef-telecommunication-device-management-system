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
            user: {},
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
            this.bindings.forEach((binding) => {
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