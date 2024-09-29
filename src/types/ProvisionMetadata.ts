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

/**
 * API response object for the provision metadata endpoint.
 */
export type ProvisionMetadata = {
    /** Phone configuration files */
    config: {
        filename: string;
        filesize: number;
        mac: string;
        accountname: string;
        extension: string;
        mpk: { [id: string] : {
                keyMode: string;
                account: string;
                value: string;
                description: string;
            }
        };
    }[];

    /** Firmware files */
    firmware: {
        filename: string;
        filesize: number;
    }[];

    /** Phonebooks */
    phonebook: {
        filename: string;
        filesize: number;
        entries: {
            firstname: string | null;
            lastname: string | null;
            phone: string | number | null;
        }[];
    }[];

    /** Wallpaper */
    wallpaper: {
        filename: string;
        filesize: number;
    } | null;
};