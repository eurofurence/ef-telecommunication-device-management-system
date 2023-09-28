<template>
  <HelloWorld />
</template>

<script lang="ts" setup>
    import HelloWorld from '@/components/HelloWorld.vue'

    import {useAuthStore} from "@/store/auth";
    import {useUsersStore} from "@/store/users";
    const authStore = useAuthStore();
    await authStore.login("admin", "admin");

    const userStore = useUsersStore();
    await userStore.fetchUsers();
    userStore.users.forEach(user => console.log(user));
</script>
