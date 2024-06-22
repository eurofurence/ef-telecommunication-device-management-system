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
    <v-fade-transition>
        <span class="text-caption" v-show="animationTrigger">
            {{ label }} {{ dateTimeFormat.format(date) }}
        </span>
    </v-fade-transition>
</template>

<script lang="ts">
import {defineComponent} from 'vue'

export default defineComponent({
    name: "LastUpdated",

    props: {
        date: {type: Date, required: true},
        label: {type: String, default: "Last updated:"},
    },

    data() {
        return {
            animationTrigger: true,
            dateTimeFormat: new Intl.DateTimeFormat('de-DE', {
                year: 'numeric',
                month: '2-digit',
                day: '2-digit',
                hour: '2-digit',
                minute: '2-digit',
                second: '2-digit',
            }),
        }
    },

    watch: {
        date() {
            this.animationTrigger = false;
            setTimeout(() => {
                this.animationTrigger = true;
            }, 250);
        }
    }
})
</script>