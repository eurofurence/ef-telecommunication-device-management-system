<template>
    <v-card>
        <v-card-title v-if="!isEdit">New Pager</v-card-title>
        <v-card-title v-if="isEdit">Edit Pager</v-card-title>
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
                    :fetch-function="itemsStore.fetchPagerTemplatesPage"
                    :prefetch="true"
                    label="Pager Template"
                    icon="mdi-bell-ring-outline"
                    item-title-key="pretty_name"
                    item-value-key="id"
                    :autofocus="false"
                    :no-filter="true"
                    :initial-selection="data.template"
                    @update:selection="data.template = $event"
                ></ServerItemSelector>
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
    name: "PagerForm",

    components: {ServerItemSelector},

    emits: ['abort', 'submit'],

    props: {
        item: {type: Object, required: false, default: null},
    },

    data() {
        return {
            isValid: false,
            data: {
                id: null,
                template: null as any,
                serialnumber: '',
                notes: '',
            },
            rules: {
                template: [
                    (v: any) => !!v || 'Template is required',
                    (v: any) => (/^[0-9]+/.test(v.id)) || 'Template is invalid',
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

    watch: {
        item: {
            immediate: true,
            handler(item) {
                if (item === null) {
                    this.data = {
                        id: null,
                        template: null,
                        serialnumber: '',
                        notes: '',
                    };
                } else {
                    this.data = {
                        id: item.id,
                        template: item.template,
                        serialnumber: item.serialnumber ?? '',
                        notes: item.notes ?? '',
                    };
                }
            }
        }
    },

    computed: {
        isEdit() {
            return this.item !== null;
        }
    },
});
</script>
