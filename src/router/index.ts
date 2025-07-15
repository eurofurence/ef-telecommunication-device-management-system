/* Eurofurence Telecommunication Device Management System (EF-TDMS)
 * Copyright (C) 2025 Niels Gandraß <niels@gandrass.de>
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

// Composables
import {createRouter, createWebHistory} from 'vue-router'
import {useAuthStore} from "@/store/auth";

const routes = [{
    path: '/',
    component: () => import('@/layouts/default/Default.vue'),
    children: [
        {
            path: '',
            name: 'Home',
            component: () => import(/* webpackChunkName: "home" */ '@/views/Home.vue'),
            meta: { requiresAuth: false },
            beforeEnter: (to: any, from: any, next: any) => {
                // Redirect authorized users to the overview page
                const authStore = useAuthStore()
                if (authStore.isLoggedIn) {
                    next('/overview')
                } else {
                    next()
                }
            }
        },
        {
            path: 'login',
            name: 'Login',
            component: () => import('@/views/Login.vue'),
            meta: { requiresAuth: false },
        },
        {
            path: 'logout',
            name: 'Logout',
            component: () => import('@/views/Logout.vue'),
            meta: { requiresAuth: true },
        },
        {
            path: 'overview',
            name: 'Overview',
            component: () => import('@/views/Overview.vue'),
            meta: { requiresAuth: true },
        },
        {
            path: 'profile',
            name: 'Profile',
            component: () => import('@/views/Profile.vue'),
            meta: { requiresAuth: true },
        },
        {
            path: 'inventory',
            name: 'Inventory',
            component: () => import('@/views/Inventory.vue'),
            meta: { requiresAuth: true },
        },
        {
            path: 'deployment-map/:floor/:highlightItemId(\\d+)?',
            name: 'Deployment Map',
            component: () => import('@/views/DeploymentMap.vue'),
            props: true,
            meta: { requiresAuth: true },
            beforeEnter: (to: any, from: any, next: any) => {
                to.params.floor = parseInt(to.params.floor)
                // Redirect to the ground floor if the floor parameter is invalid
                if (isNaN(to.params.floor) || [-1, 0, 1, 2, 3, 4, 100].indexOf(to.params.floor) === -1) {
                    next('/deployment-map/0')
                } else {
                    next()
                }
            }
        },
        {
            path: 'bindings/overview',
            name: 'Bindings Overview',
            component: () => import('@/views/bindings/BindingsOverview.vue'),
            meta: { requiresAuth: true },
        },
        {
            path: 'bindings/preorders',
            name: 'Pre-Orders',
            component: () => import('@/views/bindings/BindingsPreorders.vue'),
            meta: { requiresAuth: true },
        },
        {
            path: 'bindings/issue',
            name: 'Create Binding',
            component: () => import('@/views/bindings/BindingsIssue.vue'),
            meta: { requiresAuth: true },
        },
        {
            path: 'bindings/return',
            name: 'Return Binding',
            component: () => import('@/views/bindings/BindingsReturn.vue'),
            meta: { requiresAuth: true },
        },
        {
            path: 'users',
            name: 'Users',
            component: () => import('@/views/people/Users.vue'),
            meta: { requiresAuth: true },
        },
        {
            path: 'itemowners',
            name: 'Item Owners',
            component: () => import('@/views/people/ItemOwners.vue'),
            meta: {requiresAuth: true},
        },
        {
            path: 'radio/devices',
            name: 'Radios',
            component: () => import('@/views/radio/RadioDevices.vue'),
            meta: {requiresAuth: true},
        },
        {
            path: 'radio/accessories',
            name: 'Accessories',
            component: () => import('@/views/radio/RadioAccessories.vue'),
            meta: {requiresAuth: true},
        },
        {
            path: 'radio/codings',
            name: 'Codings',
            component: () => import('@/views/radio/RadioCodings.vue'),
            meta: {requiresAuth: true},
        },
        {
            path: 'radio/pagers',
            name: 'Pagers',
            component: () => import('@/views/radio/RadioPagers.vue'),
            meta: {requiresAuth: true},
        },
        {
            path: 'voip/phones',
            name: 'Phones',
            component: () => import('@/views/voip/VoipPhones.vue'),
            meta: {requiresAuth: true},
        },
        {
            path: 'voip/callboxes',
            name: 'Callboxes',
            component: () => import('@/views/voip/VoipCallboxes.vue'),
            meta: {requiresAuth: true},
        },
        {
            path: 'voip/provisioning',
            name: 'Provisioning',
            component: () => import('@/views/voip/VoipProvisioning.vue'),
            meta: {requiresAuth: true},
        },
        {
            path: 'eventlog',
            name: 'Event Log',
            component: () => import('@/views/EventLog.vue'),
            meta: {requiresAuth: true},
        }
    ],
}]

const router = createRouter({
    history: createWebHistory(process.env.BASE_URL),
    routes,
})

// Block unauthorized access to routes that require authentication
router.beforeEach((to, _) => {
    if (to.meta.requiresAuth) {
        const authStore = useAuthStore()
        if (!authStore.isLoggedIn) {
            return '/login';
        }
    }
});

export default router
