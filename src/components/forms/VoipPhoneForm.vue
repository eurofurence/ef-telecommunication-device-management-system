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
        <v-card-title v-if="!isEdit">New VoIP Phone</v-card-title>
        <v-card-title v-if="isEdit">Edit VoIP Phone</v-card-title>
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
                    :fetch-function="itemsStore.fetchPhoneTemplatesPage"
                    :prefetch="true"
                    label="Phone Template"
                    icon="mdi-phone"
                    item-title-key="pretty_name"
                    item-value-key="id"
                    :autofocus="false"
                    :no-filter="true"
                    :initial-selection="data.template"
                    @update:selection="data.template = $event"
                ></ServerItemSelector>
                <v-text-field
                    v-model="data.extension"
                    label="Extension"
                    :rules="rules.extension"
                    variant="outlined"
                    prepend-inner-icon="mdi-dialpad"
                ></v-text-field>
                <div class="d-inline-flex align-center">
                    <v-radio-group
                        v-model="data.network"
                        :rules="rules.network"
                        inline
                    >
                        <template v-slot:prepend>
                        <span class="text-grey-darken-2">
                           <v-icon>mdi-network-outline</v-icon>
                            &nbsp;
                            Network
                        </span>
                        </template>
                        <v-radio label="Staff" value="STAFF"/>
                        <v-radio label="Security" value="SECU"/>
                    </v-radio-group>
                    <v-switch
                        v-model="data.dhcp"
                        label="DHCP"
                        color="primary"
                        class="ml-3"
                    >
                        <template v-slot:label>
                            <v-icon>mdi-ethernet-cable</v-icon>
                            &nbsp;
                            DHCP
                        </template>
                    </v-switch>
                </div>
                <v-text-field
                    v-model="data.ip_address"
                    label="IP Address"
                    :rules="rules.ip_address"
                    variant="outlined"
                    prepend-inner-icon="mdi-ip-outline"
                ></v-text-field>
                <v-text-field
                    v-model="data.mac_address"
                    label="MAC Address"
                    :rules="rules.mac_address"
                    variant="outlined"
                    prepend-inner-icon="mdi-ethernet"
                ></v-text-field>
                <v-text-field
                    v-model="data.location"
                    label="Location"
                    :rules="rules.location"
                    variant="outlined"
                    prepend-inner-icon="mdi-map-marker"
                ></v-text-field>
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
    name: "VoipPhoneForm",

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
                extension: null,
                network: null,
                dhcp: false,
                ip_address: '',
                mac_address: '',
                location: '',
                serialnumber: '',
                notes: '',
            },
            rules: {
                template: [
                    (v: any) => !!v || 'Template is required',
                    (v: any) => (/^[0-9]+/.test(v.id)) || 'Template is invalid',
                ],
                extension: [
                    (v: string) => !!v || 'Extension is required',
                    (v: string) => (/^[0-9]*/.test(v)) || 'Extension must be numeric',
                    (v: string) => (v.length <= 32) || 'Extension must be less or equal than 32 characters',
                ],
                network: [
                    (v: string) => !!v || 'Network is required',
                    (v: string) => (v == 'STAFF' || v == 'SECU') || 'Network is invalid',
                ],
                ip_address: [
                    (v: string) => (v.length <= 45) || 'IP Address must be less than 45 characters',
                ],
                mac_address: [
                    (v: string) => (v.length <= 17) || 'MAC Address must be less than 17 characters',
                ],
                location: [
                    (v: string) => (v.length <= 128) || 'Location must be less than 128 characters',
                ],
                serialnumber: [
                    (v: string) => (v.length <= 128) || 'Serialnumber must be less than 128 characters',
                ],
                notes: [
                    (v: string) => (v.length <= 256) || 'Notes must be less than 256 characters',
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
                        extension: null,
                        network: null,
                        dhcp: false,
                        ip_address: '',
                        mac_address: '',
                        location: '',
                        serialnumber: '',
                        notes: '',
                    };
                } else {
                    this.data = {
                        id: item.id,
                        template: item.template,
                        extension: item.extension,
                        network: item.network,
                        dhcp: item.dhcp,
                        ip_address: item.ip_address ?? '',
                        mac_address: item.mac_address ?? '',
                        location: item.location ?? '',
                        serialnumber: item.serialnumber ?? '',
                        notes: item.notes ?? '',
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
