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
</template>

<script lang="ts">
import {defineComponent} from 'vue';
import {LogEvent, LogEventType} from "@/types/LogEvent";

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
