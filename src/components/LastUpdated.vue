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