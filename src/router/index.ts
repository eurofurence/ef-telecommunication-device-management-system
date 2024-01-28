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
                path: 'deployment-map',
                name: 'Deployment Map',
                component: () => import('@/views/DeploymentMap.vue'),
                meta: { requiresAuth: true },
            },
            {
                path: 'bindings/overview',
                name: 'Bindings Overview',
                component: () => import('@/views/BindingsOverview.vue'),
                meta: { requiresAuth: true },
            },
            {
                path: 'bindings/issue',
                name: 'Create Binding',
                component: () => import('@/views/BindingsIssue.vue'),
                meta: { requiresAuth: true },
            },
            {
                path: 'bindings/return',
                name: 'Return Binding',
                component: () => import('@/views/BindingsReturn.vue'),
                meta: { requiresAuth: true },
            },
            {
                path: 'users',
                name: 'Users',
                component: () => import('@/views/Users.vue'),
                meta: { requiresAuth: true },
            },
            {
                path: 'itemowners',
                name: 'Item Owners',
                component: () => import('@/views/ItemOwners.vue'),
                meta: {requiresAuth: true},
            },
            {
                path: 'radio/devices',
                name: 'Radios',
                component: () => import('@/views/RadioDevices.vue'),
                meta: {requiresAuth: true},
            },
            {
                path: 'radio/accessories',
                name: 'Accessories',
                component: () => import('@/views/RadioAccessories.vue'),
                meta: {requiresAuth: true},
            },
            {
                path: 'radio/pagers',
                name: 'Pagers',
                component: () => import('@/views/RadioPagers.vue'),
                meta: {requiresAuth: true},
            },
            {
                path: 'voip/phones',
                name: 'Phones',
                component: () => import('@/views/VoipPhones.vue'),
                meta: {requiresAuth: true},
            },
            {
                path: 'voip/callboxes',
                name: 'Callboxes',
                component: () => import('@/views/VoipCallboxes.vue'),
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
