<template>
    <v-timeline side="end">
        <v-timeline-item
            v-for="event in events"
            :key="event.id"
            :dot-color="event.color"
            :icon="event.icon"
            fill-dot
        >
            <template v-slot:opposite>
                {{ event.date }}
            </template>
            {{ event.title }}<br/>
            {{ event.subtitle }}
        </v-timeline-item>
    </v-timeline>
</template>

<script lang="ts">
import {defineComponent} from 'vue';
import type {PropType} from 'vue';
import {LogEvent} from "@/types/LogEvent";

export default defineComponent({
    name: "EventTimeline",

    props: {
        events: {type: Array as PropType<LogEvent[]>, required: true},
    },

    data() {
        return {
            events: [
                {id: 1, title: "Event 1", subtitle: "Subtitle 1", date: '01.02.23 12:34', color: "primary", icon: "mdi-account-arrow-right-outline"},
                {id: 2, title: "Event 2", subtitle: "Subtitle 2", date: '01.02.23 12:34', color: "red", icon: "mdi-account-arrow-left-outline"},
                {id: 3, title: "Event 3", subtitle: "Subtitle 3", date: '01.02.23 12:34', color: "green-lighten-1", icon: "mdi-flask"},
                {id: 4, title: "Event 4", subtitle: "Subtitle 4", date: '01.02.23 12:34', color: "blue-lighten-1", icon: "mdi-account-arrow-right-outline"},
                {id: 5, title: "Event 5", subtitle: "Subtitle 5", date: '01.02.23 12:34', color: "purple-lighten-2", icon: "mdi-account-arrow-left-outline"},
            ]
        }
    }
})
</script>
