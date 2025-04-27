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

/**
 * Coordinates of an item on the deployment map.
 */
export type ItemCoordinates = {
    floor: number;      /** Floor the item is on **/
    latitude: number;   /** Latitude of the item **/
    longitude: number;  /** Longitude of the item **/
};
