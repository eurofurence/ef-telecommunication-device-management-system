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
    <v-container>
        <v-row>
            <v-col>
                <h1>VoIP Phone Provisioning</h1>
                <div v-if="provisionMetadata">
                    <v-container>
                        <v-row>
                            <v-col cols="12" lg="6" class="pa-0 pa-lg-3">
                                <v-card
                                    title="Phone Configurations"
                                    prepend-icon="mdi-file-code-outline"
                                    class="mb-4"
                                >
                                    <v-list>
                                        <v-list-item
                                            v-for="cfg in provisionMetadata.config"
                                            :title="`${cfg.accountname} (${FormatUtils.formatMacAddress(cfg.mac)})`"
                                            :subtitle="`${cfg.filename} (${FormatUtils.bytesToHumanReadableString(cfg.filesize)})`"
                                            class="mb-1"
                                        >
                                            <template v-slot:append>
                                                <v-btn
                                                    color="primary"
                                                    @click="showPhoneConfig(cfg.mac)"
                                                    density="comfortable"
                                                    variant="text"
                                                    icon
                                                >
                                                    <v-icon>mdi-magnify</v-icon>
                                                    <v-tooltip activator="parent">
                                                        View
                                                    </v-tooltip>
                                                </v-btn>
                                                <v-btn
                                                    color="primary"
                                                    @click="console.error('Yoink!')"
                                                    density="comfortable"
                                                    variant="text"
                                                    icon
                                                >
                                                    <v-icon>mdi-gesture-tap-button</v-icon>
                                                    <v-tooltip activator="parent">
                                                        Multi-Purpose-Keys (MPKs)
                                                    </v-tooltip>
                                                </v-btn>
                                                <v-btn
                                                    color="primary"
                                                    @click="console.error('Yoink!')"
                                                    density="comfortable"
                                                    variant="text"
                                                    icon
                                                >
                                                    <v-icon>mdi-download</v-icon>
                                                    <v-tooltip activator="parent">
                                                        Download
                                                    </v-tooltip>
                                                </v-btn>
                                            </template>
                                        </v-list-item>
                                    </v-list>
                                </v-card>
                            </v-col>
                            <v-col cols="12" lg="6" class="pa-0 pa-lg-3">
                                <v-card
                                    title="Firmware Files"
                                    prepend-icon="mdi-file-cog-outline"
                                    class="mb-4"
                                >
                                    <v-list>
                                        <v-list-item
                                            v-for="fw in provisionMetadata.firmware"
                                            :title="`${fw.filename}`"
                                            :subtitle="`${FormatUtils.bytesToHumanReadableString(fw.filesize)}`"
                                            class="mb-1"
                                        >
                                            <template v-slot:append>
                                                <v-btn
                                                    color="primary"
                                                    @click="console.error('Yoink!')"
                                                    density="comfortable"
                                                    variant="text"
                                                    icon
                                                >
                                                    <v-icon>mdi-download</v-icon>
                                                    <v-tooltip activator="parent">
                                                        Download
                                                    </v-tooltip>
                                                </v-btn>
                                            </template>
                                        </v-list-item>
                                    </v-list>
                                </v-card>

                                <v-card
                                    title="Phonebooks"
                                    prepend-icon="mdi-notebook-outline"
                                    class="mb-4"
                                >
                                    <v-list>
                                        <v-list-item
                                            v-for="pb in provisionMetadata.phonebook"
                                            :title="`${pb.filename}`"
                                            :subtitle="`${pb.entries.length} entries (${FormatUtils.bytesToHumanReadableString(pb.filesize)})`"
                                            class="mb-1"
                                        >
                                            <template v-slot:append>
                                                <v-btn
                                                    color="primary"
                                                    @click="console.error('Yoink!')"
                                                    density="comfortable"
                                                    variant="text"
                                                    icon
                                                >
                                                    <v-icon>mdi-magnify</v-icon>
                                                    <v-tooltip activator="parent">
                                                        View
                                                    </v-tooltip>
                                                </v-btn>
                                                <v-btn
                                                    color="primary"
                                                    @click="console.error('Yoink!')"
                                                    density="comfortable"
                                                    variant="text"
                                                    icon
                                                >
                                                    <v-icon>mdi-card-account-details-outline</v-icon>
                                                    <v-tooltip activator="parent">
                                                        Entries
                                                    </v-tooltip>
                                                </v-btn>
                                                <v-btn
                                                    color="primary"
                                                    @click="console.error('Yoink!')"
                                                    density="comfortable"
                                                    variant="text"
                                                    icon
                                                >
                                                    <v-icon>mdi-download</v-icon>
                                                    <v-tooltip activator="parent">
                                                        Download
                                                    </v-tooltip>
                                                </v-btn>
                                            </template>
                                        </v-list-item>
                                    </v-list>
                                </v-card>

                                <v-card
                                    title="Wallpapers"
                                    prepend-icon="mdi-wallpaper"
                                    class="mb-4"
                                >
                                    <v-list>
                                        <v-list-item
                                            v-if="provisionMetadata.wallpaper"
                                            :title="`${provisionMetadata.wallpaper.filename}`"
                                            :subtitle="`${FormatUtils.bytesToHumanReadableString(provisionMetadata.wallpaper.filesize)}`"
                                            class="mb-1"
                                        >
                                            <template v-slot:append>
                                                <v-btn
                                                    color="primary"
                                                    @click="console.error('Yoink!')"
                                                    density="comfortable"
                                                    variant="text"
                                                    icon
                                                >
                                                    <v-icon>mdi-magnify</v-icon>
                                                    <v-tooltip activator="parent">
                                                        View
                                                    </v-tooltip>
                                                </v-btn>
                                                <v-btn
                                                    color="primary"
                                                    @click="console.error('Yoink!')"
                                                    density="comfortable"
                                                    variant="text"
                                                    icon
                                                >
                                                    <v-icon>mdi-download</v-icon>
                                                    <v-tooltip activator="parent">
                                                        Download
                                                    </v-tooltip>
                                                </v-btn>
                                            </template>
                                        </v-list-item>
                                        <v-list-item
                                            v-if="!provisionMetadata.wallpaper"
                                            title="No wallpaper found"
                                        ></v-list-item>
                                    </v-list>
                                </v-card>

                            </v-col>
                        </v-row>
                    </v-container>
                </div>
            </v-col>
        </v-row>
    </v-container>
</template>

<script lang="ts" setup>
import {FormatUtils} from "@/classes/util/FormatUtils";
</script>

<script lang="ts">
import {defineComponent} from "vue";
import {useProvisionStore} from "@/store/provision";
import {ProvisionMetadata} from "@/types/ProvisionMetadata";

const provisionStore = useProvisionStore();

export default defineComponent({
    name: "VoipProvisioning",

    data() {
        return {
            loading: true,
            provisionMetadata: null as ProvisionMetadata | null,
        }
    },

    mounted() {
        provisionStore.fetchProvisionMetadata().then((resp) => {
            this.loading = false;

            // Sort data structures
            resp.data.config.sort((a: any, b: any) => a.extension - b.extension);
            resp.data.firmware.sort((a: any, b: any) => a.filename.localeCompare(b.filename));
            resp.data.phonebook.sort((a: any, b: any) => a.filename.localeCompare(b.filename));

            this.provisionMetadata = resp.data;
        });
    },

    methods: {
        showPhoneConfig(mac: string) {
            console.log(`Downloading phone config for MAC ${mac}`);
            provisionStore.fetchPhoneConfig(mac).then((resp) => {
                console.log(resp);
            });
        }
    }
})
</script>