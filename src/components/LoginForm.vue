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
                    <v-card v-if="authStore.isLoggedIn">
                        <v-card-title>
                            Login
                        </v-card-title>

                        <v-card-text>
                            You are currently logged in as {{authStore.username}}.
                        </v-card-text>

                        <v-card-actions>
                            <v-btn to="/logout" color="primary">Logout</v-btn>
                        </v-card-actions>
                    </v-card>
                    <v-card v-if="!authStore.isLoggedIn">
                        <v-card-title>
                            Login
                        </v-card-title>

                        <v-card-text>
                            <v-form fast-fail @submit.prevent="login">
                                <v-text-field
                                    v-model="username"
                                    name="username"
                                    label="Username"
                                    placeholder="Username"
                                    type="text"
                                    required
                                ></v-text-field>

                                <v-text-field
                                    v-model="password"
                                    name="password"
                                    label="Password"
                                    placeholder="Password"
                                    type="password"
                                    required
                                ></v-text-field>

                                <div class="text-error">{{loginFormErrorMessage}}</div>
                                <v-btn type="submit" class="mt-4" color="primary">Login</v-btn>
                            </v-form>
                        </v-card-text>
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

export default {
    name: 'LoginForm',

    data() {
        return {
            authStore: authStore,
            username: '',
            password: '',
            loginFormErrorMessage: '',
        }
    },

    methods: {
        async login() {
            try {
                await authStore.login(this.username, this.password);
                this.loginFormErrorMessage = '';
                router.push('/overview');
            } catch (e) {
                this.loginFormErrorMessage = e.message;
            } finally {
                this.username = '';
                this.password = '';
            }
        },
    }
}
</script>
