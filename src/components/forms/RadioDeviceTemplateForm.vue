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
    <v-card>
        <v-card-title v-if="!isEdit">New Radio Device Template</v-card-title>
        <v-card-title v-if="isEdit">Edit Radio Device Template</v-card-title>
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
                    label="Template Name"
                    :rules="rules.name"
                    variant="outlined"
                    prepend-inner-icon="mdi-format-title"
                ></v-text-field>
                <ServerItemSelector
                    ref="ownerSelector"
                    :fetch-function="usersStore.fetchItemOwnersPage"
                    :prefetch="true"
                    label="Item Owner"
                    icon="mdi-account"
                    item-title-key="pretty_name"
                    item-value-key="id"
                    :autofocus="false"
                    :no-filter="true"
                    :initial-selection="data.owner"
                    @update:selection="data.owner = $event"
                ></ServerItemSelector>
                <v-switch
                    v-model="data.private"
                    label="Private Item"
                    color="primary"
                    prepend-icon="mdi-account-lock"
                ></v-switch>
                <ServerItemSelector
                    ref="codingSelector"
                    :fetch-function="itemsStore.fetchRadioCodingsPage"
                    :prefetch="true"
                    label="Radio Coding"
                    icon="mdi-sim"
                    item-title-key="name"
                    item-value-key="id"
                    :autofocus="false"
                    :no-filter="true"
                    :initial-selection="data.coding"
                    @update:selection="data.coding = $event"
                ></ServerItemSelector>
                <v-text-field
                    v-model="data.description"
                    label="Description"
                    :rules="rules.description"
                    variant="outlined"
                    prepend-inner-icon="mdi-pencil"
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

<script lang="ts" setup>
import ServerItemSelector from "@/components/ServerItemSelector.vue";
</script>

<script lang="ts">
import {defineComponent} from 'vue'
import {useItemsStore} from "@/store/items";
import {useUsersStore} from "@/store/users";

const itemsStore = useItemsStore();
const usersStore = useUsersStore();

export default defineComponent({
    name: "RadioDeviceTemplateForm",

    components: {ServerItemSelector},

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
                owner: null as any,
                private: false,
                coding: null as any,
                description: '',
            },
            rules: {
                name: [
                    (v: string) => !!v || 'Name is required',
                    (v: string) => (v.length <= 128) || 'Name must be less than 128 characters',
                ],
                owner: [
                    (v: any) => !!v || 'Owner is required',
                    (v: any) => (/^[0-9]+/.test(v.id)) || 'Owner is invalid',
                ],
                coding: [
                    (v: any) => !!v || 'Coding is required',
                    (v: any) => (/^[0-9]+/.test(v.id)) || 'Coding is invalid',
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
                        owner: null,
                        private: false,
                        coding: null,
                        description: '',
                    };
                } else {
                    this.data = {
                        id: item.id,
                        name: item.name,
                        owner: item.owner,
                        private: item.private,
                        coding: item.coding,
                        description: item.description ?? '',
                    };
                }
            },
        },
    },

    computed: {
        isEdit() {
            return this.item !== null;
        }
    },
});
</script>
