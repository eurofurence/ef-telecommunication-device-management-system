<!--
Eurofurence Telecommunication Device Management System (EF-TDMS)
Copyright (C) 2025 Niels Gandraß <niels@gandrass.de>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
-->

<template>
  <router-view />
</template>

<style lang="scss">
html {
    overflow-y: auto !important;
}

.v-container.main-container-boxed {
    max-width: 1400px;
}

@media (max-width: 960px) {
    .binding-stepper .v-window {
        margin: 10px;
    }
    .binding-stepper .v-stepper-item {
        padding: 16px;
        flex-basis: 100px !important;
    }
    .v-stepper-header hr.v-divider {
        display: none;
    }
}

@media (max-width: 600px) {
    .binding-stepper .v-window {
        margin: 4px;
    }
}
</style>