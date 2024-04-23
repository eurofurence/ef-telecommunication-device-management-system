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
                            <v-form v-model="loginFormIsValid" fast-fail @submit.prevent="login">
                                <v-text-field
                                    v-model="username"
                                    :rules="[v => !!v || 'Username is required']"
                                    name="username"
                                    label="Username"
                                    placeholder="Username"
                                    type="text"
                                    class="my-2"
                                    required
                                ></v-text-field>

                                <v-text-field
                                    v-model="password"
                                    :rules="[v => !!v || 'Password is required']"
                                    name="password"
                                    label="Password"
                                    placeholder="Password"
                                    type="password"
                                    class="my-2"
                                    required
                                ></v-text-field>

                                <div class="d-flex mt-4">
                                    <v-btn type="submit" color="primary" :disabled="!loginFormIsValid">Login</v-btn>
                                    <div class="text-error align-content-center ml-4">{{loginFormErrorMessage}}</div>
                                </div>
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
            loginFormIsValid: false,
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
                this.loginFormErrorMessage = 'Login failed';
            } finally {
                this.username = '';
                this.password = '';
            }
        },
    }
}
</script>
