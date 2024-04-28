import axios from 'axios';
import { useToast } from 'vue-toastification';
import { useAuthStore } from "@/store/auth";
import router from "@/router";

const toast = useToast();

axios.defaults.xsrfHeaderName = "X-CSRFToken"
axios.defaults.xsrfCookieName = 'csrftoken'

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
    }
);


// Register auth axios interceptor
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