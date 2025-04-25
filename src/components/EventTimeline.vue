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
    <v-timeline v-if="!loading" side="end">
        <v-timeline-item
            v-for="event in eventsToDisplay"
            :key="event.id"
            :dot-color="event.type.color"
            :icon="event.type.icon"
            fill-dot
        >
            <template v-slot:opposite>
                <div class="text-right">
                    <p>{{ event.user }}</p>
                    <p class="text-caption">{{ event.date }}</p>
                </div>
            </template>
            <div class="text-left">
                <p>{{ event.message }}</p>
                <p class="text-caption">{{ event.description }}</p>
            </div>
        </v-timeline-item>
    </v-timeline>
    <v-timeline v-if="loading" side="end">
        <v-timeline-item
            v-for="idx in loaderHeight"
            :key="idx"
            dot-color="grey"
            fill-dot
        >
            <template v-slot:opposite>
                <div class="text-right" style="width: 200px; max-width: 200px;">
                    <v-skeleton-loader type="list-item"></v-skeleton-loader>
                </div>
            </template>
            <div class="text-left" style="width: 400px; max-width: 400px;">
                <v-skeleton-loader type="list-item"></v-skeleton-loader>
            </div>
        </v-timeline-item>
    </v-timeline>
    <p v-if="!loading && events.length === 0" class="text-center">No events to display</p>
</template>

<script lang="ts">
import {defineComponent} from 'vue';
import {LogEventType} from "@/types/LogEvent";
import type {LogEvent} from "@/types/LogEvent";

export default defineComponent({
    name: "EventTimeline",

    props: {
        events: {type: Array, required: true},
        loading: {type: Boolean, required: false, default: false},
        loaderHeight: {type: Number, required: false, default: 10}
    },

    computed: {
        eventsToDisplay(): LogEvent[] {
            return this.events.map((entry: any) => {
                let type = LogEventType.get(entry.action);
                return {
                    id: entry.id,
                    date: entry.timestamp,
                    user: entry.user.pretty_name,
                    type: type,
                    message: type.label,
                    description: type.description(entry.data),
                }
            })
        }
    },
})
</script>
