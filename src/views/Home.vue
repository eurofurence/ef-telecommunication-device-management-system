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
                        :min-width="buttonWidth"
                        size="x-large"
                        color="primary"
                        @click="dialogOnSiteInfo = true"
                    >
                        <v-icon
                            icon="mdi-office-building-marker-outline"
                            size="large"
                            start
                        />
                        On-site service info
                    </v-btn>
                    <v-dialog
                        v-model="dialogOnSiteInfo"
                        width="auto"
                        max-width="800"
                    >
                        <v-card
                            prepend-icon="mdi-office-building-marker-outline"
                            title="On-Site Service Information"
                            subtitle="Radio Desk Service, Device Handout and Returns, Battery Replacement, ..."
                        >
                            <v-card-text>
                                <v-container>
                                    <v-row>
                                        <v-col>
                                            <h3>Radio Desk</h3>
                                            <p>
                                                You can find us at the radio desk, located at:
                                            </p>
                                            <v-list>
                                                <v-list-item
                                                    title="Room 031, Ground Floor"
                                                    subtitle="Tuesday (17.09.24)"
                                                >
                                                    <template v-slot:prepend>
                                                        <v-btn
                                                            color="primary"
                                                            icon="mdi-map-marker"
                                                            density="comfortable"
                                                            class="mr-4"
                                                        ></v-btn>
                                                    </template>
                                                </v-list-item>
                                                <v-list-item
                                                    title="Room 201, Second Floor"
                                                    subtitle="Wednesday (18.09.24) to Sunday (22.09.24)"
                                                >
                                                    <template v-slot:prepend>
                                                        <v-btn
                                                            color="primary"
                                                            icon="mdi-map-marker"
                                                            density="comfortable"
                                                            class="mr-4"
                                                        ></v-btn>
                                                    </template>
                                                </v-list-item>
                                            </v-list>
                                        </v-col>
                                    </v-row>
                                    <v-row>
                                        <v-col>
                                            <h3>Staff Radio Training</h3>
                                            <p>
                                                You are unsure how to use your radio? No problem! We offer hands-on
                                                radio training sessions during the convention. If you are interested,
                                                simply show up at one of the following events or ask a staff member at
                                                any time.
                                            </p>
                                            <v-list slim>
                                                <v-list-item
                                                    title="Radio Training Session 1"
                                                    subtitle="Tuesday (17.09.24) 17:00, CCH Foyer 4"
                                                    prepend-icon="mdi-radio-handheld"
                                                ></v-list-item>
                                                <v-list-item
                                                    title="Radio Training Session 2"
                                                    subtitle="Wednesday (18.09.24) 14:00, CCH Y 7-8"
                                                    prepend-icon="mdi-radio-handheld"
                                                ></v-list-item>
                                            </v-list>
                                        </v-col>
                                    </v-row>
                                    <v-row>
                                        <v-col>
                                            <h3>Radio Handout and Service</h3>
                                            <p>
                                                Want to pick up your radio, experience a problem or have a question?
                                                Visit our radio desk during the times listed below. If you need help
                                                outside of these times, use the support station at the radio desk or
                                                contact us directly via <a :href="telegramContactUrl" target="_blank">Telegram</a>.
                                            </p>
                                            <v-list slim>
                                                <v-list-subheader>Tuesday (17.09.24), Room 031</v-list-subheader>
                                                <v-list-item title="16:00 - 17:00" prepend-icon="mdi-chevron-right" class="ml-3"></v-list-item>
                                                <v-list-item title="18:00 - 20:00" prepend-icon="mdi-chevron-right" class="ml-3"></v-list-item>

                                                <v-divider></v-divider>

                                                <v-list-subheader>Tuesday (17.09.24), Room 201</v-list-subheader>
                                                <v-list-item title="13:00 - 14:00" prepend-icon="mdi-chevron-right" class="ml-3"></v-list-item>
                                                <v-list-item title="15:00 - 16:00" prepend-icon="mdi-chevron-right" class="ml-3"></v-list-item>
                                                <v-list-item title="19:00 - 20:00" prepend-icon="mdi-chevron-right" class="ml-3"></v-list-item>
                                            </v-list>
                                        </v-col>
                                    </v-row>
                                    <v-row>
                                        <v-col>
                                            <h3>Radio Returns</h3>
                                            <p>
                                                Please return your radio at the radio desk <b>no later than Sunday
                                                (22.09.24) 11:00</b>. Belated returns may result in additional costs
                                                for shipping and compensation beverages.
                                            </p>
                                            <p>
                                                You can already return your radio on Saturday to avoid having to get up
                                                early on Sunday.
                                            </p>
                                            <p>
                                                Radio return is possible during the following times:
                                            </p>
                                            <v-list slim>
                                                <v-list-subheader>Saturday (21.09.24), Room 201</v-list-subheader>
                                                <v-list-item title="15:00 - 16:00" prepend-icon="mdi-chevron-right" class="ml-3"></v-list-item>
                                                <v-list-item title="21:00 - 22:00" prepend-icon="mdi-chevron-right" class="ml-3"></v-list-item>

                                                <v-divider></v-divider>

                                                <v-list-subheader>Sunday (22.09.24), Room 201</v-list-subheader>
                                                <v-list-item title="09:00 - 11:00" prepend-icon="mdi-chevron-right" class="ml-3"></v-list-item>
                                            </v-list>
                                        </v-col>
                                    </v-row>
                                    <v-row>
                                        <v-col>
                                            <h3>Replacement Batteries</h3>
                                            <p>
                                                Just need a quick recharge? You can find freshly <b>charged batteries
                                                inside the staff lounge</b>. Pick a fully charged one, replace your
                                                depleted battery with it, and place the empty battery in the charger.
                                                Done!
                                            </p>
                                            <p>
                                                If you need help, ask a fellow staff member or approach us at the radio desk.
                                            </p>
                                        </v-col>
                                    </v-row>
                                </v-container>
                            </v-card-text>

                            <template v-slot:actions>
                                <v-btn
                                    class="ms-auto"
                                    text="Close"
                                    @click="dialogOnSiteInfo = false"
                                ></v-btn>
                            </template>
                        </v-card>
                    </v-dialog>
                </v-col>
            </v-row>

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
                            icon="mdi-radio-handheld"
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
                        :href="telegramContactUrl"
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
                        Support chat
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
import { ref } from 'vue';

const buttonWidth = 320;
const radioHandoutUrl = new URL('@/assets/radio-handout.pdf', import.meta.url).href;
const telegramContactUrl = new URL('https://t.me/EFTelecom').href;

const dialogOnSiteInfo = ref(false);
</script>
