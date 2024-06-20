<template>
    <v-card>
        <v-card-title v-if="!isEdit">New Radio Accessory</v-card-title>
        <v-card-title v-if="isEdit">Edit Radio Accessory</v-card-title>
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
                    :fetch-function="itemsStore.fetchRadioAccessoryTemplatesPage"
                    :prefetch="true"
                    label="Radio Accessory Template"
                    icon="mdi-headset"
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
                <v-slider
                    v-if="!isEdit"
                    v-model="data.amount"
                    :step="1"
                    :min="1"
                    :max="200"
                    :rules="rules.amount"
                >
                    <template v-slot:prepend>
                        <span class="text-grey-darken-2">
                            <v-icon>mdi-counter</v-icon>&nbsp;Amount
                        </span>
                    </template>

                    <template v-slot:append>
                        <v-text-field
                            v-model="data.amount"
                            type="number"
                            min="1"
                            max="200"
                            step="1"
                            variant="outlined"
                            density="compact"
                            style="width: 80px"
                            hide-details
                            class="ml-2"
                        ></v-text-field>
                    </template>
                </v-slider>

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
    name: "RadioAccessoriesForm",

    components: {ServerItemSelector},

    emits: ['submit', 'abort'],

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
                amount: 1,
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
                amount: [
                    (v: number) => (v >= 1) || 'Amount must be greater than or equal to 1',
                    (v: number) => (v <= 200) || 'Amount must be less than or equal to 200',
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
                        amount: 1,
                    };
                } else {
                    this.data = {
                        id: item.id,
                        template: item.template,
                        serialnumber: item.serialnumber ?? '',
                        notes: item.notes ?? '',
                        amount: item.amount,
                    };
                }
            },
        },
    },

    computed: {
        isEdit() {
            return this.item !== null;
        }
    },
});
</script>
