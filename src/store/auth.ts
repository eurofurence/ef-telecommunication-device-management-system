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

import { defineStore } from 'pinia'
import axios from '@/plugins/axios'

export const useAuthStore = defineStore('auth', {
    state: () => {
        // Restore the access token from localStorage, if it exists
        if (localStorage.getItem('auth.accessToken') !== null) {
            axios.defaults.headers['Authorization'] = `Bearer ${localStorage.getItem('auth.accessToken')}`;
        }

        return {
            /** The access token, used with every API request */
            _accessToken: localStorage.getItem('auth.accessToken'),

            /** The refresh token, used to refresh the access token */
            _refreshToken: localStorage.getItem('auth.refreshToken'),

            /** The username of the currently logged-in user */
            _username: localStorage.getItem('auth.username'),

            /** The user ID of the currently logged-in user */
            _userid: localStorage.getItem('auth.userid'),
        };
    },

    getters: {
        /**
         * Returns true if the user is logged in, false otherwise.
         * @param state
         */
        isLoggedIn: state => state._refreshToken !== null,

        /**
         * Returns the username of the currently logged-in user.
         * @param state
         */
        username: state => state._username,

        /**
         * Returns the user ID of the currently logged-in user.
         * @param state
         */
        userid: state => state._userid,
    },

    actions: {
        /**
         * Sets the access and refresh tokens and persists them to local storage.
         * Also updates the Authorization header for axios.
         *
         * @param accessToken
         * @param refreshToken
         * @param username
         */
        setAuthTokens(accessToken: string | null, refreshToken: string | null, username: string | null) {
            this._accessToken = accessToken;
            this._refreshToken = refreshToken;
            this._username = username;

            if (this._accessToken !== null) {
                axios.defaults.headers['Authorization'] = `Bearer ${this._accessToken}`;
            } else {
                axios.defaults.headers['Authorization'] = null;
            }

            this.persist();
        },

        /**
         * Persists the access and refresh tokens to localStorage.
         */
        persist() {
            if (this._refreshToken !== null) {
                localStorage.setItem('auth.refreshToken', this._refreshToken);
            } else {
                localStorage.removeItem('auth.refreshToken');
            }

            if (this._accessToken !== null) {
                localStorage.setItem('auth.accessToken', this._accessToken);
            } else {
                localStorage.removeItem('auth.accessToken');
            }

            if (this._username !== null) {
                localStorage.setItem('auth.username', this._username);
            } else {
                localStorage.removeItem('auth.username');
            }
        },

        /**
         * Logs in the user by retrieving a refresh and an access token.
         *
         * @param username
         * @param password
         */
        async login(username: string, password: string) {
            await axios.post(`${import.meta.env.VITE_EFTDMS_API_BASE_URL}/token/obtain/`, {
                username: username,
                password: password,
            }).then((response) => {
                this.setAuthTokens(response.data.access, response.data.refresh, username);
            }).catch((error) => {
                throw error;
            })
        },

        /**
         * Logs out the user.
         */
        logout() {
            this.setAuthTokens(null, null, null);
        },

        /**
         * Refreshes the current access token.
         */
        async refresh() {
             await axios.post(`${import.meta.env.VITE_EFTDMS_API_BASE_URL}/token/refresh/`, {
                refresh: this._refreshToken
             }).then((response) => {
                 this.setAuthTokens(response.data.access, response.data.refresh, this.username);
             }).catch((error) => {
                throw error;
             });
        },
    },
})
