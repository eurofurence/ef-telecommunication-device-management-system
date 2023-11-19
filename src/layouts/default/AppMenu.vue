<template>
    <v-navigation-drawer
        permanent
        location="left"
    >
        <v-list density="compact" nav>
            <v-list-item prepend-icon="mdi-home-city" title="Overview" value="overview" to="/overview"></v-list-item>
            <v-list-item prepend-icon="mdi-account" title="My Account" value="account" to="/profile"></v-list-item>
            <v-list-item prepend-icon="mdi-account-group-outline" title="Users" value="users" to="/users"></v-list-item>
        </v-list>

        <template v-slot:append>
            <v-divider></v-divider>
            <v-list density="compact" small>
                <v-list-item prepend-icon="mdi-logout" title="Logout" value="logout" to="/logout"></v-list-item>
            </v-list>
        </template>
    </v-navigation-drawer>
</template>
