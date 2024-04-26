<template>
    <v-app-bar color="#006357" class="pr-2">
        <v-app-bar-title>
            <router-link to="/" class="d-flex align-center text-decoration-none font-weight-medium text-white">
                <v-img src="@/assets/logo-white.png" width="50" class="mr-3" inline/>
                <div>Eurofurence Telecommunication Device Management System</div>
            </router-link>
        </v-app-bar-title>

        <v-btn v-if="!authStore.isLoggedIn" to="/login">Login</v-btn>
        <v-menu v-if="authStore.isLoggedIn">
            <template v-slot:activator="{ props }">
                <v-btn
                    v-bind="props"
                    icon
                >
                    <v-avatar color="grey" size="36" class="mx-2">
                        <span class="white--text headline">{{ (authStore.username ?? '??').slice(0, 2).toUpperCase() }}</span>
                    </v-avatar>
                </v-btn>
            </template>

            <v-list density="compact" slim>
                <v-list-item prepend-icon="mdi-account" title="My Account" value="account" to="/profile"></v-list-item>
                <v-list-item prepend-icon="mdi-logout" title="Logout" value="logout" to="/logout"></v-list-item>
            </v-list>
        </v-menu>
    </v-app-bar>
</template>

<script lang="ts" setup>
import {useAuthStore} from "@/store/auth";

const authStore = useAuthStore();
</script>
