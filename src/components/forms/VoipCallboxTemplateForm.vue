<template>
    <v-card>
        <v-card-title v-if="!isEdit">New Callbox Template</v-card-title>
        <v-card-title v-if="isEdit">Edit Callbox Template</v-card-title>
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
                    icon="mdi-account"
                    item-title-key="pretty_name"
                    item-value-key="id"
                    :autofocus="false"
                    :no-filter="true"
                    @update:selection="data.owner = $event.id"
                ></ServerItemSelector>
                <v-switch
                    v-model="data.private"
                    label="Private Item"
                    color="primary"
                    prepend-icon="mdi-account-lock"
                ></v-switch>
                <v-text-field
                    v-model="data.description"
                    label="Description"
                    :rules="rules.description"
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
import {useUsersStore} from "@/store/users";

const usersStore = useUsersStore();

export default defineComponent({
    name: "VoipCallboxTemplateForm",

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
                private: false,
                description: '',
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
