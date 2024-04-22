<template>
    <v-app-bar color="#006357" class="pr-2">
        <v-app-bar-title>
            <router-link to="/" class="d-flex align-center text-decoration-none font-weight-medium text-white">
                <v-img src="@/assets/logo-white.png" width="50" class="mr-3" inline/>
                <div>Eurofurence Telecommunication Device Management System</div>
            </router-link>
        </v-app-bar-title>

        <v-btn v-if="!authStore.isLoggedIn" to="/login" text>Login</v-btn>
        <router-link v-if="authStore.isLoggedIn" to="/profile">
            <v-avatar color="grey" size="36" class="mx-2">
                <span class="white--text headline">{{authStore.username.slice(0, 2).toUpperCase()}}</span>
            </v-avatar>
        </router-link>
    </v-app-bar>
</template>

<script lang="ts" setup>
import {useAuthStore} from "@/store/auth";

const authStore = useAuthStore();
</script>
