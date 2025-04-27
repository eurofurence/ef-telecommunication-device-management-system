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
