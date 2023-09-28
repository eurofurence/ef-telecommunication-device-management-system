import { defineStore } from 'pinia'
import axios from '@/plugins/axios'

export const useUsersStore = defineStore("user", {
    state: () => ({
        /** The list of users */
        users: [],
    }),
    actions: {
        /**
         * Fetches all users from the API.
         */
        async fetchUsers() {
            await axios.get(`${import.meta.env.VITE_EFRMS_API_BASE_URL}/users/`)
                .then((response) => {
                    // TODO: Implement pagination
                    this.users = response.data.results
                })
                .catch((error) => {
                    console.log(error)
                })
        }
    },
})