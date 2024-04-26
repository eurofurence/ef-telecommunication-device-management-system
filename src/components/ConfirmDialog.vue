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