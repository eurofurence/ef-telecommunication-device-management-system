<template>
    <v-container class="fill-height">
        <v-responsive class="align-center text-center fill-height">
            <v-img height="480" src="@/assets/logo-brand.svg"/>

            <div class="py-10"/>

            <v-row class="d-flex align-center justify-center">
                <v-col cols="auto">
                    <v-btn
                        to="/login"
                        min-width="228"
                        size="x-large"
                        color="#e20074"
                    >
                        <v-icon
                            icon="mdi-login"
                            size="large"
                            start
                        />
                        Login
                    </v-btn>
                </v-col>
            </v-row>
        </v-responsive>
    </v-container>
</template>
