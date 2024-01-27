<template>
    <v-container class="fill-height">
        <v-row>
            <v-col>
                <v-sheet
                    max-width="500"
                    elevation="4"
                    class="mx-auto align-self-center"
                    rounded
                >
                    <v-card>
                        <v-card-title>
                            Logout
                        </v-card-title>

                        <v-card-text>
                            Are you sure that you want to logout?
                        </v-card-text>

                        <v-card-actions>
                            <v-btn color="primary" @click="logout">Logout</v-btn>
                            <v-btn color="muted" @click="abort">Cancel</v-btn>
                        </v-card-actions>
                    </v-card>
                </v-sheet>
            </v-col>
        </v-row>
    </v-container>
</template>

<style scoped>

</style>

<script lang="ts">
import {useAuthStore} from "@/store/auth";
import router from "@/router";

const authStore = useAuthStore();

if (!authStore.isLoggedIn) {
    router.push('/login');
}

export default {
    name: 'LogoutForm',
    methods: {
        logout() {
            authStore.logout();
            router.push('/');
        },
        abort() {
            router.back();
        },
    }
}
</script>
