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
                path: 'users',
                name: 'Users',
                component: () => import('@/views/Users.vue'),
                meta: { requiresAuth: true },
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
