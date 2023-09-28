import { defineStore } from 'pinia'
import axios from '@/plugins/axios'

// Register auth axios interceptor
axios.interceptors.response.use((response) => {
    return response;
}, async (error) => {
    if (error.response) {
        if (useAuthStore().isLoggedIn) {
            // Try to refresh the access token if the request failed with a 401
            if (error.response.status === 401 && !error.config._isRetry) {
                // Do not refresh a refresh
                if (error.config.url?.includes('token/refresh/')) {
                    console.debug('Request failed with 401, but it was a refresh request. Logging out and aborting...');
                    useAuthStore().logout();
                    return Promise.reject(error);
                }

                // Mark the request as a retry
                error.config._isRetry = true;
                console.debug('Request failed with 401, trying to refresh the access token...');

                // Try to refresh the access token and retry original request
                try {
                    await useAuthStore().refresh();
                    error.config.headers['Authorization'] = axios.defaults.headers['Authorization'];
                    return axios(error.config);
                } catch (innerError: any) {
                    if (innerError.response && innerError.response.data) {
                        return Promise.reject(innerError.response.data);
                    }

                    return Promise.reject(innerError);
                }
            }
        }

        if (error.response.status === 403 && error.response.data) {
            return Promise.reject(error.response.data);
        }
    }

    return Promise.reject(error);
});

export const useAuthStore = defineStore({
    id: 'auth',
    state: () => {
        // Restore the access token from localStorage, if it exists
        if (localStorage.getItem('auth.accessToken') !== null) {
            axios.defaults.headers['Authorization'] = `Bearer ${localStorage.getItem('auth.accessToken')}`;
        }

        return {
            /** The access token, used with every API request */
            accessToken: localStorage.getItem('auth.accessToken'),

            /** The refresh token, used to refresh the access token */
            refreshToken: localStorage.getItem('auth.refreshToken'),
        };
    },
    getters: {
        /**
         * Returns true if the user is logged in, false otherwise.
         * @param state
         */
        isLoggedIn: state => state.refreshToken !== null,
    },
    actions: {
        /**
         * Sets the access and refresh tokens and persists them to local storage.
         * Also updates the Authorization header for axios.
         *
         * @param accessToken
         * @param refreshToken
         */
        setAuthTokens(accessToken: string | null, refreshToken: string | null) {
            this.accessToken = accessToken;
            this.refreshToken = refreshToken;

            if (this.accessToken !== null) {
                axios.defaults.headers['Authorization'] = `Bearer ${this.accessToken}`;
            } else {
                axios.defaults.headers['Authorization'] = null;
            }

            this.persist();
        },

        /**
         * Persists the access and refresh tokens to localStorage.
         */
        persist() {
            if (this.refreshToken !== null) {
                localStorage.setItem('auth.refreshToken', this.refreshToken);
            } else {
                localStorage.removeItem('auth.refreshToken');
            }

            if (this.accessToken !== null) {
                localStorage.setItem('auth.accessToken', this.accessToken);
            } else {
                localStorage.removeItem('auth.accessToken');
            }
        },

        /**
         * Logs in the user by retrieving a refresh and an access token.
         *
         * @param username
         * @param password
         */
        async login(username: string, password: string) {
            await axios.post(`${import.meta.env.VITE_EFRMS_API_BASE_URL}/token/obtain/`, {
                username: username,
                password: password,
            }).then((response) => {
                this.setAuthTokens(response.data.access, response.data.refresh);
            }).catch((error) => {
                throw error;
            })
        },

        /**
         * Logs out the user.
         */
        logout() {
            this.setAuthTokens(null, null);
        },

        /**
         * Refreshes the current access token.
         */
        async refresh() {
             await axios.post(`${import.meta.env.VITE_EFRMS_API_BASE_URL}/token/refresh/`, {
                refresh: this.refreshToken
             }).then((response) => {
                 this.setAuthTokens(response.data.access, response.data.refresh);
             }).catch((error) => {
                throw error;
             });
        },
    },
})
