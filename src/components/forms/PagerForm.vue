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
        <v-card-title v-if="!isEdit">New Pager</v-card-title>
        <v-card-title v-if="isEdit">Edit Pager</v-card-title>
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
                    ref="templateSelector"
                    :fetch-function="itemsStore.fetchPagerTemplatesPage"
                    :prefetch="true"
                    label="Pager Template"
                    icon="mdi-bell-ring-outline"
                    item-title-key="pretty_name"
                    item-value-key="id"
                    :autofocus="false"
                    :no-filter="true"
                    :initial-selection="data.template"
                    @update:selection="data.template = $event"
                ></ServerItemSelector>
                <v-text-field
                    v-model="data.serialnumber"
                    label="Serialnumber"
                    :rules="rules.serialnumber"
                    variant="outlined"
                    prepend-inner-icon="mdi-tag"
                ></v-text-field>
                <v-text-field
                    v-model="data.notes"
                    label="Notes"
                    :rules="rules.notes"
                    variant="outlined"
                    prepend-inner-icon="mdi-pencil"
                ></v-text-field>
                <v-switch
                    v-model="data.has_coordinates"
                    color="primary"
                >
                    <template v-slot:prepend>
                            <span class="text-grey-darken-2">
                                <v-icon>mdi-map-marker</v-icon>
                                &nbsp;
                                Show on Deployment Map
                            </span>
                    </template>
                </v-switch>
                <div v-if="data.has_coordinates" class="d-inline-flex mt-n3 ga-3 align-center">
                    <v-select
                        v-model="data.coordinates.floor"
                        :items="[0, 1, 2, 3, 4].map(i => ({title: `Floor ${i}`, value: i}))"
                        :rules="rules.coordinates_floor"
                        variant="outlined"
                        density="comfortable"
                        label="Floor"
                        prepend-icon="mdi-stairs"
                    ></v-select>
                    <v-text-field
                        v-model="data.coordinates.latitude"
                        :rules="rules.coordinates_latitude"
                        variant="outlined"
                        density="comfortable"
                        label="Latitude"
                        prepend-icon="mdi-latitude"
                        width="120"
                    ></v-text-field>
                    <v-text-field
                        v-model="data.coordinates.longitude"
                        :rules="rules.coordinates_longitude"
                        variant="outlined"
                        density="comfortable"
                        label="Longitude"
                        prepend-icon="mdi-longitude"
                        width="120"
                    ></v-text-field>
                </div>

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

const itemsStore = useItemsStore();

export default defineComponent({
    name: "PagerForm",

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
                template: null as any,
                serialnumber: '',
                notes: '',
                has_coordinates: false,
                coordinates: {
                    floor: 0,
                    latitude: null,
                    longitude: null,
                }
            },
            rules: {
                template: [
                    (v: any) => !!v || 'Template is required',
                    (v: any) => (/^[0-9]+/.test(v.id)) || 'Template is invalid',
                ],
                serialnumber: [
                    (v: string) => (v.length <= 128) || 'Serialnumber must be less than 128 characters',
                ],
                notes: [
                    (v: string) => (v.length <= 256) || 'Notes must be less than 256 characters',
                ],
                coordinates_floor: [
                    (v: number) => (v >= 0 && v <= 4) || 'Floor must be between 0 and 4',
                ],
                coordinates_latitude: [
                    (v: number) => (v >= 0 && v <= 100) || 'Latitude must be between 0 and 100',
                ],
                coordinates_longitude: [
                    (v: number) => (v >= 0 && v <= 100) || 'Longitude must be between 0 and 100',
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
                        template: null,
                        serialnumber: '',
                        notes: '',
                        has_coordinates: false,
                        coordinates: {
                            floor: 0,
                            latitude: null,
                            longitude: null,
                        }
                    };
                } else {
                    this.data = {
                        id: item.id,
                        template: item.template,
                        serialnumber: item.serialnumber ?? '',
                        notes: item.notes ?? '',
                        has_coordinates: !!item.coordinates,
                        coordinates: item.coordinates ?? {
                            floor: 0,
                            latitude: null,
                            longitude: null,
                        }
                    };
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
