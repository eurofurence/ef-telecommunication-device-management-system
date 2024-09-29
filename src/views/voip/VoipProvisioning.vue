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
                                                    @click="showPhoneConfig(cfg.mac, cfg.accountname)"
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
                                                    @click="showMpksDialog(cfg.mpk, cfg.accountname, cfg.mac)"
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
                                        <v-list-item
                                            v-if="provisionMetadata.config.length === 0"
                                            title="No phone configurations found"
                                            class="mb-1"
                                            disabled
                                        ></v-list-item>
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
                                        <v-list-item
                                            v-if="provisionMetadata.firmware.length === 0"
                                            title="No firmware files found"
                                            class="mb-1"
                                            disabled
                                        ></v-list-item>
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
                                                    @click="showPhonebook(pb.filename.split('.')[0])"
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
                                                    @click="showPhonebookEntriesDialog(pb.entries, pb.filename)"
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
                                        <v-list-item
                                            v-if="provisionMetadata.phonebook.length === 0"
                                            title="No phonebooks found"
                                            class="mb-1"
                                            disabled
                                        ></v-list-item>
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
                                                    @click="showWallpaper"
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
                                            class="mb-1"
                                            disabled
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

    <v-dialog
        v-model="xmlInspectionDialog.show"
        max-width="1200"
    >
        <template v-slot:default="{ isActive }">
            <v-card
                :title="xmlInspectionDialog.title"
                :subtitle="xmlInspectionDialog.subtitle"
            >
                <template v-slot:append>
                    <v-btn
                        @click="xmlInspectionDialog.show = false"
                        icon="mdi-close"
                        variant="elevated"
                        elevation="3"
                        class="position-fixed mt-n16"
                        style="z-index: 999;"
                    ></v-btn>
                </template>

                <v-card-text>
                    <div v-if="xmlInspectionDialog.loading" class="d-flex justify-center">
                        <v-progress-circular
                            indeterminate
                            color="muted"
                            size="64"
                            class="ma-5"
                        ></v-progress-circular>
                    </div>

                    <div v-if="!xmlInspectionDialog.loading">
                        <highlightjs language="xml" :code="xmlInspectionDialog.xml"></highlightjs>
                    </div>
                </v-card-text>
            </v-card>
        </template>
    </v-dialog>

    <v-dialog
        v-model="wallpaperInspectionDialog.show"
        max-width="480"
    >
        <template v-slot:default="{ isActive }">
            <v-card
                :title="wallpaperInspectionDialog.title"
                :subtitle="wallpaperInspectionDialog.subtitle"
            >
                <template v-slot:append>
                    <v-btn
                        @click="wallpaperInspectionDialog.show = false"
                        icon="mdi-close"
                        variant="elevated"
                        elevation="3"
                        class="position-fixed mt-n16"
                        style="z-index: 999;"
                    ></v-btn>
                </template>

                <v-card-text>
                    <div v-if="wallpaperInspectionDialog.loading" class="d-flex justify-center">
                        <v-progress-circular
                            indeterminate
                            color="muted"
                            size="64"
                            class="ma-5"
                        ></v-progress-circular>
                    </div>

                    <div v-if="!wallpaperInspectionDialog.loading">
                        <img :src="`data:image/jpg;base64,${wallpaperInspectionDialog.wallpaperBase64}`"></img>
                    </div>
                </v-card-text>
            </v-card>
        </template>
    </v-dialog>

    <v-dialog
        v-model="phoneMpksDialog.show"
        max-width="480"
    >
        <template v-slot:default="{ isActive }">
            <v-card
                :title="phoneMpksDialog.title"
                :subtitle="phoneMpksDialog.subtitle"
            >
                <template v-slot:append>
                    <v-btn
                        @click="phoneMpksDialog.show = false"
                        icon="mdi-close"
                        variant="elevated"
                        elevation="3"
                        class="position-fixed mt-n16"
                        style="z-index: 999;"
                    ></v-btn>
                </template>

                <v-card-text>
                    <v-list>
                        <v-list-item
                            v-for="(mpk, idx) in phoneMpksDialog.mpks"
                            :title="`[MPK ${idx}] ${mpk.keyMode}: ${mpk.value} (${mpk.description})`"
                            :subtitle="`Account ${mpk.account}`"
                            class="mb-1"
                        ></v-list-item>
                    </v-list>
                </v-card-text>
            </v-card>
        </template>
    </v-dialog>

    <v-dialog
        v-model="phonebookEntriesDialog.show"
        max-width="480"
    >
        <template v-slot:default="{ isActive }">
            <v-card
                :title="phonebookEntriesDialog.title"
                :subtitle="phonebookEntriesDialog.subtitle"
            >
                <template v-slot:append>
                    <v-btn
                        @click="phonebookEntriesDialog.show = false"
                        icon="mdi-close"
                        variant="elevated"
                        elevation="3"
                        class="position-fixed mt-n16"
                        style="z-index: 999;"
                    ></v-btn>
                </template>

                <v-card-text>
                    <v-list>
                        <v-list-item
                            v-for="entry in phonebookEntriesDialog.entries"
                            :title="`${entry.firstname} ${entry.lastname ?? ''}`"
                            :subtitle="entry.phone"
                            class="mb-1"
                        ></v-list-item>
                    </v-list>
                </v-card-text>
            </v-card>
        </template>
    </v-dialog>

