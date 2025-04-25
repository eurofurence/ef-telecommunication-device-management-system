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

import {ItemType} from "@/types/ItemType";
import type {ItemTypeMetadata} from "@/types/ItemType";

export class IconUtils {

    /**
     * Generates an mdi-map-marker icon with the specified color
     *
     * @param color The color of the icon in hexadecimal format (e.g. #000000)
     * @returns The base64 encoded SVG icon
     */
    public static MapMarker(color = '#000000') {
        return 'data:image/svg+xml;base64,' + btoa(`
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
                <path style="fill:${color};" d="M12,11.5A2.5,2.5 0 0,1 9.5,9A2.5,2.5 0 0,1 12,6.5A2.5,2.5 0 0,1 14.5,9A2.5,2.5 0 0,1 12,11.5M12,2A7,7 0 0,0 5,9C5,14.25 12,22 12,22C12,22 19,14.25 19,9A7,7 0 0,0 12,2Z"/>
            </svg>
        `);
    }

    /**
     * Generates an mdi-map-marker icon with the specified color
     *
     * @param color The color of the icon in hexadecimal format (e.g. #000000)
     * @returns A base64 encoded SVG image
     */
    public static MapMarkerFilled(color = '#000000') {
        return 'data:image/svg+xml;base64,' + btoa(`
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
                <path style="fill:${color};" d="M 12,2 C 8.1340068,2 5,5.1340068 5,9 c 0,5.25 7,13 7,13 0,0 7,-7.75 7,-13 0,-3.8659932 -3.134007,-7 -7,-7 z"/>
            </svg>
        `);
    }

    public static MapMarkerWithItemType(itemType: string, color = '#000000', overlayColor = '#FFFFFF') {
        // Determine the overlay icon
        let itemIconSVG = '';
        switch (itemType) {
            case ItemType.RadioDevice.key:
                // mdi-cellphone-basic
                itemIconSVG = `<g transform="scale(0.45 0.45) translate(14 9)"><path style="fill:${overlayColor};" d="M15,2A1,1 0 0,0 14,3V6H10C8.89,6 8,6.89 8,8V20C8,21.11 8.89,22 10,22H15C16.11,22 17,21.11 17,20V8C17,7.26 16.6,6.62 16,6.28V3A1,1 0 0,0 15,2M10,8H15V13H10V8M10,15H11V16H10V15M12,15H13V16H12V15M14,15H15V16H14V15M10,17H11V18H10V17M12,17H13V18H12V17M14,17H15V18H14V17M10,19H11V20H10V19M12,19H13V20H12V19M14,19H15V20H14V19Z" /></g>`;
                break;
            case ItemType.RadioAccessory.key:
                // mdi-headset
                itemIconSVG = `<g transform="scale(0.42 0.42) translate(16.5 10)"><path style="fill:${overlayColor};" d="M12,1C7,1 3,5 3,10V17A3,3 0 0,0 6,20H9V12H5V10A7,7 0 0,1 12,3A7,7 0 0,1 19,10V12H15V20H19V21H12V23H18A3,3 0 0,0 21,20V10C21,5 16.97,1 12,1Z" /></g>`;
                break;
            case ItemType.Pager.key:
                // mdi-bell-ring
                itemIconSVG = `<g transform="scale(0.42 0.42) translate(16 10)"><path style="fill:${overlayColor}" d="M21,19V20H3V19L5,17V11C5,7.9 7.03,5.17 10,4.29C10,4.19 10,4.1 10,4A2,2 0 0,1 12,2A2,2 0 0,1 14,4C14,4.1 14,4.19 14,4.29C16.97,5.17 19,7.9 19,11V17L21,19M14,21A2,2 0 0,1 12,23A2,2 0 0,1 10,21M19.75,3.19L18.33,4.61C20.04,6.3 21,8.6 21,11H23C23,8.07 21.84,5.25 19.75,3.19M1,11H3C3,8.6 3.96,6.3 5.67,4.61L4.25,3.19C2.16,5.25 1,8.07 1,11Z" /></g>`;
                break;
            case ItemType.Phone.key:
                // mdi-phone
                itemIconSVG = `<g transform="scale(0.45 0.45) translate(15 9)"><path style="fill:${overlayColor};" d="M6.62,10.79C8.06,13.62 10.38,15.94 13.21,17.38L15.41,15.18C15.69,14.9 16.08,14.82 16.43,14.93C17.55,15.3 18.75,15.5 20,15.5A1,1 0 0,1 21,16.5V20A1,1 0 0,1 20,21A17,17 0 0,1 3,4A1,1 0 0,1 4,3H7.5A1,1 0 0,1 8.5,4C8.5,5.25 8.7,6.45 9.07,7.57C9.18,7.92 9.1,8.31 8.82,8.59L6.62,10.79Z" /></g>`;
                break;
            case ItemType.Callbox.key:
                // mdi-webcam
                itemIconSVG = `<g transform="scale(0.45 0.45) translate(14.5 8)"><path style="fill:${overlayColor};" d="M12,2A7,7 0 0,1 19,9A7,7 0 0,1 12,16A7,7 0 0,1 5,9A7,7 0 0,1 12,2M12,4A5,5 0 0,0 7,9A5,5 0 0,0 12,14A5,5 0 0,0 17,9A5,5 0 0,0 12,4M12,6A3,3 0 0,1 15,9A3,3 0 0,1 12,12A3,3 0 0,1 9,9A3,3 0 0,1 12,6M6,22A2,2 0 0,1 4,20C4,19.62 4.1,19.27 4.29,18.97L6.11,15.81C7.69,17.17 9.75,18 12,18C14.25,18 16.31,17.17 17.89,15.81L19.71,18.97C19.9,19.27 20,19.62 20,20A2,2 0 0,1 18,22H6Z" /></g>`;
                break;
            default:
                return IconUtils.MapMarker(color);
        }

        return 'data:image/svg+xml;base64,' + btoa(`
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
                <path style="fill:${color};" d="M 12,2 C 8.1340068,2 5,5.1340068 5,9 c 0,5.25 7,13 7,13 0,0 7,-7.75 7,-13 0,-3.8659932 -3.134007,-7 -7,-7 z"/>
                ${itemIconSVG}
            </svg>
        `);
    }

    /**
     * Generates an mdi-tooltip icon with the specified color
     *
     * @param color The color of the icon in hexadecimal format (e.g. #000000)
     * @returns A base64 encoded SVG image
     */
    public static Tooltip(color = '#000000') {
        return 'data:image/svg+xml;base64,' + btoa(`
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
                <path style="fill:${color};" d="M4,2H20A2,2 0 0,1 22,4V16A2,2 0 0,1 20,18H16L12,22L8,18H4A2,2 0 0,1 2,16V4A2,2 0 0,1 4,2Z" />
            </svg>
        `);
    }

}
