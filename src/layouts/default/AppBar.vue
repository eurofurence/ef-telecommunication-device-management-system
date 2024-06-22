<!--
Eurofurence Telecommunication Device Management System (EF-TDMS)
Copyright (C) 2024 Niels Gandraß <niels@gandrass.de>

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
                <v-list-item prepend-icon="mdi-form-textbox-password" title="Change Password" value="change-password" :href="passwordChangeUrl" target="_blank"></v-list-item>
                <v-list-item prepend-icon="mdi-logout" title="Logout" value="logout" to="/logout"></v-list-item>
            </v-list>
        </v-menu>
    </v-app-bar>
</template>

<script lang="ts" setup>
import {useAuthStore} from "@/store/auth";

const authStore = useAuthStore();
const passwordChangeUrl = import.meta.env.VITE_EFTDMS_PASSWORD_CHANGE_URL;
</script>