</template>

<script lang="ts" setup>
import {FormatUtils} from "@/classes/util/FormatUtils";
</script>

<script lang="ts">
import {defineComponent} from "vue";
import {useProvisionStore} from "@/store/provision";
import {ProvisionMetadata} from "@/types/ProvisionMetadata";
import {FormatUtils} from "@/classes/util/FormatUtils";

const provisionStore = useProvisionStore();

export default defineComponent({
    name: "VoipProvisioning",

    data() {
        return {
            loading: true,
            provisionMetadata: null as ProvisionMetadata | null,
            xmlInspectionDialog: {
                show: false,
                loading: true,
                title: "",
                subtitle: "",
                xml: ""
            },
            wallpaperInspectionDialog: {
                show: false,
                loading: true,
                title: "",
                subtitle: "",
                wallpaperBase64: ""
            },
            phoneMpksDialog: {
                show: false,
                title: "",
                subtitle: "",
                mpks: [] as any
            },
            phonebookEntriesDialog: {
                show: false,
                title: "",
                subtitle: "",
                entries: [] as any
            }
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
        showPhoneConfig(mac: string, accountname: string) {
            this.xmlInspectionDialog.title = `Phone config file: ${accountname}`;
            this.xmlInspectionDialog.subtitle = `MAC: ${FormatUtils.formatMacAddress(mac)}`;
            this.xmlInspectionDialog.loading = true;
            this.xmlInspectionDialog.show = true;

            provisionStore.fetchPhoneConfig(mac).then((resp) => {
                this.xmlInspectionDialog.xml = resp.data;
                this.xmlInspectionDialog.loading = false;
            });
        },

        showPhonebook(name: string) {
            this.xmlInspectionDialog.title = `Phonebook: ${name}`;
            this.xmlInspectionDialog.subtitle = '';
            this.xmlInspectionDialog.loading = true;
            this.xmlInspectionDialog.show = true;

            provisionStore.fetchPhonebook(name).then((resp) => {
                this.xmlInspectionDialog.xml = resp.data;
                this.xmlInspectionDialog.loading = false;
            });
        },

        showWallpaper() {
            this.wallpaperInspectionDialog.title = `Wallpaper`;
            this.wallpaperInspectionDialog.subtitle = 'File: wallpaper.jpg';
            this.wallpaperInspectionDialog.loading = true;
            this.wallpaperInspectionDialog.show = true;

            provisionStore.fetchWallpaper().then((resp) => {
                this.wallpaperInspectionDialog.wallpaperBase64 = resp.data;
                this.wallpaperInspectionDialog.loading = false;
            });
        },

        showMpksDialog(mpks: any, accountname: string, mac: string) {
            this.phoneMpksDialog.title = 'Multi-Purpose-Keys (MPKs)';
            this.phoneMpksDialog.subtitle = `${accountname} (${FormatUtils.formatMacAddress(mac)})`;
            this.phoneMpksDialog.mpks = mpks;
            this.phoneMpksDialog.show = true;
        },

        showPhonebookEntriesDialog(entries: any, filename: string) {
            this.phonebookEntriesDialog.title = 'Phonebook Entries';
            this.phonebookEntriesDialog.subtitle = `Phonebook: ${filename}`;
            this.phonebookEntriesDialog.entries = entries;
            this.phonebookEntriesDialog.show = true;
        }
    }
})
</script>