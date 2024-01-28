<template>
    <v-app-bar >
        <v-app-bar-title>
            <router-link to="/" class="text-decoration-none font-weight-medium" style="color: #d900d9">
                <v-icon icon="mdi-radio-tower"/>
                EF-RMS
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
