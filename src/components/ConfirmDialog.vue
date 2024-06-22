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
    <v-dialog>
        <v-card>
            <v-card-title v-if="title">{{ title }}</v-card-title>
            <v-card-text>
                <slot></slot>
            </v-card-text>
            <v-card-actions>
                <v-btn color="error" @click="$emit('abort')">Cancel</v-btn>
                <v-btn color="success" @click="$emit('confirm')">Confirm</v-btn>
            </v-card-actions>
        </v-card>
    </v-dialog>
</template>

<script lang="ts">
import {defineComponent} from 'vue'

export default defineComponent({
    name: "ConfirmDialog",
    emits: ['abort', 'confirm'],
    props: {
        title: {type: String, required: false},
    },
})
</script>

<style scoped>

</style>