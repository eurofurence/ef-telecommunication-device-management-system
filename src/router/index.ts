// Composables
import {createRouter, createWebHistory} from 'vue-router'
import {useAuthStore} from "@/store/auth";

const routes = [
    {
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
                path: 'deployment-map/:floor',
                name: 'Deployment Map',
                component: () => import('@/views/DeploymentMap.vue'),
                props: true,
                meta: { requiresAuth: true },
                beforeEnter: (to: any, from: any, next: any) => {
                    to.params.floor = parseInt(to.params.floor)
                    // Redirect to the ground floor if the floor parameter is invalid
                    if (isNaN(to.params.floor) || to.params.floor < 0 || to.params.floor > 4) {
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
                path: 'eventlog',
                name: 'Event Log',
                component: () => import('@/views/EventLog.vue'),
                meta: {requiresAuth: true},
            }
        ],
    },
]

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
