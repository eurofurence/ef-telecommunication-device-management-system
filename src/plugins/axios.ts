/* Eurofurence Telecommunication Device Management System (EF-TDMS)
 * Copyright (C) 2024 Niels Gandraß <niels@gandrass.de>
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.

 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <https://www.gnu.org/licenses/>.
 */

import axios from 'axios';
import { useToast } from 'vue-toastification';
import { useAuthStore } from "@/store/auth";
import router from "@/router";

const toast = useToast();

axios.defaults.xsrfHeaderName = "X-CSRFToken"
axios.defaults.xsrfCookieName = 'csrftoken'

/**
 * Catch connection refused errors and display a toast message.
 */
axios.interceptors.response.use((response) => response, (error) => {
    if (error.code === 'ERR_NETWORK') {
        toast.error('API Request failed: Connection refused');
    }

    return Promise.reject(error);
});

/**
 * Catch 403 Forbidden errors and display a toast message.
 */
axios.interceptors.response.use((response) => response, (error) => {
    if (error.response) {
        if (error.response.status === 403) {
            if (error.response.data.detail) {
                toast.error(error.response.data.detail);
            } else {
                toast.error('API Request failed with status 403');
            }
        }
    }

    return Promise.reject(error);
});


/**
 * Catch 401 Unauthorized errors and try to refresh the access token.
 */
axios.interceptors.response.use((response) => response, async (error) => {
    if (error.response) {
        const authStore = useAuthStore();

        if (authStore.isLoggedIn) {
            // Try to refresh the access token if the request failed with a 401
            if (error.response.status === 401 && !error.config._isRetry) {
                // Do not refresh a refresh
                if (error.config.url?.includes('token/refresh/')) {
                    console.debug('Request failed with 401, but it was a refresh request. Logging out and aborting...');
                    authStore.logout();
                    router.push('/login');
                    toast.warning('Your session has expired. Please log in again.');
                    return Promise.reject(error);
                }

                // Mark the request as a retry
                error.config._isRetry = true;
                console.debug('Request failed with 401, trying to refresh the access token...');

                // Try to refresh the access token and retry original request
                try {
                    await authStore.refresh();
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

        if (error.response.status === 401 && error.response.data.code === 'user_inactive') {
            authStore.logout();
            router.push('/login');
            toast.error('Your account has been deactivated. Please contact your administrator.');
            return Promise.reject(error);
        }

        if (error.response.status === 403 && error.response.data) {
            return Promise.reject(error.response.data);
        }
    }

    return Promise.reject(error);
});

export default axios