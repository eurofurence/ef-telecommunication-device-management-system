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
        <v-card-title v-if="!isEdit">New Item Owner</v-card-title>
        <v-card-title v-if="isEdit">Edit Item Owner</v-card-title>
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
                    v-model="data.shortname"
                    label="Shortname"
                    :rules="rules.shortname"
                    variant="outlined"
                    prepend-inner-icon="mdi-label"
                ></v-text-field>

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
    name: "ItemOwnerForm",

    emits: ['submit', 'abort'],

    props: {
        item: {type: Object, required: false, default: null},
    },

    data() {
        return {
            isValid: false,
            data: {
                id: null,
                name: '',
                shortname: '',
            },
            rules: {
                name: [
                    (v: string) => !!v || 'Name is required',
                    (v: string) => (v && v.length <= 128) || 'Name must be less than 128 characters',
                    (v: string) => (v && v.length >= 2) || 'Name must be at least 2 characters',
                ],
                shortname: [
                    (v: string) => !!v || 'Shortname is required',
                    (v: string) => (v && v.length <= 16) || 'Shortname must be less than 32 characters',
                    (v: string) => (v && v.length >= 2) || 'Shortname must be at least 2 characters',
                ],
            },
        }
    },

    watch: {
        item: {
            immediate: true,
            handler(item) {
                if (item !== null) {
                    this.data = {
                        id: item.id,
                        name: item.name,
                        shortname: item.shortname,
                    }
                } else {
                    this.data = {
                        id: null,
                        name: '',
                        shortname: '',
                    }
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