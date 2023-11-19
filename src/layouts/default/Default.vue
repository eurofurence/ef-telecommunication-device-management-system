<template>
    <v-app>
        <v-layout>
            <DefaultBar/>
            <DefaultMenu v-if="authStore.isLoggedIn"/>
            <DefaultView/>
        </v-layout>
    </v-app>
</template>

<script lang="ts" setup>
import DefaultBar from './AppBar.vue';
import DefaultMenu from './AppMenu.vue';
import DefaultView from './View.vue';
import {useAuthStore} from "@/store/auth";

const authStore = useAuthStore();
</script>
