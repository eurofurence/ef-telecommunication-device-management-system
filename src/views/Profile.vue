<template>
    <h1>Profile</h1>
    Hello {{ authStore.username }}
</template>

<script lang="ts" setup>
import {useAuthStore} from "@/store/auth";

const authStore = useAuthStore();
</script>