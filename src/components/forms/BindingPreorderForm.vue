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
        <v-card-title v-if="!isEdit">New Pre-Order</v-card-title>
        <v-card-title v-if="isEdit">Edit Pre-Order</v-card-title>
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
                <ServerItemSelector
                    ref="userSelector"
                    :fetch-function="usersStore.fetchUsersPage"
                    :prefetch="false"
                    label="User"
                    icon="mdi-account"
                    item-title-key="pretty_name"
                    item-value-key="id"
                    :autofocus="false"
                    :no-filter="true"
                    :initial-selection="data.user"
                    @update:selection="data.user = $event"
                ></ServerItemSelector>
                <v-radio-group
                    v-model="data.type"
                    :rules="rules.type"
                    inline
                >
                    <v-radio
                        v-for="type in [...ItemType.getAll(), {key: 'Other', label: 'Other', icon: 'mdi-help'}]"
                        :key="type.key"
                        :value="type.key"
                        color="primary"
                        class="mr-2"
                    >
                        <template v-slot:label>
                            <span :class="data.type === type.key ? 'text-primary' : ''">
                                <v-icon>{{ type.icon }}</v-icon>
                                {{ type.label }}
                            </span>
                        </template>
                    </v-radio>
                </v-radio-group>
                <v-text-field
                    v-model="data.title"
                    label="Title"
                    :rules="rules.title"
                    variant="outlined"
                    prepend-inner-icon="mdi-format-title"
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
import {ItemType} from "@/types/ItemType";
</script>

<script lang="ts">
import {defineComponent} from 'vue'
import {useUsersStore} from "@/store/users";

const usersStore = useUsersStore();

export default defineComponent({
    name: "BindingPreorderForm",

    components: {ServerItemSelector},

    emits: ['submit', 'abort'],

    props: {
        item: {type: Object, required: false, default: null},
    },

    data() {
        return {
            isValid: false,
            data: {
                id: null,
                user: null,
                type: null,
                title: '',
            },
            rules: {
                user: [
                    (v: any) => !!v || 'User is required',
                    (v: any) => (/^[0-9]+/.test(v.id)) || 'User is invalid',
                ],
                type: [
                    (v: any) => !!v || 'Type is required',
                ],
                title: [
                    (v: string) => !!v || 'Title is required',
                    (v: string) => (v.length <= 128) || 'Title must be less or equal than 128 characters',
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
                        user: item.user,
                        type: item.type,
                        title: item.title ?? '',
                    }
                } else {
                    this.data = {
                        id: null,
                        user: null,
                        type: null,
                        title: '',
                    }
                }
            }
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