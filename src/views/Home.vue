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
    <v-container class="fill-height">
        <v-responsive class="align-center text-center fill-height">
            <v-img height="480" src="@/assets/logo-brand.svg"/>

            <div class="py-10"/>

            <v-row class="d-flex align-center justify-center">
                <v-col cols="auto">
                    <v-btn
                        :href="radioHandoutUrl"
                        target="_blank"
                        :min-width="buttonWidth"
                        size="x-large"
                        color="info"
                    >
                        <v-icon
                            icon="mdi-chat-question-outline"
                            size="large"
                            start
                        />
                        Radio usage guide
                    </v-btn>
                </v-col>
            </v-row>
            <v-row class="d-flex align-center justify-center">
                <v-col cols="auto">
                    <v-btn
                        to="/login"
                        :min-width="buttonWidth"
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

<script setup>
const buttonWidth = 320;
const radioHandoutUrl = new URL('@/assets/radio-handout.pdf', import.meta.url).href;
</script>
