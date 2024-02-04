<template>
    <h1>Create Binding</h1>
    <v-container>
        <v-row>
            <v-col cols="6">
                <ServerItemSelector
                    :fetch-function="usersStore.fetchUsersPage"
                    label="User"
                    icon="mdi-account"
                    item-title-key="pretty_name"
                    item-value-key="id"
                    @update:selection="onUserSelected"
                ></ServerItemSelector>
            </v-col>
            <v-col cols="6">
                <p>Selected User: {{ selectedUser }}</p>
            </v-col>
        </v-row>
        <v-row>
            <v-col cols="6">
                <ServerItemSelector
                    :fetch-function="itemsStore.fetchRadiosPage"
                    label="Radio"
                    icon="mdi-cellphone-basic"
                    item-title-key="pretty_name"
                    item-value-key="id"
                    @update:selection="onRadioSelected"
                ></ServerItemSelector>
            </v-col>
            <v-col cols="6">
                <p>Selected Radio: {{ selectedRadio }}</p>
            </v-col>
        </v-row>
    </v-container>
</template>

<script setup lang="ts">
import ServerItemSelector from "@/components/ServerItemSelector.vue";
import {useUsersStore} from "@/store/users";
import {useItemsStore} from "@/store/items";

const usersStore = useUsersStore();
const itemsStore = useItemsStore();
</script>

<script lang="ts">
import { defineComponent } from "vue";

export default defineComponent({

    data() {
        return {
            selectedUser: null,
            selectedRadio: null,
        }
    },

    methods: {
        onUserSelected(user: any) {
            this.selectedUser = user;
        },
        onRadioSelected(radio: any) {
            this.selectedRadio = radio;
        }
    }

})

</script>