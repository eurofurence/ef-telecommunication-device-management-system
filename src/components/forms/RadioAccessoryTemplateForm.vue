<template>
    <v-card>
        <v-card-title v-if="!isEdit">New Radio Accessory Template</v-card-title>
        <v-card-title v-if="isEdit">Edit Radio Accessory Template</v-card-title>
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
                <v-text-field
                    v-model="data.name"
                    label="Template Name"
                    :rules="rules.name"
                    variant="outlined"
                    prepend-inner-icon="mdi-format-title"
                ></v-text-field>
                <ServerItemSelector
                    ref="ownerSelector"
                    :fetch-function="usersStore.fetchItemOwnersPage"
                    :prefetch="true"
                    label="Item Owner"
                    icon="mdi-account-arrow-right"
                    item-title-key="pretty_name"
                    item-value-key="id"
                    :autofocus="false"
                    :no-filter="true"
                    @update:selection="data.owner = $event.id"
                ></ServerItemSelector>
                <v-text-field
                    v-model="data.description"
                    label="Description"
                    :rules="rules.description"
                    variant="outlined"
                    prepend-inner-icon="mdi-pencil"
                ></v-text-field>
                <v-switch
                    v-model="data.allow_quickadd"
                    :rules="rules.allow_quickadd"
                    color="primary"
                >
                    <template v-slot:label>
                        <v-icon>mdi-timer-plus-outline</v-icon>
                        &nbsp;
                        Allow Quickadd
                    </template>
                </v-switch>

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
import {useUsersStore} from "@/store/users";

const usersStore = useUsersStore();

export default defineComponent({
    name: "RadioDeviceTemplateForm",

    components: {ServerItemSelector},

    props: {
        item: {type: Object, required: false, default: null},
    },

    data() {
        return {
            isValid: false,
            data: {
                id: null,
                name: '',
                owner: null,
                description: '',
                allow_quickadd: false,
            },
            rules: {
                name: [
                    (v: string) => !!v || 'Name is required',
                    (v: string) => (v.length <= 128) || 'Name must be less than 128 characters',
                ],
                owner: [
                    (v: any) => !!v || 'Owner is required',
                    (v: string) => (/^[0-9]+/.test(v)) || 'Owner is invalid',
                ],
                description: [
                    (v: string) => (v.length <= 256) || 'Description must be less than 256 characters',
                ],
                allow_quickadd: [
                    (v: any) => v !== null || 'Quickadd is required',
                ],
            },
        }
    },

    computed: {
        isEdit() {
            return this.item !== null;
        }
    },
});
</script>
