<template>
    <v-card>
        <v-card-title v-if="!isEdit">New Callbox</v-card-title>
        <v-card-title v-if="isEdit">Edit Callbox</v-card-title>
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
                    :fetch-function="itemsStore.fetchCallboxTemplatesPage"
                    :prefetch="true"
                    label="Callbox Template"
                    icon="mdi-webcam"
                    item-title-key="pretty_name"
                    item-value-key="id"
                    :autofocus="false"
                    :no-filter="true"
                    @update:selection="data.template = $event.id"
                ></ServerItemSelector>
                <v-text-field
                    v-model="data.extension"
                    label="Extension"
                    :rules="rules.extension"
                    variant="outlined"
                    prepend-inner-icon="mdi-dialpad"
                ></v-text-field>
                <div class="d-inline-flex align-center mx-2">
                    <v-radio-group
                        v-model="data.network"
                        :rules="rules.network"
                        inline
                    >
                        <template v-slot:prepend>
                        <span class="text-grey-darken-2">
                           <v-icon>mdi-network-outline</v-icon>
                            &nbsp;
                            Phone Network
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
                    label="Phone IP Address"
                    :rules="rules.ip_address"
                    variant="outlined"
                    prepend-inner-icon="mdi-ip-outline"
                ></v-text-field>
                <v-text-field
                    v-model="data.mac_address"
                    label="Phone MAC Address"
                    :rules="rules.mac_address"
                    variant="outlined"
                    prepend-inner-icon="mdi-ethernet"
                ></v-text-field>
                <v-switch
                    v-model="data.has_camera"
                    color="primary"
                    class="ml-3"
                    hide-details
                    density="compact"
                >
                    <template v-slot:label>
                        <v-icon>mdi-cctv</v-icon>
                        &nbsp;
                        Has Camera
                    </template>
                </v-switch>
                <div class="d-inline-flex align-center mx-2">
                    <v-radio-group
                        v-model="data.camera_network"
                        v-show="data.has_camera"
                        :rules="rules.camera_network"
                        inline
                    >
                        <template v-slot:prepend>
                        <span class="text-grey-darken-2">
                           <v-icon>mdi-network-outline</v-icon>
                            &nbsp;
                            Camera Network
                        </span>
                        </template>
                        <v-radio label="Staff" value="STAFF"/>
                        <v-radio label="Security" value="SECU"/>
                    </v-radio-group>
                    <v-switch
                        v-model="data.camera_dhcp"
                        v-show="data.has_camera"
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
                    v-model="data.camera_ip_address"
                    v-show="data.has_camera"
                    label="Camera IP Address"
                    :rules="rules.camera_ip_address"
                    variant="outlined"
                    prepend-inner-icon="mdi-ip-outline"
                ></v-text-field>
                <v-text-field
                    v-model="data.camera_mac_address"
                    v-show="data.has_camera"
                    label="Camera MAC Address"
                    :rules="rules.camera_mac_address"
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
    name: "VoipCallboxForm",

    components: {ServerItemSelector},

    props: {
        item: {type: Object, required: false, default: null},
    },

    data() {
        return {
            isValid: false,
            data: {
                id: null,
                template: null,
                extension: null,
                network: null,
                dhcp: false,
                ip_address: '',
                mac_address: '',
                location: '',
                has_camera: false,
                camera_network: null,
                camera_dhcp: false,
                camera_ip_address: '',
                camera_mac_address: '',
                serialnumber: '',
                notes: '',
            },
            rules: {
                template: [
                    (v: any) => !!v || 'Template is required',
                    (v: string) => (/^[0-9]+/.test(v)) || 'Template is invalid',
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
                camera_network: [
                    (v: string|null) => (v === null || (v && (v == 'STAFF' || v == 'SECU'))) || 'Camera Network is invalid',
                ],
                camera_ip_address: [
                    (v: string) => (v.length <= 45) || 'Camera IP Address must be less than 45 characters',
                ],
                camera_mac_address: [
                    (v: string) => (v.length <= 17) || 'Camera MAC Address must be less than 17 characters',
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

    computed: {
        isEdit() {
            return this.item !== null;
        }
    },
});
</script>