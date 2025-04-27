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
    <v-card>
        <v-card-title v-if="!isEdit">New Radio Coding</v-card-title>
        <v-card-title v-if="isEdit">Edit Radio Coding</v-card-title>
        <v-divider></v-divider>

        <v-card-text>
            <v-form
                v-model="isValid"
                @submit.prevent
                class="mt-3"
            >
                <v-text-field
                    v-if="isEdit"
                    v-model="data.id"
                    label="ID"
                    type="number"
                    variant="outlined"
                    prepend-inner-icon="mdi-identifier"
                    disabled
                ></v-text-field>
                <v-text-field
                    v-model="data.name"
                    label="Name"
                    :rules="rules.name"
                    variant="outlined"
                    prepend-inner-icon="mdi-account"
                ></v-text-field>
                <v-text-field
                    v-model="data.description"
                    label="Description"
                    :rules="rules.description"
                    variant="outlined"
                    prepend-inner-icon="mdi-label"
                ></v-text-field>
                <v-input
                    v-model="data.color"
                    label="Color"
                    :rules="rules.color"
                    variant="outlined"
                    prepend-icon="mdi-palette"
                    class="text-grey-darken-2"
                >
                    <v-color-picker
                        v-model="data.color"
                        mode="hex"
                        :modes="['hex']"
                    ></v-color-picker>
                </v-input>


                <v-card-actions>
                    <v-btn
                        :disabled="!isValid"
                        color="success"
                        @click="$emit('submit', data)"
                    >
                        {{ isEdit ? 'Update' : 'Create' }}
                    </v-btn>
                    <v-btn
                        color="error"
                        @click="$emit('abort')"
                    >
                        Cancel
                    </v-btn>
                </v-card-actions>
            </v-form>
        </v-card-text>
    </v-card>
</template>

<script lang="ts">
import {defineComponent} from 'vue'

export default defineComponent({
    name: "RadioCodingForm",

    emits: ['abort', 'submit'],

    props: {
        item: {type: Object, required: false, default: null},
    },

    data() {
        return {
            isValid: false,
            data: {
                id: null,
                name: '',
                color: '',
                description: '',
            },
            rules: {
                name: [
                    (v: string) => !!v || 'Name is required',
                    (v: string) => (v && v.length <= 128) || 'Name must be less than 128 characters',
                    (v: string) => (v && v.length >= 2) || 'Name must be at least 2 characters',
                ],
                color: [
                    (v: string) => !!v || 'Color is required',
                    (v: string) => (v && /^#[0-9A-F]{6}$/i.test(v)) || 'Color must be a valid hex color (e.g. #FF0000)'
                ],
                description: [
                    (v: string) => (v.length <= 256) || 'Description must be less than 256 characters',
                ],
            },
        }
    },

    watch: {
        item: {
            immediate: true,
            handler(item) {
                if (item === null) {
                    this.data = {
                        id: null,
                        name: '',
                        color: '',
                        description: '',
                    };
                } else {
                    this.data = {
                        id: item.id,
                        name: item.name,
                        color: item.color,
                        description: item.description ?? '',
                    };
                }
            },
        }
    },

    computed: {
        isEdit() {
            return this.item !== null;
        }
    },
});
</script>

<style scoped>

</style>